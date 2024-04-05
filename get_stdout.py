import subprocess
import os


def branch():
    command = "/usr/bin/git branch"
    name = os.name
    if name == "ne":
        command = "git branch"

    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout
