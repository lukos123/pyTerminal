import os
import subprocess

from get_stdout import branch


def git_branch():
    arr = []

    text = branch()
    if text != "":
        branches = text.split('\n')
        for i in branches:
            if i != "":
                arr.append([i[2:], 0])

    return arr


functions = {
    "git_branch": git_branch
}
