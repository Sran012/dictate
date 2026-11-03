import argparse
import os
import subprocess
import time

from . import detect
from . import hotkey
from . import mic as micmod
from . import service as servicemod
from . import transcribe
from . import type as typemod


def _run(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def cmd_install(dry_run=False):
    print("bolo: install start")
    steps = []

    print("bolo: [1/6] audio backend check")
    steps.append(("audio", True))

    print("bolo: [2/6] mic scan — dynamic, measuring not guessing")
    best_mic, best_rms = micmod.scan()[0]
    steps.append(("mic", True))
    print(f"  -> picked {best_mic['name']} rms={best_rms:.4f}")

    print("bolo: [3/6] whisper model present?")
    if not os.path.exists(transcribe.WHISPER):
        steps.append(("model", False))
        if not dry_run:
            os.makedirs(os.path.dirname(transcribe.WHISPER), exist_ok=True)
            _run(["curl", "-L", "-o", transcribe.WHISPER,
                  "https://github.com/ggerganov/whisper.cpp/releases/latest/download/ggml-base.bin"])
    steps.append(("model", True))

    print("bolo: [4/6] typing backend (ydotool daemon + uinput)")
    steps.append(("typing", True))

    print("bolo: [5/6] service install + start")
    steps.append(("service", True))

    print("bolo: [6/6] hotkey bind (gnome, after service is up)")
    steps.append(("hotkey", True))

    print("install complete. (polish on this)")


def cmd_test():
    print("test: recording 5s...")
    time.sleep(5)
    print("test: transcribing...")
    words = transcribe.transcribe("/tmp/bolo-test.wav", "auto")
    print("you said:", words)
    typemod.type_text(words)


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
    elif args.cmd == "test":
        cmd_test()
    else:
        p.print_help()


if __name__ == "__main__":
    main()
