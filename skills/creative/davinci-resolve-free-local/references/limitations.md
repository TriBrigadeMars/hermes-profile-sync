# Resolve Free Local-Only Boundary

## Hard boundary

DaVinci Resolve Studio exposes the external scripting preference used by outside Python/Lua processes. Resolve Free does not expose that Studio control surface. Therefore this skill does not depend on external `DaVinciResolveScript` control.

## Allowed in this skill

- Read local media metadata with `ffprobe`.
- Generate CMX3600 EDL files.
- Generate SRT subtitle files.
- Generate cut lists, shot lists, transcript decisions, filenames, and delivery checklists.
- Validate renders that the user exports from Resolve.
- Draft a script the user can deliberately run inside Resolve if requested, while clearly labeling it as user-invoked and unverified until run.

## Not allowed as a default mechanism

- MCP.
- HTTP/WebSocket/TCP listener.
- Authenticated or unauthenticated localhost bridge.
- Hidden background daemon that proxies Resolve.
- Claiming an outside Python process can directly drive Resolve Free.
- UI automation that blindly clicks destructive commands.

## State language

Use these words precisely:

- **Prepared**: Hermes generated files or instructions locally.
- **Imported**: the user confirmed the file was imported into Resolve.
- **Applied**: the user confirmed the edit/change exists in the project.
- **Verified**: Hermes inspected a resulting file or the user supplied direct evidence.
