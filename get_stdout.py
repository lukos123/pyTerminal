import subprocess
import os


def branch():
    command = ["/usr/bin/git", "branch"]
    name = os.name
    if name == "nt":
        command = ["git", "branch"]
    print(name)
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout
