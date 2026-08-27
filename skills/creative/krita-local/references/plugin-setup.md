# Krita Plugin Setup

Krita Python plugins consist of a `.desktop` file plus a same-named Python package inside the `pykrita` resource directory.

## Install helper

Run:

```bash
python "${HERMES_SKILL_DIR}/scripts/install_plugin.py"
```

Use `--target PATH` if the detected resource directory is not the one your Krita installation uses.

Then restart Krita, enable **Hermes Local Jobs** in Krita's Python Plugin Manager, and restart if prompted.

The action appears under **Tools > Scripts > Hermes Local: Run Job**.

## Job execution

1. Hermes writes a JSON job.
2. The user invokes the menu action.
3. A file chooser asks for that JSON job.
4. The plugin runs only allowlisted operations against the active document.
5. It writes `<jobname>.result.json` next to the job.

There is no watcher and no listener.
