# turn words into keystrokes. uses ydotool via its daemon.
import subprocess


def type_text(text):
    subprocess.run(
        ["ydotool", "type", "--delay", "0", text],
        capture_output=True, text=True, timeout=600,
    )
