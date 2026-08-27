# Script-Fu v3 Rules for GIMP 3

- Write new jobs for GIMP 3, not GIMP 2.x.
- Call `(script-fu-use-v3)` inside the job before relying on v3 return-value conventions.
- Verify every PDB procedure in GIMP 3's Procedure Browser or current developer documentation.
- Internal PDB procedures use their generated Script-Fu function and full required argument list.
- Plug-in PDB procedures can support `#:argument-name` keyword syntax; prefer it when documented.
- Do not assume an old GIMP 2.x procedure name or signature still works.

## Batch invocation

The official Script-Fu batch pattern is conceptually:

```text
gimp-console --batch-interpreter=plug-in-script-fu-eval --batch="(load \"job.scm\")"
```

The bundled Python launcher constructs this argument vector without using a shell, reducing quoting and injection problems.

## Discovery

When a new task needs an unfamiliar procedure:

1. Search the GIMP 3 Procedure Browser by operation name.
2. Record exact procedure name and signature in the job comments.
3. Prefer a small smoke job before processing important source files.
4. Use new output files.
