#!/usr/bin/env bash
# hermes-sync.sh — Export all Hermes profiles, push to git, pull & import from other machines
# Run via: bash hermes-sync.sh
# Or set up as a scheduled task via hermes-sync.bat.

set -euo pipefail

# ── Resolve Windows-native paths (hermes.exe needs C:\ style paths) ──
SYNC_DIR="$(cd "$(dirname "$0")" && pwd)"
# Convert MSYS path to Windows path for hermes
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

# ── Step 1: Export all profiles ──────────────────────────────────────
echo "[1/4] Exporting profiles..."
cd "$SYNC_DIR"
mkdir -p profiles

# Export the default profile
if [ -f "$HERMES_HOME/config.yaml" ]; then
    echo "  Exporting: default"
    out="$SYNC_DIR_WIN\\profiles\\default.tar.gz"
    hermes profile export default -o "$out" 2>/dev/null || echo "  (default export skipped)"
fi

# Export named profiles
if [ -d "$PROFILES_DIR" ]; then
    for profile_dir in "$PROFILES_DIR"/*/; do
        [ -d "$profile_dir" ] || continue
        name="$(basename "$profile_dir")"
        echo "  Exporting: $name"
        out="$SYNC_DIR_WIN\\profiles\\${name}.tar.gz"
        hermes profile export "$name" -o "$out" 2>/dev/null || echo "  ($name export failed, skipping)"
    done
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

    # Convert to Windows path for hermes
    if command -v cygpath &>/dev/null; then
        archive_win="$(cygpath -w "$archive")"
    else
        archive_win="$archive"
    fi

    if [ "$name" = "default" ]; then
        echo "  Updating: default"
        hermes profile import "$archive_win" --name default 2>/dev/null && imported=$((imported+1)) || echo "  (default import skipped)"
    elif [ -d "$PROFILES_DIR/$name" ]; then
        echo "  Already exists: $name (skipping)"
    else
        echo "  Importing: $name"
        hermes profile import "$archive_win" 2>/dev/null && imported=$((imported+1)) || echo "  ($name import failed)"
    fi
done

echo ""
echo "=== Done! Imported $imported new profile(s). ==="
