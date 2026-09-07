#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Render a Mermaid flowchart subset as a flat-editorial flowchart HTML plate.

    uv run scripts/flowfig.py SPEC.mmd [-o OUT.html] [--png OUT.png] [--scale 2]

Supported Mermaid syntax
    graph LR / flowchart TD
    id[Title<br/>sub label]      process node
    id([Title])                  terminal (outlined)
    id((Title))                  terminal (filled, end state)
    id[(Title)]                  store
    id{Question?}                decision
    a --> b   a -.-> b   a --x b arrows: solid, dashed, failure
    a -->|label| b   a -- label --> b   a -.->|label| b
    a -->|[40 ms]| b             a bracketed label renders as a measurement chip
    id:::focus  id:::warn  id:::fail   tone classes (also: class a,b focus)
    id:::below  id:::beside      layout hints: force a node under, or right of, its parent
    subgraph name [Title] ... end        dashed group boundary; groups may nest

Directives (comment lines)
    %% note: An annotation rendered inside the plate.
    %% steps: sdk, relay, queue       numbered badges in this order
    %% width: 1200
"""
from __future__ import annotations

import argparse
import base64
import html
import heapq
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field

INK = "#2B2233"
MUTED = "#80708F"
BODY = "#4D4158"
PAPER = "#FAF9FB"
PLATE = "#FFFFFF"
ACCENT = "#6C5FC7"
ACCENT_INK = "#4D3FA3"
ACCENT_FILL = "#EFEBFA"
ACCENT_LINE = "#C6BEEB"
WARN = "#FFC227"
WARN_INK = "#7A5200"
WARN_FILL = "#FFF4D4"
FAIL = "#FF45A8"
FAIL_INK = "#B01B70"
FAIL_FILL = "#FFEBF5"

SANS = "'Rubik',-apple-system,system-ui,sans-serif"
MONO = "Monaco,Menlo,'Ubuntu Mono',monospace"

TONES = {
    "plain": (PLATE, INK, MUTED),
    "focus": (ACCENT_FILL, ACCENT, ACCENT_INK),
    "warn": (WARN_FILL, WARN, WARN_INK),
    "fail": (FAIL_FILL, FAIL, FAIL_INK),
}
TONE_ALIASES = {"attention": "warn", "failure": "fail", "error": "fail", "accent": "focus"}
LAYOUT_CLASSES = {"below", "beside"}

NODE_COL = "minmax(146px,1fr)"
EDGE_COL = "76px"
NODE_ROW = "auto"
EDGE_ROW = "60px"


def warn(msg: str) -> None:
    print(f"flowfig: {msg}", file=sys.stderr)


# ---------------------------------------------------------------- model


@dataclass
class Node:
    id: str
    title: str
    sub: str = ""
    shape: str = "process"
    tone: str = "plain"
    layout: str | None = None
    group: str | None = None


@dataclass
class Edge:
    src: str
    dst: str
    label: str = ""
    dashed: bool = False
    fail: bool = False


@dataclass
class Group:
    id: str
    title: str
    parent: str | None = None


@dataclass
class Spec:
    direction: str = "LR"
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    groups: dict[str, Group] = field(default_factory=dict)
    meta: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------- parser

SHAPES = [
    ("([", "])", "terminal"),
    ("[(", ")]", "store"),
    ("((", "))", "end"),
    ("[[", "]]", "process"),
    ("[", "]", "process"),
    ("(", ")", "process"),
    ("{", "}", "decision"),
]

ID_RE = re.compile(r"\s*([A-Za-z0-9_]+)")
CLASS_RE = re.compile(r":::([\w,]+)")
ARROW_RE = re.compile(
    r"""\s*(?:
        --\s+(?P<l1>.+?)\s+-->
      | -\.\s+(?P<l2>.+?)\s+\.->
      | ==\s+(?P<l3>.+?)\s+==>
      | (?P<arr>(?:-{2,}|-\.+-|={2,})(?P<head>[>xo]))
    )\s*(?:\|(?P<lp>[^|]*)\|)?\s*""",
    re.X,
)


def split_text(text: str) -> tuple[str, str]:
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] == '"':
        text = text[1:-1]
    parts = re.split(r"<br\s*/?>|\\n", text)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return "", ""
    return parts[0], " · ".join(parts[1:])


class Parser:
    def __init__(self) -> None:
        self.spec = Spec()
        self.group_stack: list[str] = []

    def parse(self, text: str) -> Spec:
        lines = text.splitlines()
        if lines and lines[0].strip() == "---":
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
            if end is not None:
                for fm in lines[1:end]:
                    if ":" in fm:
                        k, v = fm.split(":", 1)
                        self.spec.meta[k.strip().lower()] = v.strip()
                lines = lines[end + 1 :]
        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            m = re.match(r"%%\s*([A-Za-z_]+)\s*:\s*(.*)$", line)
            if m:
                self.spec.meta[m.group(1).lower()] = m.group(2).strip()
                continue
            if line.startswith("%%"):
                continue
            line = re.sub(r"\s%%.*$", "", line).strip()
            for stmt in line.split(";"):
                stmt = stmt.strip()
                if stmt:
                    self.statement(stmt)
        return self.spec

    def statement(self, s: str) -> None:
        m = re.match(r"^(graph|flowchart)\b\s*(\w+)?", s)
        if m:
            d = (m.group(2) or "LR").upper()
            if d in ("TD", "TB", "BT"):
                self.spec.direction = "TD"
            else:
                self.spec.direction = "LR"
            if d in ("RL", "BT"):
                warn(f"direction {d} is not supported; using {self.spec.direction}")
            return
        m = re.match(r"^subgraph\s+(.+)$", s)
        if m:
            body = m.group(1).strip()
            mm = re.match(r'^([^\[\s]+)\s*(?:\[\s*"?(.*?)"?\s*\])?$', body)
            if mm:
                gid, title = mm.group(1), mm.group(2) or mm.group(1)
            else:
                gid, title = body, body
            parent = self.group_stack[-1] if self.group_stack else None
            self.spec.groups[gid] = Group(gid, title, parent)
            self.group_stack.append(gid)
            return
        if s == "end":
            if self.group_stack:
                self.group_stack.pop()
            return
        m = re.match(r"^class\s+([\w,\s]+?)\s+(\w+)$", s)
        if m:
            for nid in re.split(r"[,\s]+", m.group(1)):
                if nid:
                    self.apply_class(self.node(nid), m.group(2))
            return
        if re.match(r"^(classDef|style|linkStyle|click|direction)\b", s):
            return
        self.chain(s)

    def node(self, nid: str) -> Node:
        n = self.spec.nodes.get(nid)
        if n is None:
            n = Node(nid, nid)
            self.spec.nodes[nid] = n
        if self.group_stack and n.group is None:
            n.group = self.group_stack[-1]
        return n

    def apply_class(self, n: Node, cls: str) -> None:
        cls = TONE_ALIASES.get(cls, cls)
        if cls in TONES:
            n.tone = cls
        elif cls in LAYOUT_CLASSES:
            n.layout = cls
        else:
            warn(f"unknown class '{cls}' on node '{n.id}' (ignored)")

    def node_token(self, s: str, pos: int) -> tuple[Node, int]:
        m = ID_RE.match(s, pos)
        if not m:
            raise ValueError(f"expected a node id at: {s[pos:]!r}")
        n = self.node(m.group(1))
        pos = m.end()
        for opener, closer, shape in SHAPES:
            if s.startswith(opener, pos):
                end = s.find(closer, pos + len(opener))
                if end < 0:
                    raise ValueError(f"unclosed node text in: {s!r}")
                n.title, n.sub = split_text(s[pos + len(opener) : end])
                n.shape = shape
                pos = end + len(closer)
                break
        m = CLASS_RE.match(s, pos)
        if m:
            for cls in m.group(1).split(","):
                self.apply_class(n, cls)
            pos = m.end()
        return n, pos

    def chain(self, s: str) -> None:
        src, pos = self.node_token(s, 0)
        while pos < len(s):
            m = ARROW_RE.match(s, pos)
            if not m or m.end() == pos:
                raise ValueError(f"cannot parse {s[pos:]!r} in: {s!r}")
            label = m.group("l1") or m.group("l2") or m.group("l3") or m.group("lp") or ""
            arrow_text = m.group(0)
            dashed = "." in arrow_text.split("|")[0] and not m.group("l1") and not m.group("l3")
            fail = m.group("head") == "x"
            dst, pos = self.node_token(s, m.end())
            self.spec.edges.append(Edge(src.id, dst.id, label.strip(), dashed, fail))
            src = dst


# ---------------------------------------------------------------- layout


@dataclass
class Placement:
    layer: int
    row: int


def assign_positions(spec: Spec) -> tuple[dict[str, Placement], set[int]]:
    """Return (id -> Placement, indices of back edges)."""
    ids = list(spec.nodes)
    out: dict[str, list[tuple[int, Edge]]] = {i: [] for i in ids}
    for idx, e in enumerate(spec.edges):
        out[e.src].append((idx, e))

    back: set[int] = set()
    state: dict[str, int] = {}

    def dfs(u: str) -> None:
        state[u] = 1
        for idx, e in out[u]:
            if state.get(e.dst) == 1:
                back.add(idx)
            elif e.dst not in state:
                dfs(e.dst)
        state[u] = 2

    for u in ids:
        if u not in state:
            dfs(u)

    fwd = [(i, e) for i, e in enumerate(spec.edges) if i not in back]
    fpred: dict[str, list[Edge]] = {i: [] for i in ids}
    fsucc: dict[str, list[Edge]] = {i: [] for i in ids}
    primary: dict[str, str] = {}
    for _, e in fwd:
        if e.src == e.dst:
            continue
        fpred[e.dst].append(e)
        fsucc[e.src].append(e)
        primary.setdefault(e.src, e.dst)

    def is_drop(e: Edge) -> bool:
        v = spec.nodes[e.dst]
        if v.layout == "beside":
            return False
        if v.layout == "below":
            return True
        return primary[e.src] != e.dst and len(fpred[e.dst]) == 1 and not fsucc[e.dst]

    order_index = {nid: i for i, nid in enumerate(ids)}
    indeg = {i: len(fpred[i]) for i in ids}
    layer: dict[str, int] = {}
    pref: dict[str, int] = {}
    placed: dict[str, Placement] = {}
    occupied: set[tuple[int, int]] = set()
    ready: list[tuple[int, int, int, str]] = []

    def push(v: str) -> None:
        if fpred[v]:
            layer[v] = max(layer[e.src] + (0 if is_drop(e) else 1) for e in fpred[v])
            anchor = fpred[v][0]
            pref[v] = placed[anchor.src].row + (1 if is_drop(anchor) else 0)
        else:
            layer[v] = 0
            pref[v] = 0
        heapq.heappush(ready, (layer[v], pref[v], order_index[v], v))

    for v in ids:
        if indeg[v] == 0:
            push(v)
    while ready:
        _, _, _, v = heapq.heappop(ready)
        r = pref[v]
        while (layer[v], r) in occupied:
            r += 1
        occupied.add((layer[v], r))
        placed[v] = Placement(layer[v], r)
        for e in fsucc[v]:
            indeg[e.dst] -= 1
            if indeg[e.dst] == 0:
                push(e.dst)
    for v in ids:
        if v not in placed:
            warn(f"node '{v}' could not be placed (cycle without entry?)")
            placed[v] = Placement(0, len(placed))
    return placed, back


# ---------------------------------------------------------------- routing

Cell = tuple[int, int]
OPPOSITE = {"L": "R", "R": "L", "T": "B", "B": "T"}


@dataclass
class Piece:
    sides: frozenset[str]
    arrow: str | None
    dashed: bool
    fail: bool
    label: str = ""

    def same_geometry(self, other: "Piece") -> bool:
        return (self.sides, self.arrow, self.dashed, self.fail) == (
            other.sides,
            other.arrow,
            other.dashed,
            other.fail,
        )


def side_toward(frm: Cell, to: Cell) -> str:
    if to[0] > frm[0]:
        return "R"
    if to[0] < frm[0]:
        return "L"
    if to[1] > frm[1]:
        return "B"
    return "T"


def walk(points: list[Cell]) -> list[Cell] | None:
    cells: list[Cell] = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 != x1 and y0 != y1:
            return None
        dx = (x1 > x0) - (x1 < x0)
        dy = (y1 > y0) - (y1 < y0)
        x, y = x0, y0
        while (x, y) != (x1, y1):
            x += dx
            y += dy
            cells.append((x, y))
    return cells


def candidate_paths(a: Cell, b: Cell, direction: str) -> list[list[Cell]]:
    ax, ay = a
    bx, by = b
    paths: list[list[Cell]] = []

    def add(pts: list[Cell]) -> None:
        dedup: list[Cell] = []
        for p in pts:
            if not dedup or dedup[-1] != p:
                dedup.append(p)
        if len(dedup) >= 2 and dedup not in paths:
            paths.append(dedup)

    if ax == bx or ay == by:
        add([a, b])
    rows = [ay, by, ay + 1, by + 1, ay - 1, by - 1]
    cols = [ax, bx, ax + 1, bx - 1, ax - 1, bx + 1]
    row_paths = [[a, (ax, cy), (bx, cy), b] for cy in rows]
    col_paths = [[a, (cx, ay), (cx, by), b] for cx in cols]
    for p in row_paths + col_paths if direction == "LR" else col_paths + row_paths:
        add(p)
    return paths


def route(
    a: Cell, b: Cell, edge: Edge, direction: str, blocked: set[Cell], pieces: dict[Cell, Piece]
) -> list[tuple[Cell, Piece]]:
    fallback: list[tuple[Cell, Piece]] | None = None
    for pts in candidate_paths(a, b, direction):
        cells = walk(pts)
        if cells is None or cells[-1] != b:
            continue
        body = cells[:-1]
        if a in body or b in body or len(set(body)) != len(body):
            continue
        result: list[tuple[Cell, Piece]] = []
        prev = a
        ok = True
        for i, c in enumerate(body):
            nxt = body[i + 1] if i + 1 < len(body) else b
            entry = side_toward(c, prev)
            exit_ = side_toward(c, nxt)
            piece = Piece(
                frozenset({entry, exit_}),
                exit_ if nxt == b else None,
                edge.dashed,
                edge.fail,
            )
            existing = pieces.get(c)
            if c in blocked or (existing is not None and not existing.same_geometry(piece)):
                ok = False
            result.append((c, piece))
            prev = c
        if fallback is None:
            fallback = result
        if ok:
            return result
    if fallback is None:
        raise ValueError(f"no route from {a} to {b}")
    warn(f"edge {edge.src} -> {edge.dst} overlaps another element; check the figure")
    return fallback


def attach_label(result: list[tuple[Cell, Piece]], label: str) -> None:
    if not label:
        return
    def straight(sides: str, wide_axis: int) -> list[Piece]:
        cells = [(c, p) for c, p in result if p.sides == frozenset(sides)]
        wide = [p for c, p in cells if c[wide_axis] % 2 == 0]
        return wide or [p for _, p in cells]

    target = (straight("LR", 0) or straight("TB", 1) or [result[0][1]])[0]
    target.label = label


# ---------------------------------------------------------------- render

ARROW = {
    "R": f"border-left:12px solid {{c}};border-top:8px solid transparent;border-bottom:8px solid transparent;",
    "L": f"border-right:12px solid {{c}};border-top:8px solid transparent;border-bottom:8px solid transparent;",
    "B": f"border-top:12px solid {{c}};border-left:8px solid transparent;border-right:8px solid transparent;",
    "T": f"border-bottom:12px solid {{c}};border-left:8px solid transparent;border-right:8px solid transparent;",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def arrow_div(side: str, color: str, extra: str = "") -> str:
    return f'<div style="width:0;height:0;{ARROW[side].format(c=color)}{extra}"></div>'


def label_div(label: str, fail: bool, extra: str = "") -> str:
    if not label:
        return ""
    m = re.match(r"^\[(.+)\]$", label)
    if m:
        return (
            f'<div style="padding:3px 7px;border-radius:3px;background:{WARN};'
            f"font:500 10px/1.3 {MONO};letter-spacing:.05em;color:{INK};"
            f'white-space:nowrap;{extra}">{esc(m.group(1))}</div>'
        )
    color = FAIL_INK if fail else MUTED
    return (
        f'<div style="font:500 11px/1.3 {MONO};letter-spacing:.08em;text-transform:uppercase;'
        f'color:{color};white-space:nowrap;{extra}">{esc(label)}</div>'
    )


def line_style(horizontal: bool, dashed: bool, color: str) -> str:
    if horizontal:
        return f"flex:1;height:0;border-top:3px dashed {color};" if dashed else f"flex:1;height:3px;background:{color};"
    return f"flex:1;width:0;border-left:3px dashed {color};" if dashed else f"flex:1;width:3px;background:{color};"


def render_piece(p: Piece, area: str) -> str:
    color = FAIL if p.fail else INK
    common = f"{area}align-self:stretch;justify-self:stretch;min-width:0;min-height:0;"
    if p.sides == frozenset("LR"):
        return (
            f'<div style="{common}display:grid;grid-template-rows:1fr auto 1fr;justify-items:stretch;">'
            f'{label_div(p.label, p.fail, "grid-row:1;align-self:end;justify-self:center;padding-bottom:5px;white-space:normal;text-align:center;max-width:100%;")}'
            f'<div style="grid-row:2;display:flex;align-items:center;">'
            f'{arrow_div("L", color) if p.arrow == "L" else ""}'
            f'<div style="{line_style(True, p.dashed, color)}"></div>'
            f'{arrow_div("R", color) if p.arrow == "R" else ""}'
            f"</div></div>"
        )
    if p.sides == frozenset("TB"):
        return (
            f'<div style="{common}display:grid;grid-template-columns:1fr auto 1fr;align-items:stretch;">'
            f'<div style="grid-column:2;display:flex;flex-direction:column;align-items:center;">'
            f'{arrow_div("T", color) if p.arrow == "T" else ""}'
            f'<div style="{line_style(False, p.dashed, color)}"></div>'
            f'{arrow_div("B", color) if p.arrow == "B" else ""}'
            f"</div>"
            f'{label_div(p.label, p.fail, "grid-column:3;align-self:center;padding-left:8px;")}'
            f"</div>"
        )
    return render_corner(p, common, color)


def render_corner(p: Piece, common: str, color: str) -> str:
    style = "dashed" if p.dashed else "solid"
    quadrants: dict[tuple[int, int], list[str]] = {}
    if "L" in p.sides:
        quadrants.setdefault((1, 1), []).append(f"border-bottom:3px {style} {color};margin-bottom:-1.5px;margin-right:-1.5px;")
    if "T" in p.sides:
        quadrants.setdefault((1, 1), []).append(f"border-right:3px {style} {color};margin-right:-1.5px;margin-bottom:-1.5px;")
    if "R" in p.sides:
        quadrants.setdefault((1, 2), []).append(f"border-bottom:3px {style} {color};margin-bottom:-1.5px;margin-left:-1.5px;")
    if "B" in p.sides:
        quadrants.setdefault((2, 1), []).append(f"border-right:3px {style} {color};margin-right:-1.5px;margin-top:-1.5px;")
    parts = [
        f'<div style="grid-row:{r};grid-column:{c};{"".join(styles)}"></div>'
        for (r, c), styles in quadrants.items()
    ]
    if p.arrow:
        place = {
            "T": "grid-row:1;grid-column:1/3;justify-self:center;align-self:start;",
            "B": "grid-row:2;grid-column:1/3;justify-self:center;align-self:end;",
            "L": "grid-row:1/3;grid-column:1;align-self:center;justify-self:start;",
            "R": "grid-row:1/3;grid-column:2;align-self:center;justify-self:end;",
        }[p.arrow]
        parts.append(arrow_div(p.arrow, color, place))
    if p.label:
        inside = ("B" if "B" in p.sides else "T", "L" if "L" in p.sides else "R")
        row = 1 if inside[0] == "B" else 2
        col = 2 if inside[1] == "L" else 1
        align = f"align-self:{'end' if row == 1 else 'start'};justify-self:{'start' if col == 2 else 'end'};"
        parts.append(label_div(p.label, p.fail, f"grid-row:{row};grid-column:{col};{align}padding:6px;"))
    return (
        f'<div style="{common}display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;">'
        + "".join(parts)
        + "</div>"
    )


def badge_div(n: int) -> str:
    return (
        f'<div style="position:absolute;top:-15px;left:-15px;width:30px;height:30px;box-sizing:border-box;'
        f"border-radius:999px;background:{ACCENT};color:#FFFFFF;border:2.5px solid {INK};"
        f'font:700 13px/25px {MONO};text-align:center;">{n}</div>'
    )


Port = tuple[str, bool]


def stub(port: Port | None) -> str:
    if port is None:
        return '<div style="flex:1;"></div>'
    color, dashed = port
    return f'<div style="{line_style(True, dashed, color)}"></div>'


def render_node(n: Node, area: str, step: int | None, ports: dict[str, Port]) -> str:
    fill, shadow, sub_color = TONES[n.tone]
    badge = badge_div(step) if step else ""
    title_color = INK
    if n.shape == "end":
        fill, title_color, sub_color = INK, "#FFFFFF", ACCENT_LINE
    title = f'<div style="font:600 15px/1.2 {SANS};color:{title_color};">{esc(n.title)}</div>'
    sub = (
        f'<div style="font:400 11px/1.3 {MONO};letter-spacing:.05em;color:{sub_color};">{esc(n.sub)}</div>'
        if n.sub
        else ""
    )
    frame = f"border:2.5px solid {INK};background:{fill};box-shadow:4px 4px 0 {shadow};"
    if n.shape == "decision":
        return (
            f'<div style="{area}position:relative;height:154px;display:flex;align-items:center;">'
            f"{badge}{stub(ports.get('L'))}"
            f'<div style="flex:none;width:106px;height:106px;margin:0 22px;{frame}transform:rotate(45deg);'
            f'display:flex;align-items:center;justify-content:center;">'
            f'<div style="transform:rotate(-45deg);font:600 13px/1.15 {SANS};text-align:center;">{esc(n.title)}</div>'
            f"</div>{stub(ports.get('R'))}</div>"
        )
    if n.shape == "store":
        box = "padding:19px 21px;border-radius:50%/18px;align-items:center;text-align:center;"
    elif n.shape in ("terminal", "end"):
        box = "padding:13px 24px;border-radius:999px;align-items:center;text-align:center;"
    else:
        box = "padding:13px 15px;border-radius:10px;"
    return (
        f'<div style="{area}position:relative;display:flex;flex-direction:column;justify-content:center;gap:5px;{box}{frame}">'
        f"{badge}{title}{sub}</div>"
    )


def render_group(g: Group, area: str, bleed: int) -> str:
    return (
        f'<div style="{area}align-self:stretch;justify-self:stretch;margin:-{bleed}px;position:relative;'
        f'border:2.5px dashed {ACCENT_LINE};border-radius:14px;">'
        f'<div style="position:absolute;top:-9px;left:14px;padding:0 6px;background:{PLATE};'
        f'font:700 11px/1.3 {MONO};letter-spacing:.1em;text-transform:uppercase;color:{MUTED};">{esc(g.title)}</div>'
        f"</div>"
    )


FONT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts", "rubik-latin.woff2"
)


def font_face() -> str:
    """Embed Rubik so the page renders offline and headless Chrome never waits on a webfont."""
    if not os.path.exists(FONT_FILE):
        return (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;600;700&display=swap" rel="stylesheet">'
        )
    with open(FONT_FILE, "rb") as fh:
        data = base64.b64encode(fh.read()).decode("ascii")
    return (
        "<style>@font-face{font-family:'Rubik';font-style:normal;font-weight:500 700;font-display:block;"
        f"src:url(data:font/woff2;base64,{data}) format('woff2');}}</style>"
    )


def render(spec: Spec) -> str:
    placed, back = assign_positions(spec)
    if len(spec.nodes) > 9:
        warn(f"{len(spec.nodes)} nodes; the style caps figures at nine")
    accented = sum(1 for n in spec.nodes.values() if n.tone != "plain")
    if accented > 3:
        warn(f"{accented} accented nodes; the style allows at most three")

    def cell_of(nid: str) -> Cell:
        p = placed[nid]
        return (2 * p.layer, 2 * p.row) if spec.direction == "LR" else (2 * p.row, 2 * p.layer)

    node_cells = {nid: cell_of(nid) for nid in spec.nodes}
    blocked = set(node_cells.values())
    pieces: dict[Cell, Piece] = {}
    ports: dict[str, dict[str, Port]] = {nid: {} for nid in spec.nodes}
    for e in spec.edges:
        if e.src == e.dst:
            warn(f"self-loop on '{e.src}' skipped")
            continue
        if spec.nodes[e.dst].tone == "fail":
            e.fail = True
        result = route(node_cells[e.src], node_cells[e.dst], e, spec.direction, blocked, pieces)
        attach_label(result, e.label)
        port: Port = (FAIL if e.fail else INK, e.dashed)
        ports[e.src][side_toward(node_cells[e.src], result[0][0])] = port
        ports[e.dst][side_toward(node_cells[e.dst], result[-1][0])] = port
        if e.fail and spec.direction == "LR" and node_cells[e.dst][1] < node_cells[e.src][1]:
            warn(f"failure edge {e.src} -> {e.dst} routes upward; the style says never do that")
        for c, piece in result:
            existing = pieces.get(c)
            if existing is None:
                pieces[c] = piece
            elif piece.label and not existing.label:
                existing.label = piece.label

    xs = [c[0] for c in list(blocked) + list(pieces)]
    ys = [c[1] for c in list(blocked) + list(pieces)]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    cols = " ".join(NODE_COL if x % 2 == 0 else EDGE_COL for x in range(minx, maxx + 1))
    rows = " ".join(NODE_ROW if y % 2 == 0 else EDGE_ROW for y in range(miny, maxy + 1))

    def area(c: Cell, span: Cell | None = None) -> str:
        x0, y0 = c[0] - minx + 1, c[1] - miny + 1
        if span is None:
            return f"grid-column:{x0};grid-row:{y0};"
        x1, y1 = span[0] - minx + 2, span[1] - miny + 2
        return f"grid-column:{x0}/{x1};grid-row:{y0}/{y1};"

    steps = [s.strip() for s in spec.meta.get("steps", "").split(",") if s.strip()]
    step_of = {nid: i + 1 for i, nid in enumerate(steps)}
    for nid in steps:
        if nid not in spec.nodes:
            warn(f"steps: unknown node '{nid}'")

    def group_chain(nid: str) -> list[str]:
        chain: list[str] = []
        gid = spec.nodes[nid].group
        while gid is not None:
            chain.append(gid)
            gid = spec.groups[gid].parent
        return chain

    members_of = {
        gid: [nid for nid in spec.nodes if gid in group_chain(nid)] for gid in spec.groups
    }

    def nesting_depth(gid: str) -> int:
        children = [g.id for g in spec.groups.values() if g.parent == gid and members_of[g.id]]
        return 1 + max(nesting_depth(c) for c in children) if children else 0

    items: list[str] = []
    for gid in sorted(spec.groups, key=nesting_depth, reverse=True):
        members = [node_cells[nid] for nid in members_of[gid]]
        if not members:
            continue
        lo = (min(c[0] for c in members), min(c[1] for c in members))
        hi = (max(c[0] for c in members), max(c[1] for c in members))
        for nid, c in node_cells.items():
            if nid not in members_of[gid] and lo[0] <= c[0] <= hi[0] and lo[1] <= c[1] <= hi[1]:
                warn(f"group '{gid}' box also covers node '{nid}'")
        items.append(render_group(spec.groups[gid], area(lo, hi), 14 + 22 * nesting_depth(gid)))
    for nid, n in spec.nodes.items():
        items.append(render_node(n, area(node_cells[nid]), step_of.get(nid), ports[nid]))
    for c, p in pieces.items():
        items.append(render_piece(p, area(c)))

    grid = (
        f'<div style="display:grid;grid-template-columns:{cols};grid-template-rows:{rows};'
        f'align-items:center;justify-items:stretch;">' + "".join(items) + "</div>"
    )
    note = spec.meta.get("note", "")
    note_html = (
        f'<div style="margin-top:36px;display:flex;gap:12px;max-width:640px;">'
        f'<div style="width:3px;flex:none;background:{ACCENT};border-radius:2px;"></div>'
        f'<div style="font:500 15px/1.5 {SANS};color:{BODY};">{esc(note)}</div></div>'
        if note
        else ""
    )
    for key in ("fig", "pattern", "caption"):
        if key in spec.meta:
            warn(f"'%% {key}:' is ignored; figures carry no label or caption")

    width = spec.meta.get("width", "1200").rstrip("px")
    title = spec.meta.get("title", "Flow figure")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
{font_face()}
<style>
  body {{ margin:0; padding:40px 32px; background:{PAPER}; color:{INK}; font-family:{SANS}; }}
  figure {{ margin:0 auto; padding:0 12px 12px 0; width:fit-content; min-width:min-content; max-width:{width}px; }}
  .plate {{ background:{PLATE}; border:3px solid {INK}; border-radius:18px; box-shadow:8px 8px 0 {INK}; padding:46px 38px; }}
</style>
</head>
<body>
<figure id="fig">
<div class="plate">{grid}{note_html}</div>
</figure>
</body>
</html>
"""


