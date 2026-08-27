# Krita Local Privacy Contract

The skill must not create any network control surface.

Allowed:

- Krita command-line export.
- Local files.
- A manually-triggered Krita Python plugin.
- JSON job files.
- Local preview/export files.

Forbidden by default:

- MCP.
- HTTP, WebSocket, TCP, UDP, or named network listener.
- Background directory watcher.
- Automatic execution merely because a file appeared.
- Cloud upload from the bundled plugin.
- Telemetry added by this skill.

The bundled plugin only reads a job path chosen by the user at invocation time and writes a result file next to it.
