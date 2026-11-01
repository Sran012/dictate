# whisper time. we call the whisper.cpp binary directly, its the only sane way
# to get hindi + english in one model without a python binding rabbit hole.

import os
import subprocess

WHISPER = os.path.expanduser("~/.local/share/bolo/whisper/ggml-base.bin")


def transcribe(wav_path, language="auto"):
    cmd = [WHISPER, "-m", WHISPER, "-f", wav_path, "-l", language, "-t", "30"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return out.stdout.strip()
