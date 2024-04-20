

import json
from prompt_toolkit import HTML
from prompt_toolkit.completion import Completer, Completion
from compile_functions import functions
from data import PATH
import os


def get_command_json():

    name = os.name
    command_json = "command.json"
    command_json_OS = "command_windows.json"

    if name == "posix":
        command_json_OS = "command_linuks.json"
    with open(f'{PATH}/{command_json}', 'r') as f:
        command_json: dict = json.load(f)
    with open(f'{PATH}/{command_json_OS}', 'r') as f:
        command_json = {**command_json, **json.load(f)}
    return command_json


data = get_command_json()


class MyCompleter(Completer):

    data = data

    def get_completions(self, document, complete_event):

        text_before_cursor = document.text_before_cursor

        words = text_before_cursor.split()

        if words:
            current_word = words[-1]
        else:
            current_word = ''

        def code_generator(nesting, obj, current_word, text_before_cursor, words):
            ready_arr = []
            temp_ready_arr = []

            find = False
            if "c_all" in obj:
                for i in obj:
                    temp_i = i
                    i = i.split(" ")[0]
                    if "c_all" == temp_i:
                        continue

                    if nesting < len(words):
                        if not isinstance(obj["c_all"], dict):
                            name_function = obj["c_all"]

                            temp_arr = functions[name_function](
                            )
                            if f"c_all_c_addon" in obj:
                                for r in obj[f"c_all_c_addon"]:
                                    temp_arr.append(r)
                            temp_obj = {}
                            for r in temp_arr:
                                if r == "c_all":
                                    temp_obj[r] = obj[f"c_all_c_addon"][r]
                                    continue
                                temp_obj[r] = "N"

                            arr = code_generator(nesting+1, temp_obj, current_word,
                                                 text_before_cursor, words)
                            ready_arr = ready_arr + arr
                        else:

                            arr = code_generator(nesting+1, obj["c_all"], current_word,
                                                 text_before_cursor, words)
                            ready_arr = ready_arr + arr
                        break
                    elif nesting == len(words):
                        if text_before_cursor[-1] == " ":
                            if not isinstance(obj["c_all"], dict):
                                name_function = obj["c_all"]

                                temp_arr = functions[name_function](
                                )

                                if f"c_all_c_addon" in obj:
                                    for r in obj[f"c_all_c_addon"]:
                                        if "c_all" == r:
                                            continue
                                        temp_arr.append(r)

                                if temp_arr:
                                    for r in temp_arr:
                                        ready_arr.append(
                                            [r, 0])
                            else:
                                for r in obj["c_all"]:
                                    ready_arr.append([r, 0])
                            break
                        else:

                            if words[nesting-1] in i:
                                if words[nesting-1] != i:
                                    ready_arr.append(
                                        [temp_i, -len(current_word)])

                    # elif nesting == len(words)-1:

                return ready_arr
            for i in obj:
                temp_i = i
                i = i.split(" ")[0]
                if "_c_addon" in temp_i:

                    continue

                if words[nesting-1] in i:
                    if words[nesting-1] != i:
                        temp_ready_arr.append([temp_i, -len(current_word)])
                    else:
                        find = True
                        if obj[temp_i] != 'N':

                            if len(words) == nesting:
                                if text_before_cursor[-1] == ' ':

                                    if isinstance(obj[temp_i], dict):

                                        for i1 in obj[temp_i]:
                                            if "_c_addon" in i1:
                                                continue
                                            ready_arr.append([i1, 0])
                                    else:
                                        name_function = obj[temp_i]

                                        temp_arr = functions[name_function](
                                        )

                                        if f"{temp_i}_c_addon" in obj:
                                            for r in obj[f"{temp_i}_c_addon"]:
                                                if "c_all" == r or "c_all_c_addon" == r:
                                                    continue
                                                temp_arr.append(r)

                                        if temp_arr:
                                            for r in temp_arr:
                                                ready_arr.append(
                                                    [r, 0])

                                    # ready_arr = ready_arr+temp_arr

                            else:
                                if isinstance(obj[temp_i], str):

                                    name_function = obj[temp_i]

                                    temp_arr = functions[name_function](
                                    )

                                    if f"{temp_i}_c_addon" in obj:
                                        for r in obj[f"{temp_i}_c_addon"]:
                                            temp_arr.append(r)
                                    temp_obj = {}
                                    for r in temp_arr:
                                        if r == "c_all" or r == "c_all_c_addon":
                                            temp_obj[r] = obj[f"{temp_i}_c_addon"][r]
                                            continue

                                        temp_obj[r] = "N"
                                    arr = code_generator(nesting+1, temp_obj, current_word,
                                                         text_before_cursor, words)
                                    ready_arr = ready_arr + arr
                                    # for r in temp_arr:
                                    #     if words[nesting] in r:
                                    #         if words[nesting] != r:
                                    #             ready_arr.append(
                                    #                 [r, -len(words[nesting])])
                                    # else:

                                    #     if f"{i}_c_all" in obj:
                                    #         if isinstance(obj[f"{i}_c_all"], dict):

                                    #             arr = code_generator(nesting+1, obj[f"{i}_c_all"], current_word,
                                    #                                  text_before_cursor, words)[0]
                                    #             ready_arr = ready_arr + arr
                                else:

                                    arr = code_generator(nesting+1, obj[temp_i], current_word,
                                                         text_before_cursor, words)
                                    ready_arr = ready_arr + arr
                        else:
                            pass

            if not find:
                ready_arr = temp_ready_arr
            return ready_arr
        if len(words) > 0:
            if words[0] == '?':
                for i in self.data:
                    yield Completion(i, start_position=-1, style='bg:#000 fg:#0099ff')

            # print(self.data)

            ready_arr = code_generator(1, self.data, current_word,
                                       text_before_cursor, words)
            maximum = 0
            for i in ready_arr:
                if maximum < len(i[0].split(" ")[0]):
                    maximum = len(i[0].split(" ")[0])+1
            for i in ready_arr:
                meta_text = (' '.join(i[0].split(' ')[1:])).replace(
                    '<', '(').replace('>', ')')
                yield Completion(i[0].split(" ")[0], start_position=i[1], style='bg:#000 fg:#0099ff', display=HTML(f"<b fg='#0099ff'>{i[0].split(' ')[0]}</b>{' '*(maximum-len(i[0].split(' ')[0]))}<b bg='#000'> <yellow>{meta_text}</yellow></b>"))

            if text_before_cursor[::-1].find("\\. ") != -1:
                index = len(text_before_cursor)-2 - \
                    text_before_cursor[::-1].find("\\. ")
                der = os.listdir(os.path.join(os.getcwd()))
                files = []
                folders = []
                text = text_before_cursor[index+2:]

                text = text.split("\\")

                if len(text) == 1:
                    if text[0] == "":
                        for i in der:
                            if os.path.isdir(os.path.join(os.getcwd(), i)):
                                folders.append(i)

                            if os.path.isfile(os.path.join(os.getcwd(), i)):
                                files.append(i)

                        folders.sort()
                        files.sort()
                        yield Completion('..', start_position=0, style='bg:#000 fg:yellow')
                        for i in folders:
                            yield Completion(i, start_position=0, style='bg:#000 fg:yellow')
                        for i in files:
                            yield Completion(i, start_position=0, style='bg:#000 fg:cyan')
                    else:
                        for i in der:

                            if os.path.isdir(os.path.join(os.getcwd(), i)):
                                if text[-1] in i:
                                    if text[-1] != i:

                                        folders.append([i, -len(text[-1])])

                            if os.path.isfile(os.path.join(os.getcwd(), i)):
                                if text[-1] in i:
                                    if text[-1] != i:
                                        files.append([i, -len(text[-1])])
                        folders = sorted(folders, key=lambda x: x[0])
                        files = sorted(files, key=lambda x: x[0])

                        for i in folders:
                            yield Completion(i[0], start_position=i[1], style='bg:#000 fg:yellow')
                        for i in files:
                            yield Completion(i[0], start_position=i[1], style='bg:#000 fg:cyan')
                else:
                    path = ''
                    if len(text) == 2:
                        path += text[0]+'\\'
                    else:
                        for i in text[0:-1]:
                            path += i+'\\'
                    path = os.path.join(os.getcwd(), path)

                    if os.path.isdir(path):
                        if text_before_cursor[-1] == '\\':
                            for i in os.listdir(path):

                                if os.path.isdir(os.path.join(path, i)):
                                    folders.append(i)

                                if os.path.isfile(os.path.join(path, i)):
                                    files.append(i)

                            folders.sort()
                            files.sort()
                            yield Completion('..', start_position=0, style='bg:#000 fg:yellow')
                            for i in folders:
                                yield Completion(i, start_position=0, style='bg:#000 fg:yellow')
                            for i in files:
                                yield Completion(i, start_position=0, style='bg:#000 fg:cyan')
                        else:
                            for i in os.listdir(path):

                                if os.path.isdir(os.path.join(path, i)):
                                    if text[-1] in i:
                                        if text[-1] != i:
                                            folders.append([i, -len(text[-1])])

                                if os.path.isfile(os.path.join(path, i)):
                                    if text[-1] in i:
                                        if text[-1] != i:
                                            files.append([i, -len(text[-1])])
                            folders = sorted(folders, key=lambda x: x[0])
                            files = sorted(files, key=lambda x: x[0])

                            for i in folders:
                                yield Completion(i[0], start_position=i[1], style='bg:#000 fg:yellow')
                            for i in files:
                                yield Completion(i[0], start_position=i[1], style='bg:#000 fg:cyan')
