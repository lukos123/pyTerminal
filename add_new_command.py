import json
import os

from data import PATH


def add(words: list[str], is_f=False):
    def rec(id: int, words: list[str], data):

        # id = words.index(words[step])

        if words[id] in data:
            if id < len(words)-1:
                if isinstance(data[words[id]], dict):
                    data[words[id]] = rec(id+1, words, data[words[id]])
                else:
                    if data[words[id]] != "N":
                        if f"{words[id]}_c_addon" in data:
                            if isinstance(data[f"{words[id]}_c_addon"], dict):
                                data[f"{words[id]}_c_addon"] = rec(
                                    id+1, words, data[f"{words[id]}_c_addon"])
                            else:
                                pass
                        else:
                            data[f"{words[id]}_c_addon"] = rec(
                                id+1, words, {words[id+1]: "N"})
                    else:
                        data[words[id]] = rec(
                            id+1, words, {words[id+1]: "N"})
            else:
                if is_f:
                    data = words[id]

        else:
            if id < len(words)-1:
                data[words[id]] = rec(id+1, words, {words[id+1]: "N"})
            else:
                if is_f:
                    data = words[id]
                else:
                    data[words[id]] = "N"

        return data

    command_json = "command.json"

    with open(f'{PATH}/{command_json}', 'r') as f:
        data = json.load(f)

    data = rec(0, words, data)

    with open(f'{PATH}/{command_json}', 'w') as f:
        f.write(json.dumps(data))


def addf(words: list[str]):
    add(words, is_f=True)

# type a = dict


# import add_new_command as a
