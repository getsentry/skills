---
name: presentation-creator
description: Create data-driven presentation slides using React, Vite, and Recharts with Sentry branding. Use when asked to "create a presentation", "build slides", "make a deck", "create a data presentation", "build a Sentry presentation". Scaffolds a complete slide-based app with charts, animations, and single-file HTML output.
---

# Sentry Presentation Builder

Create interactive, data-driven presentation slides using React + Vite + Recharts, styled with the Sentry design system and built as a single distributable HTML file.

## Step 1: Gather Requirements

Ask the user:
1. What is the presentation topic?
2. How many slides (typically 5-8)?
3. What data/charts are needed? (time series, comparisons, diagrams, zone charts)
4. What is the narrative arc? (problem → solution, before → after, technical deep-dive)
5. Do you want speaker notes? (a separate window with slide preview and talking points — useful for rehearsing and presenting)

If the user declines speaker notes, skip `src/notes.json`, `public/notes.html`, the `saveNotesPlugin` in `vite.config.js`, the BroadcastChannel sync, and the embed isolation logic. The `N` key shortcut should also be omitted.

### Data Assessment (CRITICAL)

Before designing any slides, assess whether the source content contains **real quantitative data** (numbers, percentages, measurements, time series, costs, metrics). Only create Recharts visualizations for slides where real data exists. Do NOT fabricate, estimate, or invent data to fill charts.

- **Has real data** → use a Recharts chart (bar, area, line, etc.)
- **Has no data** → use text-based layouts: cards, tables, bullet columns, diagrams, or quote blocks. Do NOT create a chart with made-up numbers.

If the source content is purely qualitative (narrative, opinions, strategy, process descriptions), the presentation should use zero charts. Recharts and `Charts.jsx` should only be included in the project if at least one slide has real data to visualize.

## Step 2: Scaffold the Project

Create the project structure:

```
<project-name>/
├── index.html
├── package.json
├── vite.config.js
├── public/                 # only if speaker notes enabled
│   └── notes.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── Charts.jsx
    └── notes.json          # only if speaker notes enabled
```

### index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet" />
    <title>TITLE</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### package.json

```json
{
  "name": "PROJECT_NAME",
  "private": true,
  "type": "module",
  "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" },
  "dependencies": { "react": "^18.3.1", "react-dom": "^18.3.1", "recharts": "^2.15.3" },
  "devDependencies": { "@vitejs/plugin-react": "^4.3.4", "vite": "^6.0.0", "vite-plugin-singlefile": "^2.3.0" }
}
```

### vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({ plugins: [react(), viteSingleFile()] })
```

If speaker notes are enabled, add the notes plugin to `vite.config.js`. It exposes two dev-server endpoints: `GET /__get-notes` (reads `src/notes.json` from disk with `Cache-Control: no-store`) and `POST /__save-notes` (writes a single note by index). The notes window fetches notes directly from `/__get-notes` — never from a static import — so edits survive hard refreshes and new tabs.

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import fs from 'fs'
import path from 'path'

function saveNotesPlugin() {
  return {
    name: 'save-notes',
    configureServer(server) {
      server.middlewares.use('/__get-notes', (req, res) => {
        try {
          const notesPath = path.resolve('src/notes.json');
          const notes = fs.readFileSync(notesPath, 'utf-8');
          res.setHeader('Content-Type', 'application/json');
          res.setHeader('Cache-Control', 'no-store');
          res.statusCode = 200;
          res.end(notes);
        } catch (e) {
          res.statusCode = 500;
          res.end(e.message);
        }
      });
      server.middlewares.use('/__save-notes', (req, res) => {
        if (req.method !== 'POST') { res.statusCode = 405; res.end(); return; }
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
          try {
            const { index, note } = JSON.parse(body);
            const notesPath = path.resolve('src/notes.json');
            const notes = JSON.parse(fs.readFileSync(notesPath, 'utf-8'));
            notes[index] = note;
            fs.writeFileSync(notesPath, JSON.stringify(notes, null, 2) + '\n');
            res.statusCode = 200;
            res.end('ok');
          } catch (e) {
            res.statusCode = 500;
            res.end(e.message);
          }
        });
      });
    }
  };
}

export default defineConfig({ plugins: [react(), viteSingleFile(), saveNotesPlugin()] })
```

