---
name: ml-venv-package-conflicts
description: "Use when an ML venv import error names a missing symbol."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [python, venv, pip, triton, pytorch, wheels, debugging, ml-environments]
---

# ML Venv Package Conflicts

## When to Use

- An ML/Python venv import error names a specific missing symbol from a compiled module (`.pyd`/`.so`), e.g. `cannot import name 'intel' from 'triton._C.libtriton'`.
- An ML desktop app (Unsloth Studio, ComfyUI, text-gen-webui, etc.) fails with deep-library import errors, especially right after an update.
- `pip install` of a package you know was previously installed reports "No matching distribution found".

Details: a Python environment throws an import error naming a symbol which "shouldn't" be missing, where the failing module belongs to a compiled `.pyd`/`.so` that multiple distributions could have written.

## Core insight

Several ML distributions ship the **same top-level package** and silently overwrite each other's compiled binaries on install:

| Package | Owns | For hardware |
|---|---|---|
| `triton` | `triton/` | NVIDIA (Linux) |
| `triton-windows` | `triton/` | NVIDIA (Windows) |
| `triton-xpu` (a.k.a. `pytorch-triton-xpu` before torch 2.10) | `triton/` | Intel GPUs |

Whichever installed **last** wins the binary. A mixed state produces errors where code asks for symbols from build A but the binary on disk is build B. The same pattern exists for other stacks (onnxruntime vs onnxruntime-gpu, torch cu/xpu/cpu builds, bitsandbytes multi-backend forks).

## Diagnostic workflow

1. **Read the error literally.** A symbol like `intel` inside `triton._C.libtriton` means the *Intel* backend is expected — so torch is almost certainly an `+xpu` build. Check: `grep ^Version <env>/Lib/site-packages/torch-*.dist-info/METADATA`.
2. **List every dist-info touching the module**: `ls <env>/Lib/site-packages/ | grep -i triton`. Two+ matches = conflict confirmed.
3. **Check which binary won**: compare timestamps of `<module>/_C/*.pyd|.so` against each dist-info's install date. Mismatched dates = clobbered files.
4. **Check the backends folder** (`<module>/backends/`): leftover subfolders from both builds (e.g. both `nvidia/` and `intel/`) confirm the mixed state.
5. **Find the correct wheel source BEFORE uninstalling.** Vendor wheels often are NOT on PyPI:
   - Read the app's own installer script/logs first (`setup.ps1`, `install.log`, install manifest JSON) — they contain the exact spec and `--index-url`.
   - Common indexes: `https://download.pytorch.org/whl/xpu`, `/whl/cu121`…, Intel extension index, GitHub releases.
   - Verify the exact wheel filename exists (match python tag e.g. `cp313`, OS tag, version) with `curl <index>/<package>/`.
6. **Repair**: `pip uninstall -y <all conflicting variants>` then `pip install --force-reinstall --no-deps <pkg>==<ver> --index-url <vendor-index>`.
   - `--no-deps` is critical: letting pip resolve deps can reinstall the wrong torch/triton variant and re-clobber.
7. **Verify by importing the exact missing symbol**, not just the package: `python -c "from triton._C.libtriton import intel; print('ok')"`.
8. **Expect follow-on errors.** On Windows Intel XPU, the triton fix often unearths 2–3 more errors in sequence (missing CC → missing CXX → GPU DEVICE_LOST). Don't declare victory after step 7 — run a real workload or at least check for compiler and driver errors before closing.

## Pitfalls

- **Default-PyPI failure is a clue, not a dead end.** `No matching distribution found` for a package you KNOW was installed means it came from a vendor index. Don't give up — find the index (step 5).
- **App updaters can re-break the env.** If the host app's updater reinstalls the conflicting package on each update, expect recurrence; keep the repair commands handy and tell the user to re-run them after updates.
- **Don't trust the app's own log hints blindly.** Unsloth Studio logs suggested `pip install "triton-windows<3.7"` — correct only for NVIDIA machines. Match the fix to the *torch build* (+xpu → triton-xpu), not the log message.
- **Windows long paths**: Triton/inductor filenames exceed MAX_PATH; enable Windows long paths if installs fail oddly.
- **Never hand-edit site-packages binaries**; always let pip place files so RECORD/metadata stay consistent.
- **Follow-on errors are a chain, not isolated.** On Windows Intel XPU, fixing the triton import often unearths 2–3 more errors in sequence: missing CC → missing CXX → GPU timeout (DEVICE_LOST). Don't stop after the first fix — walk the user through the full chain. See `references/unsloth-studio-triton-xpu-case.md` for the complete sequence.
- **MSVC compiler discovery on Windows.** Triton JIT needs `CC` and `CXX` env vars pointing to `cl.exe`. Unlike Linux where `gcc` is on PATH, Windows MSVC requires explicit env vars or running from a Developer Command Prompt.
- **Intel GPU watchdog timeout.** The level_zero runtime kills long-running kernels with `UR_RESULT_ERROR_DEVICE_LOST` (error 20). Set `SYCL_PI_LEVEL_ZERO_DEVICE_TIMEOUT=disable` as a permanent user env var.

## Reference

- `references/unsloth-studio-triton-xpu-case.md` — full walkthrough of the Unsloth Studio Windows Intel-XPU case, including log forensics and exact working commands.
