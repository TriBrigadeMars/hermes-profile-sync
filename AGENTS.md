# AGENTS.md — Instructions for AI agents working in this repository

This repo is maintained by both humans and LLM agents across multiple machines
(Windows desktops, macOS/Linux laptops). Before making any claim about this
repository or the local Hermes installation, read this file.

## 1. Never hardcode the Hermes home path

The Hermes home directory is **platform-dependent**. Resolve it — do not assume:

| Platform | Default location |
|---|---|
| Windows | `$LOCALAPPDATA/hermes` (e.g. `C:\Users\<user>\AppData\Local\hermes`) |
| macOS / Linux | `~/.hermes` |
| Any | `$HERMES_HOME` if the env var is set (this is what `hermes-sync.sh` uses) |

Bash resolution (same as `hermes-sync.sh`):

```bash
HERMES_HOME="${HERMES_HOME:-${LOCALAPPDATA:-$HOME/.hermes}/hermes}"
# Windows Git Bash: LOCALAPPDATA is set, so this yields .../AppData/Local/hermes
```

**Historical failure (2026-08-27):** an agent checked only `~/.hermes/skills`
on a Windows machine, found nothing, and wrote "not installed on this machine
either" into `custom-skills-inventory.md` — while 141 skills actually existed
at `$LOCALAPPDATA/hermes/skills`. Do not repeat this.

## 2. Evidence rules for absence claims

Before writing that any skill/file/profile "does not exist" or "was lost":

1. Check **both** candidate Hermes homes (Windows and Unix paths) on the machine you're on.
2. Check inside the profile tarballs in `profiles/*.tar.gz` (`tar -tzf` — don't trust filenames).
3. Run `python3 scripts/verify_inventory.py --local` and report its output.
4. Cite the exact commands you ran and their results.

If you cannot check a location (no access, no permission), say so explicitly
instead of concluding absence. Write "**unverified**" rather than "**missing**".

## 3. `custom-skills-inventory.md` is derived state

- The skill tables in the inventory **must match** `skills/**/SKILL.md` folders.
  CI enforces this via `scripts/verify_inventory.py` — a mismatch fails the build.
- If you add, remove, or rename a skill, run
  `python3 scripts/verify_inventory.py` **before committing** and fix the
  inventory in the same commit.
- Never delete or "prune" inventory entries because you can't find their code.
  Run the verification script and the checks in §2 first, and discuss in the
  commit message / PR description if entries appear stale.

## 4. Repo layout

- `skills/<category>/<skill-name>/` — skill code, mirroring the source
  installation's category layout. Each folder must contain a `SKILL.md` whose
  front-matter `name:` matches the folder name.
- `skills/_standalone/<skill-name>/` — skills that live top-level in the
  source installation (no category).
- `profiles/*.tar.gz` — exported Hermes profile archives (binary; inspect with
  `tar -tzf`, never assume contents from filenames).
- `custom-skills-inventory.md` — human-readable inventory (derived state, see §3).
- `scripts/` — sync and verification tooling.

## 5. General safety rules

- Skills may contain executable scripts. **Read every `SKILL.md` and script you
  introduce or modify.** Do not commit code with destructive commands,
  credential access, obfuscation, or unexpected network calls. If you find
  such content, flag it in the PR instead of pushing.
- `git push` is allowed to `main` (single-maintainer repo), but every push must
  leave the repo in a state where `scripts/verify_inventory.py` passes.
- Do not rewrite git history or force-push.
- Do not commit anything from `~/.hermes`/`$LOCALAPPDATA/hermes` outside the
  intended exports (profiles, pets, skills, scripts) — that tree contains
  credentials (`auth.json`, `.env` files) and session data that must never
  reach this repo.
