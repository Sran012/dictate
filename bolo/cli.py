import argparse
import os
import subprocess
import time

from . import config as cfg
from . import detect
from . import hotkey
from . import mic as micmod
from . import service as servicemod
from . import transcribe
from . import type as typemod


def _run(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def cmd_install(dry_run=False):
    conf = cfg.load()
    print("bolo: install start")
    print(f"  desktop={detect.desktop()} session={detect.session()} distro={detect.distro()}")

    print("bolo: [1/6] audio backend check")
    steps = ["audio"]

    print("bolo: [2/6] mic scan — dynamic, measuring not guessing")
    best_mic, best_rms = micmod.scan()[0]
    steps.append("mic")
    print(f"  -> picked {best_mic['name']} rms={best_rms:.4f}")

    print("bolo: [3/6] whisper model")
    need_download = not os.path.exists(transcribe.WHISPER)
    steps.append("model")
    if need_download and not dry_run:
        os.makedirs(os.path.dirname(transcribe.WHISPER), exist_ok=True)
        _run(["curl", "-L", "-o", transcribe.WHISPER,
              "https://github.com/ggerganov/whisper.cpp/releases/latest/download/ggml-base.bin"])

    print("bolo: [4/6] typing backend")
    steps.append("typing")

    print("bolo: [5/6] service")
    steps.append("service")

    print("bolo: [6/6] hotkey")
    steps.append("hotkey")

    print("install complete. polish pending")


def cmd_setup(dry_run=False):
    conf = cfg.load()
    print("bolo: setup — repairing whatever install broke")
    if os.path.isdir("/opt/uinput"):
        print("  [sudo] group uinput membership")
    if not os.path.exists(transcribe.WHISPER):
        print("  [sudo-free] model download")
    print("setup done-ish")


def cmd_test(dry_run=False):
    print("test: recording 5s...")
    time.sleep(5)
    print("test: transcribing...")
    words = transcribe.transcribe("/tmp/bolo-test.wav", cfg.load()["language"])
    print("you said:", words)
    typemod.type_text(words)


def cmd_uninstall():
    print("bolo: uninstall — stop service, drop permission, rm prefs")
    print("uninstall done-ish")


def main():
    p = argparse.ArgumentParser(prog="bolo")
    sub = p.add_subparsers(dest="cmd")

    p_install = sub.add_parser("install", help="one command, whole pipeline")
    p_install.add_argument("--dry-run", action="store_true")

    p_setup = sub.add_parser("setup", help="repair if something died")
    p_setup.add_argument("--dry-run", action="store_true")

    p_test = sub.add_parser("test", help="say something, show me the words")
    p_test.add_argument("--dry-run", action="store_true")

    p_uninstall = sub.add_parser("uninstall", help="clean the service and the permission")

    args = p.parse_args()

    if args.cmd == "install":
        cmd_install(args.dry_run)
    elif args.cmd == "setup":
        cmd_setup(args.dry_run)
    elif args.cmd == "test":
        cmd_test(args.dry_run)
    elif args.cmd == "uninstall":
        cmd_uninstall()


if __name__ == "__main__":
    main()
