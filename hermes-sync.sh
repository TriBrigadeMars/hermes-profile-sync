#!/usr/bin/env bash
# hermes-sync.sh — Export all Hermes profiles, push to git, pull & import from other machines
# Also syncs scripts and cron jobs from the repo.
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
SCRIPTS_DIR="$HERMES_HOME/scripts"
PETS_DIR="$HERMES_HOME/pets"

echo "=== Hermes Profile Sync ==="
echo "Sync dir:  $SYNC_DIR"
echo "Hermes:    $HERMES_HOME"
echo ""

# ── Step 1: Export all NAMED profiles (skip default — it's built-in) ──
echo "[1/5] Exporting profiles..."
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

# ── Step 2: Sync pets (petdex mascots — incl. hatched/generated pets) ──
echo "[2/5] Syncing pets..."
mkdir -p "$SYNC_DIR/pets"
synced_pets=0

# Export every installed pet's folder (pet.json + spritesheet.webp) to the repo
if [ -d "$PETS_DIR" ]; then
    for pet_dir in "$PETS_DIR"/*/; do
        [ -d "$pet_dir" ] || continue
        slug="$(basename "$pet_dir")"
        [ "$slug" = ".thumbs" ] && continue
        if [ -f "$pet_dir/pet.json" ] && [ -f "$pet_dir/spritesheet.webp" ]; then
            out="$SYNC_DIR/pets/$slug"
            mkdir -p "$out"
            cp "$pet_dir/pet.json" "$out/pet.json"
            cp "$pet_dir/spritesheet.webp" "$out/spritesheet.webp"
            synced_pets=$((synced_pets+1))
        fi
    done
fi
echo "  Exported $synced_pets pet(s) to repo"
echo ""

# ── Step 2b: Sync custom skills from repo → local install ───────────────
echo "[2b/6] Syncing skills from repo..."
SKILLS_DIR="$HERMES_HOME/skills"
synced_skills=0
if [ -d "$SYNC_DIR/skills" ]; then
    # Install categorized skills (skills/<category>/<skill-name>/)
    for category_dir in "$SYNC_DIR/skills"/*/; do
        [ -d "$category_dir" ] || continue
        category="$(basename "$category_dir")"
        [ "$category" = "_standalone" ] && continue
        for skill_dir in "$category_dir"*/; do
            [ -d "$skill_dir" ] || continue
            skill_name="$(basename "$skill_dir")"
            dst="$SKILLS_DIR/$category/$skill_name"
            mkdir -p "$(dirname "$dst")"
            cp -r "$skill_dir" "$dst"
            synced_skills=$((synced_skills+1))
        done
    done
    # Install standalone skills (skills/_standalone/<skill-name>/)
    if [ -d "$SYNC_DIR/skills/_standalone" ]; then
        for skill_dir in "$SYNC_DIR/skills/_standalone"/*/; do
            [ -d "$skill_dir" ] || continue
            skill_name="$(basename "$skill_dir")"
            dst="$SKILLS_DIR/$skill_name"
            mkdir -p "$dst"
            cp -r "$skill_dir" "$dst"
            synced_skills=$((synced_skills+1))
        done
    fi
fi
echo "  Installed/updated $synced_skills skill(s) from repo"
echo ""

# ── Step 3: Commit and push ──────────────────────────────────────────
echo "[3/6] Committing & pushing..."
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

# ── Step 4: Pull from other machines ─────────────────────────────────
echo "[4/6] Pulling from remote..."
cd "$SYNC_DIR"
git pull origin main --rebase 2>&1 || echo "  Pull failed (resolve manually)"
echo ""

# ── Step 5: Import any profiles we don't have locally ────────────────
echo "[5/6] Importing new profiles..."
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

# Also import repo pets that aren't installed locally (after the pull above)
imported_pets=0
for pet_dir in "$SYNC_DIR/pets"/*/; do
    [ -d "$pet_dir" ] || continue
    slug="$(basename "$pet_dir")"
    if [ -d "$PETS_DIR/$slug" ]; then
        echo "  Pet already installed: $slug (skipping)"
    elif [ -f "$pet_dir/pet.json" ] && [ -f "$pet_dir/spritesheet.webp" ]; then
        mkdir -p "$PETS_DIR/$slug"
        cp "$pet_dir/pet.json" "$PETS_DIR/$slug/pet.json"
        cp "$pet_dir/spritesheet.webp" "$PETS_DIR/$slug/spritesheet.webp"
        imported_pets=$((imported_pets+1))
        echo "  Installed pet: $slug"
    fi
done
if [ "$imported_pets" -gt 0 ]; then
    echo ""
fi

# ── Step 6: Sync scripts and cron jobs ───────────────────────────────
echo "[6/6] Syncing scripts and cron jobs..."
mkdir -p "$SCRIPTS_DIR"

# Copy digest scripts from repo to Hermes scripts dir
for script in academic_digest.py mail.py setup_digest.py cron_config.json; do
    src="$SYNC_DIR/scripts/$script"
    dst="$SCRIPTS_DIR/$script"
    if [ -f "$src" ]; then
        cp "$src" "$dst"
        echo "  Synced: $script"
    fi
done

# Install Python dependencies for digest scripts
echo "  Installing Python deps (feedparser)..."
python -m pip install feedparser -q 2>/dev/null || echo "  (pip install failed, run manually: pip install feedparser)"

# Check if the academic digest cron job already exists; create if not
if command -v hermes &>/dev/null; then
    # Check existing cron jobs
    existing=$(hermes cron list 2>/dev/null || echo "")
    if echo "$existing" | grep -q "Academic-Journal-Digest" 2>/dev/null; then
        echo "  Cron job 'Academic-Journal-Digest' already exists (skipping)"
    else
        echo "  Creating academic digest cron job..."
        hermes cron create \
            --name "Academic-Journal-Digest-Biweekly" \
            --schedule "0 9 */14 * *" \
            --prompt "Run python $SCRIPTS_DIR/academic_digest.py to send the biweekly academic journal digest email to nalcs.mika@gmail.com" \
            2>/dev/null || echo "  (cron create failed — set up manually in Hermes)"
    fi
fi

echo ""
echo "=== Done! Exported $exported profile(s), imported $imported new profile(s), synced $synced_pets pet(s) + $synced_skills skill(s) + scripts + cron. ==="