# ---------------------------------------------------------------- export

CHROME_CANDIDATES = [
    "google-chrome",
    "chromium",
    "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        found = shutil.which(c)
        if found:
            return found
    return None


def run_chrome_proc(proc: subprocess.Popen, done: Callable[[], bool], timeout: float = 60) -> None:
    """Wait until `done()` reports Chrome's output is complete, then kill Chrome.

    Headless Chrome reliably produces its output but does not reliably exit
    afterwards (its shutdown can wait on component extensions), so waiting
    for the process is not an option.
    """
    deadline = time.monotonic() + timeout
    try:
        while time.monotonic() < deadline:
            if done():
                return
            if proc.poll() is not None:
                raise SystemExit("flowfig: Chrome exited without producing the export")
            time.sleep(0.2)
        raise SystemExit(f"flowfig: Chrome did not produce output within {timeout:.0f} seconds")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def export_png(html_path: str, png_path: str, scale: float, width: int) -> None:
    chrome = find_chrome()
    if not chrome:
        raise SystemExit("flowfig: no Chrome or Chromium found for --png")
    url = "file://" + os.path.abspath(html_path)
    workdir = tempfile.mkdtemp(prefix="flowfig-chrome-")
    base = [
        chrome,
        "--headless=new",
        f"--user-data-dir={os.path.join(workdir, 'profile')}",
        "--no-first-run",
        "--no-default-browser-check",
        "--use-mock-keychain",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-component-update",
        "--hide-scrollbars",
        "--disable-gpu",
    ]
    dom_path = os.path.join(workdir, "dom.html")
    png_tmp = os.path.join(workdir, "shot.png")

    def dom_done() -> bool:
        return os.path.exists(dom_path) and open(dom_path, "rb").read().rstrip().endswith(b"</html>")

    def png_done() -> bool:
        return os.path.exists(png_tmp) and open(png_tmp, "rb").read()[-8:] == b"IEND\xaeB`\x82"

    try:
        with open(dom_path, "wb") as fh:
            proc_args = base + [f"--window-size={width},800", "--dump-dom", url]
            proc = subprocess.Popen(proc_args, stdout=fh, stderr=subprocess.DEVNULL)
        run_chrome_proc(proc, dom_done)
        dom = open(dom_path, "rb").read()
        m = re.search(rb'<figure id="fig"[^>]*data-h="(\d+)"', dom)
        height = int(m.group(1)) + 80 if m else 800
        m = re.search(rb'<figure id="fig"[^>]*data-w="(\d+)"', dom)
        if m:
            width = max(width, int(m.group(1)) + 64)
        run_chrome_proc(
            subprocess.Popen(
                base
                + [
                    f"--window-size={width},{height}",
                    f"--force-device-scale-factor={scale}",
                    f"--screenshot={png_tmp}",
                    url,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ),
            png_done,
        )
        shutil.move(png_tmp, png_path)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


MEASURE_SCRIPT = (
    "<script>addEventListener('load',()=>{const f=document.getElementById('fig');"
    "const r=f.getBoundingClientRect();f.dataset.h=Math.ceil(r.bottom);f.dataset.w=Math.ceil(r.width);});</script>"
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="Mermaid spec file (default: stdin)")
    ap.add_argument("-o", "--out", help="HTML output path (default: SPEC with .html, or stdout)")
    ap.add_argument("--png", help="also export a PNG through headless Chrome")
    ap.add_argument("--scale", type=float, default=2, help="device scale factor for --png (default 2)")
    args = ap.parse_args(argv)

    text = open(args.spec, encoding="utf-8").read() if args.spec else sys.stdin.read()
    try:
        spec = Parser().parse(text)
    except ValueError as exc:
        raise SystemExit(f"flowfig: {exc}")
    if not spec.nodes:
        raise SystemExit("flowfig: the spec has no nodes")
    page = render(spec)

    out = args.out
    if out is None and args.spec:
        out = os.path.splitext(args.spec)[0] + ".html"
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page)
        print(out)
    else:
        sys.stdout.write(page)

    if args.png:
        width = int(spec.meta.get("width", "1200").rstrip("px")) + 64
        with tempfile.TemporaryDirectory() as tmp:
            measured = os.path.join(tmp, "fig.html")
            with open(measured, "w", encoding="utf-8") as fh:
                fh.write(page.replace("</body>", MEASURE_SCRIPT + "</body>"))
            export_png(measured, args.png, args.scale, width)
        print(args.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
