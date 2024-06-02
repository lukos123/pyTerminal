import json
import os

from data import PATH
import command_type as t


def add(words: list[str]):
    def rec(id: int, words: list[str], data:list):

        search = False
        for i, it in enumerate(data):
            if it[t.command] == words[id]:
                data[i][t.next] = rec(id+1, words, it[t.next])
                search =True
                break
        if not search:
            data.append({
                        t.command: words[id],
                        t.help: "",
                        t.compile_function: "",
                        t.addon_with_compile_function: [],
                        t.next: [],
                        t.next_always: False
                    })
            if id < len(words)-1:
                data[-1][t.next] = rec(id+1, words, [])

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
