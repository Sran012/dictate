# the background service. this is the thing that holds the key and runs the
# loop. for now we just know what a unit file looks like, the actual install
# comes with the setup command.
import os


UNIT = """[Unit]
Description=bolo dictation
After=graphical-session.target

[Service]
ExecStart=/home/sujal/.local/bin/bolo-daemon
Restart=on-failure

[Install]
WantedBy=default.target
"""


def unit_text():
    return UNIT
