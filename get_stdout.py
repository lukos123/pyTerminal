import subprocess
import os


def branch():
    command = ""
    name = os.name
    if name == "ne":
        command = "git branch"
    elif name == "posix":
        command = "/usr/bin/git branch"
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout
