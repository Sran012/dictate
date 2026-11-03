# where are we. this is the front door, everything downstream reads this so we
# only write the linux-specific branches once.

import os


def _os_release():
    info = {}
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    k, v = line.split("=", 1)
                    info[k] = v.strip().strip('"')
    except FileNotFoundError:
        pass
    return info


def distro():
    return _os_release().get("ID", "unknown")


def desktop():
    return os.environ.get("XDG_CURRENT_DESKTOP", "unknown")


def session():
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return "unknown"


def is_gnome():
    d = desktop().lower()
    return "gnome" in d or "zorin" in d or "linuxmint" in d or "pop" in d


def is_kde():
    return "kde" in desktop().lower()


def is_sway():
    return "sway" in os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