### main.jsx

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './App.css'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
```

## Step 3: Build the Slide System

Read `${CLAUDE_SKILL_ROOT}/references/design-system.md` for the complete Sentry color palette, typography, CSS variables, layout utilities, and animation system.

### App.jsx Structure

Define slides as an array of functions returning JSX:

```jsx
const SLIDES = [
  () => ( /* Slide 0: Title */ ),
  () => ( /* Slide 1: Context */ ),
  // ...
];
```

Each slide function returns a `<div className="slide-content">` with:
1. An `<h2>` heading
2. Optional subtitle paragraph
3. Main content (charts, cards, diagrams, tables)
4. Animation classes: `.anim`, `.d1`, `.d2`, `.d3` for staggered fade-in

Do NOT add category tag pills/badges above headings (e.g., "BACKGROUND", "EXPERIMENTS"). They look generic and add no value. Let the heading speak for itself.

### Navigation

Implement keyboard navigation (ArrowRight/Space = next, ArrowLeft = prev) and a bottom nav overlay with prev/next buttons, dot indicators, and slide number. The nav has **no border or background** — it floats transparently. A small low-contrast Sentry glyph watermark sits fixed in the top-left corner of every slide.

### Speaker Notes

Store notes in `src/notes.json` — a JSON array with one string per slide:

```json
[
  "Welcome everyone...",
  "• First point\n• Second point"
]
```

**CRITICAL: Do NOT use `import NOTES from './notes.json'`.** Static imports get cached by Vite's module system and edits won't survive hard refreshes or new tabs. Instead, fetch notes dynamically at runtime via the `/__get-notes` endpoint:

```jsx
const [notes, setNotes] = useState([]);

