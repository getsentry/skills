#!/bin/bash
# List all git repositories from configured repo directories
config="$HOME/.claude/repos.local.json"
if [ -f "$config" ]; then
    jq -r '.repoDirs[]' "$config" 2>/dev/null | while read -r dir; do
        [ -d "$dir" ] && ls -1 "$dir" 2>/dev/null | while read -r repo; do
            [ -d "$dir/$repo/.git" ] && echo "- $repo"
        done
    done | sort -u | head -30
else
    echo "(No repos.local.json config found)"
fi
