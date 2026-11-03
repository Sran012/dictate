# user prefs. we keep this tiny, just the things the user actually chose.
import os
import yaml


DEFAULTS = {
    "language": "auto",       # auto | hi | en
    "hotkey": "<Super>d",     # set at install time
    "mode": "type",           # type | paste
    "mic": "auto",            # auto means scan every time
}


def load():
    path = os.path.expanduser("~/.config/bolo/config.yaml")
    if not os.path.exists(path):
        return dict(DEFAULTS)
    with open(path) as f:
        return {**DEFAULTS, **yaml.safe_load(f) or {}}


def save(cfg):
    path = os.path.expanduser("~/.config/bolo/config.yaml")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(cfg, f)
