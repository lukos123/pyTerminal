import subprocess
import os


def branch():
    command = ["/usr/bin/git", "branch"]
    name = os.name
    if name == "nt":
        command = ["git", "branch"]
    # print(name)
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout


def git_user_name():
    command = ["/usr/bin/git", "config", "--global", "user.username"]
    name = os.name
    if name == "nt":
        command = ["git", "config", "--global", "user.username"]
    # for i in command:
    #     print(i, end=" ")
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout


def git_get_remote():
    command = ["/usr/bin/git", "remote", "-v"]
    name = os.name
    if name == "nt":
        command = ["git", "remote", "-v"]
    
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout
