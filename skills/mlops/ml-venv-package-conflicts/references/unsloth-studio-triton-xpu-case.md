# Case Study: Unsloth Studio on Windows — `cannot import name 'intel' from 'triton._C.libtriton'`

Session date: 2026-08-21. User: Mars, Windows 11, Unsloth Studio installed at
`C:\Users\cruzmars\.unsloth\studio\unsloth_studio` (Python 3.13 venv).

## Error

```
Failed to import ML libraries: cannot import name 'intel' from 'triton._C.libtriton'
(C:\Users\cruzmars\.unsloth\studio\unsloth_studio\Lib\site-packages\triton\_C\libtriton.pyd)
```

## Environment findings

- torch **2.10.0+xpu** → Intel GPU build; expects Intel triton symbols.
- TWO triton dist-infos present: `triton_windows-3.7.1.post27` (NVIDIA) and `triton_xpu-3.6.0` (Intel).
- Both ship the same file `triton/_C/libtriton.pyd`; last install wins.
- Forensic detail: `.pdb`/`.ilk` debug files dated Aug 20 (NVIDIA install), but `libtriton.pyd` dated Aug 11 — mismatched set.
- `triton/backends/` contained BOTH `nvidia/` and `intel/` subfolders.

## Where triton-xpu actually comes from

NOT PyPI. PyPI's `triton-xpu` tops out at 3.3.0b1 and is Linux-only. The Windows wheel lives on
**PyTorch's XPU index**: `https://download.pytorch.org/whl/xpu`

Verified available: `triton_xpu-3.6.0-cp313-cp313-win_amd64.whl` (and 3.7.2 variants).

## Log forensics that cracked it

Unsloth Studio's own update logs (`~/.unsloth/studio/logs/update-*.log`) showed its updater had been
trying and failing to do this same swap on every update:

```
replacing triton-windows 3.7.1.post27 with triton-xpu==3.6.0 (Intel XPU)...
[WARN] could not fetch triton-xpu==3.6.0 (exit 1)
ERROR: Directory '...\Temp\unsloth_triton_xpu_<hash>' is not installable.
       Neither 'setup.py' nor 'pyproject.toml' found.
```

The installer script (`Lib/site-packages/studio/setup.ps1`) revealed the mechanism:
it downloads via `--index-url $XpuIndexUrl` where `$XpuIndexUrl = https://download.pytorch.org/whl/xpu`.
The user's manual `pip install triton-xpu==3.6.0` failed because pip defaulted to PyPI.

Note: the Studio backend log also emitted a misleading hint —
`pip install "triton-windows<3.7"` — which is correct ONLY for NVIDIA machines.

## Working repair commands (PowerShell)

```powershell
cd C:\Users\cruzmars\.unsloth\studio\unsloth_studio

# Remove both conflicting packages
.\Scripts\python.exe -m pip uninstall -y triton-windows triton-xpu triton

# Reinstall Intel build from the vendor index (--no-deps prevents re-clobbering torch)
.\Scripts\python.exe -m pip install --force-reinstall --no-deps triton-xpu==3.6.0 --index-url https://download.pytorch.org/whl/xpu

# Verify package imports
.\Scripts\python.exe -c "import triton; print(triton.__version__)"

# Verify the exact missing symbol
.\Scripts\python.exe -c "from triton._C.libtriton import intel; print('intel backend OK')"
```

## Follow-on errors after triton fix (same session)

The triton import fix landed successfully, but two more errors appeared in sequence:

### Error 2: `RuntimeError: Failed to find C compiler. Please specify via CC environment variable`

Triton JIT-compiles GPU kernels and needs a C compiler. On Windows with MSVC Build Tools installed
(VS 18 Build Tools, MSVC 14.51), `cl.exe` exists but isn't on PATH and triton doesn't find it
automatically (unlike Linux where `gcc` is typically available).

Fix — set `CC` permanently for the user:

```powershell
[System.Environment]::SetEnvironmentVariable("CC",
    "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe",
    "User")
```

Verify: `[System.Environment]::GetEnvironmentVariable("CC", "User")` should print the path.
Restart Unsloth Studio after setting.

### Error 3: `RuntimeError: Failed to find C++ compiler. Please specify via CXX environment variable`

Same pattern — triton distinguishes C and C++ compilers. On MSVC, `cl.exe` handles both, but
triton checks `CXX` separately.

Fix — set `CXX` to the same `cl.exe`:

```powershell
[System.Environment]::SetEnvironmentVariable("CXX",
    "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe",
    "User")
```

### Error 4: `level_zero backend failed with error: 20 (UR_RESULT_ERROR_DEVICE_LOST)`

Intel GPU driver timeout — the level_zero runtime killed a long-running kernel. This is the
Intel equivalent of NVIDIA's TDR. Common with older drivers or large workloads.

Fix — disable the GPU watchdog timeout:

```powershell
[System.Environment]::SetEnvironmentVariable("SYCL_PI_LEVEL_ZERO_DEVICE_TIMEOUT", "disable", "User")
```

Also recommended: update Intel GPU drivers from https://www.intel.com/content/www/us/en/support/detect.html
and reduce batch size / sequence length if the GPU runs out of memory.

## Full repair sequence (all four errors, in order)

```powershell
cd C:\Users\cruzmars\.unsloth\studio\unsloth_studio

# 1. Fix triton conflict
.\Scripts\python.exe -m pip uninstall -y triton-windows triton-xpu triton
.\Scripts\python.exe -m pip install --force-reinstall --no-deps triton-xpu==3.6.0 --index-url https://download.pytorch.org/whl/xpu

# 2. Set compiler env vars (permanent, user-level)
[System.Environment]::SetEnvironmentVariable("CC",
    "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe", "User")
[System.Environment]::SetEnvironmentVariable("CXX",
    "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64\cl.exe", "User")

# 3. Disable Intel GPU watchdog timeout (permanent, user-level)
[System.Environment]::SetEnvironmentVariable("SYCL_PI_LEVEL_ZERO_DEVICE_TIMEOUT", "disable", "User")

# 4. Verify everything
.\Scripts\python.exe -c "import triton; print('triton', triton.__version__)"
.\Scripts\python.exe -c "from triton._C.libtriton import intel; print('intel backend OK')"

# 5. Restart Unsloth Studio, then retry training
```

## Outcome

All four errors resolved in sequence. The triton import, compiler discovery, and GPU timeout
issues are a common chain on Windows Intel XPU environments — fixing only the first one
and stopping will leave the user with the next error in the chain.

## Recurrence

If Unsloth Studio updates reinstall `triton-windows`, expect Error 1 to recur — re-run the
pip uninstall/install commands. The CC/CXX/SYCL env vars persist across updates.
