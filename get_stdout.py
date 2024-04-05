import subprocess
import os


def branch():
    command = "/usr/bin/git branch"
    name = os.name
    if name == "ne":
        command = "git branch"
    print(command)
    result: subprocess.CompletedProcess[str]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except:
        pass
    return result.stdout
