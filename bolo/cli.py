import argparse
import os
import subprocess
import time

from . import detect
from . import mic as micmod
from . import type as typemod
from . import transcribe


def _run(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def cmd_install(dry_run=False):
    print("bolo: step 1/5 — audio check")
    # audio check would live here, abbreviated for now

    print("bolo: step 2/5 — mic scan (dynamic, we measure not guess)")
    best_mic, best_rms = micmod.scan()[0]
    print(f"  picked {best_mic['name']} rms={best_rms:.4f}")

    print("bolo: step 3/5 — whisper model")
    if not os.path.exists(transcribe.WHISPER):
        subprocess.run(["mkdir", "-p", os.path.dirname(transcribe.WHISPER)])
        subprocess.run(["curl", "-L", "-o", transcribe.WHISPER,
                        "https://github.com/ggerganov/whisper.cpp/releases/download/"
                        "v1.0.0/ggml-base.bin"])

    print("bolo: step 4/5 — typing")
    typemod.type_text("hola")

    print("done. (rest of the steps land soon)")


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
