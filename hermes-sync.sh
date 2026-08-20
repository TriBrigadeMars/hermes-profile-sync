#!/usr/bin/env bash
# hermes-sync.sh — Export all Hermes profiles, push to git, pull & import from other machines
# Run via: bash hermes-sync.sh
# Or set up as a scheduled task / cron job.

set -euo pipefail

SYNC_DIR="$(cd "$(dirname "$0")" && pwd)"
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

# Export the default profile (no profile dir, lives in hermes home root)
if [ -f "$HERMES_HOME/config.yaml" ]; then
    echo "  Exporting: default"
    hermes profile export default -o "$SYNC_DIR/profiles/default.tar.gz" 2>/dev/null || echo "  (default export skipped)"
fi

# Export named profiles
if [ -d "$PROFILES_DIR" ]; then
    for profile_dir in "$PROFILES_DIR"/*/; do
        [ -d "$profile_dir" ] || continue
        name="$(basename "$profile_dir")"
        echo "  Exporting: $name"
        hermes profile export "$name" -o "$SYNC_DIR/profiles/${name}.tar.gz" 2>/dev/null || echo "  ($name export failed, skipping)"
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
    hostname="$(hostname)"
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "Sync from $hostname — $timestamp"
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

    # Check if this profile already exists locally
    if [ "$name" = "default" ]; then
        # Default always exists, re-import to update
        echo "  Updating: default"
        hermes profile import "$archive" --name default 2>/dev/null && imported=$((imported+1)) || echo "  (default import skipped)"
    elif [ -d "$PROFILES_DIR/$name" ]; then
        echo "  Already exists: $name (skipping)"
    else
        echo "  Importing: $name"
        hermes profile import "$archive" 2>/dev/null && imported=$((imported+1)) || echo "  ($name import failed)"
    fi
done

echo ""
echo "=== Done! Imported $imported new profile(s). ==="
