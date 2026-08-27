# GIMP Local Privacy Contract

Allowed:

- A new local GIMP batch process for each job.
- Script-Fu Eval batch interpreter.
- Local `.scm` files and image outputs.
- GIMP Procedure Browser / local PDB documentation.

Forbidden in this profile:

- Script-Fu Server.
- MCP.
- Any network listener or remote client.
- Persistent daemon used to control GIMP.
- Cloud upload from bundled scripts.

The lifecycle should be finite:

`write job -> launch GIMP batch -> execute -> save/export -> process exits`.
