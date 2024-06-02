import os
import subprocess

from get_stdout import branch, git_user_name, git_get_remote, python_get_library
import requests


def git_branch():
    arr = []

    text = branch()
    if text != "":
        branches = text.split('\n')
        for i in branches:
            if i != "":
                arr.append(i[2:])

    return arr


def git_repos_url_local():
    user_name = git_user_name().replace(" ", "").replace("\n", "")

    if user_name != "":
        repos_url = f"https://api.github.com/users/{user_name}/repos"
        json = []
        try:
            json = requests.get(repos_url).json()
        except:
            return ["err", "err21"]
        arr = []

        for i in json:

            arr.append(i["html_url"])
        return arr
    return ["err", "err21"]


repos = git_repos_url_local()


def git_repos_url():
    return repos.copy()


def git_remote():
    arr = []

    text = git_get_remote()
    if text != "":
        remotes = text.split('\n')
        for i in remotes:
            if i != "":
                arr.append(i.split("http")[0][:-1])

    return list(set(arr))


def python_library_get():
    arr = []
    text = python_get_library()

    if text != "":
        library = text.split('\n')[2:]
        for i in library:
            if i != "":
                arr.append(i.split(" ")[0])
    return arr


library = python_library_get()


def python_library():
    return library.copy()


def next():
    return []


functions = {
    "git_branch": git_branch,
    "git_repos_url": git_repos_url,
    "python_library": python_library,
    "git_remote": git_remote,
    "next": next
}