useEffect(() => {
  fetch('/__get-notes')
    .then(r => r.json())
    .then(setNotes)
    .catch(() => {});
}, []);
```

Notes are editable directly in the speaker notes window — the user can click the note area, type, and changes are saved to `src/notes.json` via the Vite save plugin. The notes window fetches its own copy from `/__get-notes` on load and keeps a local cache, so it never depends on the main window for note content. This means notes persist across hard refreshes, new tabs, and can be committed to git.

Press **N** to open the speaker notes window.

### Embed Isolation

The speaker notes window (`public/notes.html`) embeds an iframe of the presentation with `?embed=1`. The App must detect embed mode and behave differently:

- **Main window**: broadcasts slide changes via `BroadcastChannel('speaker-notes')`, listens for control messages via `BroadcastChannel('speaker-control')`, handles keyboard navigation.
- **Embed iframe** (`?embed=1`): does **nothing** except listen for `postMessage` goto commands. No BroadcastChannels, no keyboard listeners. This prevents feedback loops between the main window and the iframe.

```jsx
function App() {
  const [cur, setCur] = useState(0);
  const [notes, setNotes] = useState([]);
  const isEmbed = new URLSearchParams(window.location.search).get('embed') === '1';
  const go = useCallback((d) => setCur(c => Math.max(0, Math.min(SLIDES.length - 1, c + d))), []);

  // Fetch notes from disk on mount
  useEffect(() => {
    fetch('/__get-notes')
      .then(r => r.json())
      .then(setNotes)
      .catch(() => {});
  }, []);

  // ── Embed mode: only respond to postMessage goto, nothing else ──
  useEffect(() => {
    if (!isEmbed) return;
    const h = (e) => {
      if (e.data?.type === 'goto') setCur(e.data.slide);
    };
    window.addEventListener('message', h);
    return () => window.removeEventListener('message', h);
  }, [isEmbed]);

  // ── Main window only: broadcast, controls, keyboard ──
  // Broadcast slide number to speaker notes window
  const notesBcRef = React.useRef(null);
  useEffect(() => {
    if (isEmbed) return;
    if (!notesBcRef.current) {
      notesBcRef.current = new BroadcastChannel('speaker-notes');
    }
    notesBcRef.current.postMessage({ slide: cur, total: SLIDES.length, note: notes[cur] || '' });
  }, [cur, isEmbed, notes]);

  // Listen for control messages from speaker notes window
  useEffect(() => {
    if (isEmbed) return;
    const controlBc = new BroadcastChannel('speaker-control');
    controlBc.onmessage = (e) => {
      if (e.data.action === 'next') go(1);
      if (e.data.action === 'prev') go(-1);
      if (e.data.action === 'note-updated') {
        setNotes(prev => {
          const next = [...prev];
          next[e.data.index] = e.data.note;
          return next;
        });
      }
    };
    return () => controlBc.close();
  }, [go, isEmbed]);

  useEffect(() => {
    if (isEmbed) return;
    const h = (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
      if (e.key === 'n' || e.key === 'N') {
        window.open('/notes.html', 'speaker-notes', 'width=1000,height=600');
      }
    };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [go, isEmbed]);

  return (
    <>
      {cur > 0 && <div className="glyph-watermark"><SentryGlyph size={50} /><span className="watermark-title">TITLE</span></div>}
      <div className="progress" style={{ width: `${((cur + 1) / SLIDES.length) * 100}%` }} />
      {SLIDES.map((S, i) => (
        <div key={i} className={`slide ${i === cur ? 'active' : ''}`}>
          <div className={`slide-content${i === cur ? ' anim' : ''}`}>
            <S />
          </div>
        </div>
      ))}
      <Nav cur={cur} total={SLIDES.length} go={go} setCur={setCur} />
    </>
  );
}
```

### public/notes.html

The speaker notes window shows a scaled iframe preview on the left and an editable textarea on the right. **CRITICAL architecture**: the notes window fetches its own notes from `/__get-notes` on load and keeps a local `allNotes` cache. It does NOT rely on the main window's broadcast for note content — only for the current slide number. This ensures notes survive hard refreshes and new tabs. When the user edits a note, it saves to disk via `/__save-notes` and broadcasts `note-updated` back to the main window via the control channel so the main window's React state stays in sync.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Speaker Notes</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Rubik', system-ui, -apple-system, sans-serif;
      background: #1c1028; color: #e8e4ed;
      height: 100vh; display: flex;
    }
    .left {
      width: 50%; flex-shrink: 0; padding: 20px;
      display: flex; flex-direction: column; gap: 12px;
      border-right: 1px solid rgba(255,255,255,0.1);
    }
    .slide-info { font-size: 0.85rem; color: #80708f; font-variant-numeric: tabular-nums; text-align: center; }
    .preview-container {
      background: #000; border-radius: 8px; overflow: hidden;
      position: relative; width: 100%; padding-bottom: 64.2857%; /* 1400:900 */
    }
    .preview-container iframe {
      position: absolute; top: 0; left: 0;
      width: 1400px; height: 900px; border: none;
      pointer-events: none; transform-origin: 0 0;
    }
    .controls { display: flex; gap: 8px; justify-content: center; }
    .controls button {
      background: rgba(255,255,255,0.1); border: none; color: #e8e4ed;
      font-size: 1rem; padding: 6px 16px; border-radius: 6px; cursor: pointer;
    }
    .controls button:hover { background: rgba(255,255,255,0.2); }
    .right { flex: 1; padding: 28px 32px; display: flex; flex-direction: column; gap: 12px; }
    .note-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #6c5fc7; }
    .note {
      font-family: 'Rubik', system-ui, sans-serif;
      font-size: 1.4rem; line-height: 1.6; flex: 1;
      background: transparent; color: #e8e4ed; border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px; padding: 16px; resize: none;
      white-space: pre-wrap; outline: none;
    }
    .note:focus { border-color: #6c5fc7; }
    .note::placeholder { color: #80708f; font-style: italic; }
    .save-status { font-size: 0.7rem; color: #80708f; text-align: right; min-height: 1em; }
  </style>
</head>
<body>
  <div class="left">
    <div class="slide-info" id="info">Press N in the presentation</div>
    <div class="preview-container" id="previewContainer">
      <iframe id="preview" src="/?embed=1"></iframe>
    </div>
    <div class="controls">
      <button id="prev">&larr;</button>
      <button id="next">&rarr;</button>
    </div>
  </div>
  <div class="right">
    <div class="note-label">Speaker Notes</div>
    <textarea class="note" id="note" placeholder="Add notes for this slide..."></textarea>
    <div class="save-status" id="status"></div>
  </div>
  <script>
    const bc = new BroadcastChannel('speaker-notes');
    const controlBc = new BroadcastChannel('speaker-control');
    let currentSlide = 0;
    let allNotes = [];
    const saveTimeouts = new Map();

    // Fetch notes from disk — the single source of truth
    function fetchNotes() {
      return fetch('/__get-notes')
        .then(r => r.json())
        .then(data => { allNotes = data; return data; })
        .catch(() => []);
    }

    function showNoteForSlide(slide) {
      document.getElementById('note').value = allNotes[slide] || '';
    }

    // Load notes on startup
    fetchNotes().then(() => showNoteForSlide(currentSlide));

    function scalePreview() {
      const container = document.getElementById('previewContainer');
      const iframe = document.getElementById('preview');
      const scale = container.offsetWidth / 1400;
      iframe.style.transform = `scale(${scale})`;
    }
    window.addEventListener('resize', scalePreview);
    document.getElementById('preview').addEventListener('load', scalePreview);
    setTimeout(scalePreview, 100);

    function saveNote(index, note) {
      allNotes[index] = note;
      const existingTimeout = saveTimeouts.get(index);
      if (existingTimeout) clearTimeout(existingTimeout);
      const timeout = setTimeout(() => {
        saveTimeouts.delete(index);
        document.getElementById('status').textContent = 'Saving...';
        fetch('/__save-notes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ index, note })
        }).then(r => {
          document.getElementById('status').textContent = r.ok ? 'Saved' : 'Error saving';
          setTimeout(() => { document.getElementById('status').textContent = ''; }, 2000);
        }).catch(() => {
          document.getElementById('status').textContent = 'Error saving';
        });
      }, 500);
      saveTimeouts.set(index, timeout);
    }

    document.getElementById('note').addEventListener('input', (e) => {
      const note = e.target.value;
      saveNote(currentSlide, note);
      controlBc.postMessage({ action: 'note-updated', index: currentSlide, note });
    });

    // Prevent arrow keys from navigating slides while editing
    document.getElementById('note').addEventListener('keydown', (e) => {
      e.stopPropagation();
    });

    bc.onmessage = (e) => {
      const { slide, total } = e.data;
      const previousSlide = currentSlide;
      currentSlide = slide;
      document.getElementById('info').textContent = `Slide ${slide + 1} / ${total}`;
      document.getElementById('preview').contentWindow.postMessage({ type: 'goto', slide }, '*');
      // Avoid resetting cursor while typing on same slide updates
      if (slide !== previousSlide) {
        // Show note from our local cache, not from the broadcast
        showNoteForSlide(slide);
      }
    };

    document.getElementById('prev').addEventListener('click', () => controlBc.postMessage({ action: 'prev' }));
    document.getElementById('next').addEventListener('click', () => controlBc.postMessage({ action: 'next' }));

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); controlBc.postMessage({ action: 'next' }); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); controlBc.postMessage({ action: 'prev' }); }
    });
  </script>
</body>
</html>
```

## Step 4: Create Charts (Only When Data Exists)

**IMPORTANT: Only create charts for slides backed by real, concrete data from the source content.** If a slide's content is qualitative (strategies, learnings, process descriptions, opinions), use text-based layouts instead (cards, tables, bullet lists, columns). Never invent numbers, fabricate percentages, or generate synthetic data to populate a chart. If you are unsure whether data is real or inferred, do NOT create a chart.

If NO slides require charts, skip this step entirely — do not create `Charts.jsx` or import Recharts.

When real data IS available, read `${CLAUDE_SKILL_ROOT}/references/chart-patterns.md` for Recharts component patterns including axis configuration, color constants, chart types, and data generation techniques.

Put all chart components in `Charts.jsx`. Key patterns:

- Use `ResponsiveContainer` with explicit height
- Wrap in `.chart-wrap` div with max-width 920px
- Use `useMemo` for data generation
- **Color rule**: Use the Tableau-inspired categorical palette (`CAT[]`) for distinguishing data series and groups. Only use semantic colors (`SEM_GREEN`, `SEM_RED`, `SEM_AMBER`) when the color itself carries meaning (good/bad, success/failure, warning).
- Common charts: `ComposedChart` with stacked `Area`/`Line`, `BarChart`, custom SVG diagrams
- **Every data point in a chart must come from the source content.** Do not interpolate, extrapolate, or round numbers to make charts look better.

## Step 5: Style with Sentry Design System

Apply the complete CSS from the design system reference. Key elements:

- **Font**: Rubik from Google Fonts
- **Colors**: CSS variables for UI chrome (`--purple`, `--dark`, `--muted`). Semantic CSS variables (`--semantic-green`, `--semantic-red`, `--semantic-amber`) only where color conveys meaning. Categorical palette (`CAT[]`) for all other data visualization.
- **Slides**: Absolute positioned, opacity transitions
- **Animations**: `fadeUp` keyframe with staggered delays
- **Layout**: `.cols` flex rows, `.cards` grid, `.chart-wrap` containers
- **Tags**: `.tag-purple`, `.tag-red`, `.tag-green`, `.tag-amber` for slide labels
- **Logo**: Read the official SVG from `${CLAUDE_SKILL_ROOT}/references/sentry-logo.svg` (full wordmark) or `sentry-glyph.svg` (glyph only). Do NOT hardcode an approximation — always use the exact SVG paths from these files.

## Step 6: Common Slide Patterns

### Title Slide
Logo (from `${CLAUDE_SKILL_ROOT}/references/sentry-logo.svg` or `sentry-glyph.svg`) + h1 + subtitle + author/date info.

### Problem/Context Slide
Tag + heading + 2-column card grid with icon headers.

### Data Comparison Slide
Tag + heading + side-by-side charts or before/after comparison table.

### Technical Deep-Dive Slide
Tag + heading + full-width chart + annotation bullets below.

### Summary/Decision Slide
Tag + heading + 3-column layout with category headers and bullet lists.

## Step 7: Iterate and Refine

After initial scaffolding:
1. Run `npm install && npm run dev` to start the dev server
2. Iterate on chart data models and visual design
3. Adjust animations, colors, and layout spacing
4. Build final output: `npm run build` produces a single HTML file in `dist/`

## Output Expectations

A working React + Vite project that:
- Renders as a keyboard-navigable slide deck
- Uses Sentry branding (colors, fonts, icons)
- Contains Recharts visualizations **only for slides with real quantitative data** from the source content — no fabricated data
- Omits `Charts.jsx` and the Recharts dependency entirely if no slides have real data
- Builds to a single distributable HTML file
- Has smooth fade-in animations on slide transitions

If speaker notes are enabled, also:
- Stores notes in `src/notes.json` fetched dynamically via `/__get-notes` (never via static import)
- Has a speaker notes window (press N) with live slide preview, editable textarea, and auto-save to disk
- Isolates the embed iframe (`?embed=1`) to prevent feedback loops
