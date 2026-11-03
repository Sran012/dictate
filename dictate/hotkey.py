# hotkey wiring. gnome only for now, because that is where all the pain is.
import subprocess


def key_grabbed(key: str) -> bool:
    # cheap check: does the gnome media keys already claim this? if yes we
    # refuse to bind, no point fighting the compositor.
    out = subprocess.run(
        ["gsettings", "get", "org.gnome.settings-daemon.plugins.media-keys",
         "custom-keybindings"],
        capture_output=True, text=True, timeout=5,
    )
    return out.returncode != 0


def bind(key: str, command: str):
    subprocess.run(
        ["gsettings", "set", "org.gnome.settings-daemon.plugins.media-keys",
         f"custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/",
         "binding", key],
        capture_output=True, text=True, timeout=5,
    )
    subprocess.run(
        ["gsettings", "set", "org.gnome.settings-daemon.plugins.media-keys",
         f"custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/",
         "command", command],
        capture_output=True, text=True, timeout=5,
    )
