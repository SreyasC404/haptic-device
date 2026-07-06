# Haptic Device Launcher

A cross-platform (Mac/Windows) desktop GUI for configuring and launching the
`haptic-device` CHAI3D simulation, and for tweaking a few parameters while it
runs.

## Setup

```
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Run

From the `haptic-device` directory:

```
python -m launcher.main
```

## What it does

1. Builds the `haptic-device` binary's command-line arguments from the form
   (haptic mode, atom count or structure/config file, potential energy
   surface, ASE calculator spec, PBC mode) and launches it as a subprocess,
   streaming its stdout/stderr into the log view.
   - **Structure/config file** accepts anything `loadAseStructure` understands
     (`.con`, `.xyz`, `.cif`, `POSCAR`/`CONTCAR`, etc.) regardless of which
     potential you picked — the file only supplies starting positions/cell.
   - **ASE calculator spec** is an editable dropdown with common presets
     (`lj`, `morse`, `emt`, `uma`, `uma:omol`, `uma:omat`, `uma:oc20`); you can
     also type a custom `module:Class[:kwargs]` spec. Only used when the
     potential is `ase`.
   - **Periodic boundaries** is a 3-way choice: keep whatever the structure
     file specified, force PBC on, or force it off.
   - **Initial time step** sets the simulation time step (seconds) via the
     `HAPTIC_DEVICE_TIME_STEP` environment variable (valid range
     `0.0001`-`0.005`, default `0.001`).
2. Connects over a loopback TCP socket (`127.0.0.1:<port>`, default `8765`,
   configurable in the UI and passed to the simulation via the
   `HAPTIC_DEVICE_CMD_PORT` environment variable) to the IPC command server
   started inside `LJ.cpp` (`ipcServer.h`/`ipcServer.cpp`). Once connected,
   the "Live controls" panel lets you:
   - freeze/unfreeze the simulation
   - switch haptic mode (force/position/standby)
   - switch potential between `lj` and `morse` (ASE calculators need
     constructor arguments only available at launch, so they can't be
     hot-swapped — relaunch to change to/from ASE)
   - drag the time step slider (release to apply; range matches the launch
     spin box) to speed up/slow down the simulation while it runs
   - anchor/unanchor all atoms, advance to the next atom, cycle the camera
   - poll live status (mode, freeze state, potential, atom/anchor counts,
     potential energy, time step) twice a second

## Binary discovery

The binary path field is pre-filled by guessing
`<chai3d-root>/bin/<platform>/haptic-device[.exe]` (e.g. `mac-arm64`,
`win-x64`). Use "Browse..." if your build lives elsewhere.

## Notes

- The IPC server only binds to `127.0.0.1`, so it's not reachable from other
  machines.
- If a `haptic-device` binary built before this launcher existed is launched,
  it simply won't open the control port — the launcher will show "Could not
  reach the live-control port" after ~10s and the process still runs fine
  with mouse/keyboard/haptic-device input; you just won't get live control
  from the GUI.

## Running under WSL

`platform.system()` reports `"Linux"` inside WSL, so binary discovery already
falls back to `bin/lin-<arch>/haptic-device` with no launcher changes needed.
To actually see and control the simulation from WSL:

- Build `haptic-device` following the README's Linux instructions from
  *inside* your WSL distro (a native Windows build won't run there).
- You need a display: Windows 11's built-in WSLg works out of the box; on
  Windows 10 install an X server (e.g. VcXsrv) and set `DISPLAY` before
  launching.
- The haptic device itself is a USB device attached to Windows, not WSL. Use
  [`usbipd-win`](https://github.com/dorssel/usbipd-win) to bind and attach it
  to your WSL distro (`usbipd bind`/`usbipd attach`) before starting
  `haptic-device`; otherwise it runs fine in keyboard/mouse-only mode.
- Run the launcher the same way as anywhere else: `python -m launcher.main`
  from inside the WSL distro.
