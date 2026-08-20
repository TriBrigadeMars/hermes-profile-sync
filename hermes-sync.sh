#!/usr/bin/env bash
# hermes-sync.sh — Export all Hermes profiles, push to git, pull & import from other machines
# Run via: bash hermes-sync.sh
# Or set up as a scheduled task via hermes-sync.bat.

set -euo pipefail

# ── Resolve Windows-native paths (hermes.exe needs C:\ style paths) ──
SYNC_DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v cygpath &>/dev/null; then
    SYNC_DIR_WIN="$(cygpath -w "$SYNC_DIR")"
else
    SYNC_DIR_WIN="$SYNC_DIR"
fi

HERMES_HOME="${HERMES_HOME:-$LOCALAPPDATA/hermes}"
PROFILES_DIR="$HERMES_HOME/profiles"

echo "=== Hermes Profile Sync ==="
echo "Sync dir:  $SYNC_DIR"
echo "Hermes:    $HERMES_HOME"
echo ""

# ── Step 1: Export all NAMED profiles (skip default — it's built-in) ──
echo "[1/4] Exporting profiles..."
cd "$SYNC_DIR"
mkdir -p profiles

exported=0
if [ -d "$PROFILES_DIR" ]; then
    for profile_dir in "$PROFILES_DIR"/*/; do
        [ -d "$profile_dir" ] || continue
        name="$(basename "$profile_dir")"
        echo "  Exporting: $name"
        out="$SYNC_DIR_WIN\\profiles\\${name}.tar.gz"
        hermes profile export "$name" -o "$out" 2>/dev/null && exported=$((exported+1)) || echo "  ($name export failed, skipping)"
    done
fi

if [ "$exported" -eq 0 ]; then
    echo "  No named profiles found. Create one with: hermes profile create <name>"
fi
echo ""

# ── Step 2: Commit and push ──────────────────────────────────────────
echo "[2/4] Committing & pushing..."
cd "$SYNC_DIR"
git add -A
if git diff --cached --quiet; then
    echo "  No changes to push."
else
    machine="$(hostname)"
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "Sync from $machine — $timestamp"
    git push origin main 2>&1 || echo "  Push failed (will retry on next run)"
fi
echo ""

# ── Step 3: Pull from other machines ─────────────────────────────────
echo "[3/4] Pulling from remote..."
cd "$SYNC_DIR"
git pull origin main --rebase 2>&1 || echo "  Pull failed (resolve manually)"
echo ""

# ── Step 4: Import any profiles we don't have locally ────────────────
echo "[4/4] Importing new profiles..."
cd "$SYNC_DIR"
imported=0
for archive in "$SYNC_DIR/profiles/"*.tar.gz; do
    [ -f "$archive" ] || continue
    name="$(basename "$archive" .tar.gz)"

    if command -v cygpath &>/dev/null; then
        archive_win="$(cygpath -w "$archive")"
    else
        archive_win="$archive"
    fi

    if [ -d "$PROFILES_DIR/$name" ]; then
        echo "  Already exists: $name (skipping)"
    else
        echo "  Importing: $name"
        hermes profile import "$archive_win" 2>/dev/null && imported=$((imported+1)) || echo "  ($name import failed)"
    fi
done

echo ""
echo "=== Done! Exported $exported profile(s), imported $imported new profile(s). ==="
