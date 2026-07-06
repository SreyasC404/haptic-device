"""Locates the compiled haptic-device binary for the current OS/architecture."""

import platform
import struct
from pathlib import Path


def repo_root() -> Path:
    """The CHAI3D checkout root (parent of this haptic-device/ directory)."""
    return Path(__file__).resolve().parent.parent.parent


def default_binary_dir_name() -> str:
    system = platform.system()
    if system == "Darwin":
        return f"mac-{platform.machine()}"
    if system == "Windows":
        is_64_bit = struct.calcsize("P") * 8 == 64
        return "win-x64" if is_64_bit else "win-Win32"
    return f"lin-{platform.machine()}"


def default_binary_path() -> Path:
    name = "haptic-device.exe" if platform.system() == "Windows" else "haptic-device"
    return repo_root() / "bin" / default_binary_dir_name() / name
