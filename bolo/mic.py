# mic handling. the os "default" is not a suggestion, it is a lie on many
# laptops. so we scan.

import sounddevice as sd
import numpy as np

HEAR_THRESHOLD = 0.05


def list_mics():
    out = []
    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0:
            out.append({"id": i, "name": dev["name"]})
    return out


def measure(mic_id, seconds=3):
    frames = int(16000 * seconds)
    with sd.InputStream(device=mic_id, samplerate=16000, channels=1, dtype="float32") as s:
        audio, _ = s.read(frames)
    return float(np.max(np.abs(audio)))


def scan():
    res = [(m, measure(m["id"])) for m in list_mics()]
    res.sort(key=lambda r: r[1], reverse=True)
    return res
