# Resolve Free Interchange Notes

## Preferred v1 formats

### CMX3600 EDL

Use for simple cuts and a conservative rough-cut handoff. Keep a separate media manifest because EDL reel names are compact and may not preserve complete filenames.

The bundled helper expects a nominal integer timebase and non-drop timecode. Use the source project's actual timecode convention; do not silently convert drop-frame material to non-drop.

### SRT

Use for subtitle/caption handoff when the user has timestamped text. Keep each cue concise and preserve the original transcript separately.

## Edit-plan schema

See `templates/edit-plan.example.json`.

Required top-level fields:

- `title`
- `fps` — nominal integer timebase, e.g. 24, 25, 30
- `events` — ordered array

Each event requires:

- `reel`
- `track` — normally `V`
- `transition` — v1 supports `C`
- `source_in`
- `source_out`
- `record_in`
- `record_out`

Timecode format is `HH:MM:SS:FF`.

## Safe workflow

1. Preserve source media.
2. Build a manifest.
3. Generate an edit plan.
4. Validate durations.
5. Generate EDL/SRT.
6. Import manually in Resolve Free.
7. Re-link media if needed using the manifest.
8. Export a short test render before a long delivery.
9. Verify the render with `ffprobe` when available.
