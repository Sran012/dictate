# whisper time. we call the whisper.cpp binary directly, its the only sane way
# english transcription. whisper.cpp binary, direct call.

import os
import subprocess

WHISPER = os.path.expanduser("~/.local/share/dictate/whisper/ggml-base.en.bin")


def transcribe(wav_path, language="en"):
    cmd = [WHISPER, "-m", WHISPER, "-f", wav_path, "-l", language, "-t", "30"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return out.stdout.strip()
