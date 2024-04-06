import json
import os

from data import PATH


def add(words: list[str]):
    def rec(step: int, words: list[str], data):
        id = words.index(words[step])
        if words[step] in data:
            if id < len(words)-1:
                if isinstance(data[words[step]], dict):
                    data[words[step]] = rec(step+1, words, data[words[step]])
                else:
                    data[words[step]] = rec(
                        step+1, words, {words[step+1]: "N"})
            else:
                pass
        else:
            if id < len(words)-1:
                data[words[step]] = rec(step+1, words, {words[step+1]: "N"})
            else:
                data[words[step]] = "N"
        return data
    name =os.name
    command_json = "command.json"
    if name == "posix":
        command_json = "command_linuks.json"
    with open(f'{PATH}/{command_json}', 'r') as f:
        data = json.load(f)

    data = rec(0, words, data)
    with open(f'{PATH}/{command_json}', 'w') as f:
        f.write(json.dumps(data))


# import add_new_command as a
