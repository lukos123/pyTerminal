

import os
from data import PATH
import importlib
import json
from prompt_toolkit import HTML
from prompt_toolkit.completion import Completer, Completion
import compile_functions
import command_type as t
functions = compile_functions.functions


def get_command_json():

    name = os.name
    command_json = "command.json"
    command_json_OS = "command_windows.json"

    if name == "posix":
        command_json_OS = "command_linuks.json"
    with open(f'{PATH}/{command_json}', 'r') as f:
        command_json = json.load(f)
    with open(f'{PATH}/{command_json_OS}', 'r') as f:
        command_json = command_json + json.load(f)
    return command_json


data: list = get_command_json()


def sort_by_similarity(arr, string):
    ready_arr = []
    temp_arr = []

    for it in arr:
        i = it[0]

        try:
            i = i.index(string)
        except:
            print(string, i)
            return []
        if i == 0:
            ready_arr.append(it)
            continue
        temp_arr.append(it)
    for i in temp_arr:
        ready_arr.append(i)
    return ready_arr


class MyCompleter(Completer):

    data = data

    def reload():
        importlib.reload(compile_functions)

    def get_completions(self, document, complete_event):

        text_before_cursor = document.text_before_cursor

        words = text_before_cursor.split()

        if words:
            current_word = words[-1]
        else:
            current_word = ''

        def code_generator(nesting, arr, current_word, text_before_cursor, words):
            ready_arr = []
            temp_ready_arr = []

            find = False
            if t.next_always in arr:

                for i in arr:
                    # temp_i = i
                    if t.next_always == i or isinstance(i, list):
                        continue
                    command = i[t.command]

                    if nesting < len(words):
                        if not isinstance(arr[-1], str):

                            arr_ = code_generator(nesting+1, arr[-1], current_word,
                                                  text_before_cursor, words)
                            ready_arr = ready_arr + arr_
                        else:

                            # if i[t.compile_function] != "":
                            name_function = arr[-1]

                            temp_arr_1 = functions[name_function](
                            )

                            temp_arr = []

                            for r in temp_arr_1:
                                temp_arr.append({
                                    t.command: r,
                                    t.help: "",
                                    t.compile_function: "",
                                    t.addon_with_compile_function: [],
                                    t.next: [],
                                    t.next_always: False
                                })

                            # if f"{temp_i}_c_addon" in arr:
                            # for r in i[t.addon_with_compile_function]:
                            #     temp_arr.append(r)

                            arr_ = code_generator(nesting+1, temp_arr, current_word,
                                                  text_before_cursor, words)
                            ready_arr = ready_arr + arr_

                        break
                    elif nesting == len(words):
                        # if text_before_cursor[-1] == " ":

                        # arr_ = code_generator(nesting, arr[-1], current_word,
                        #                       text_before_cursor, words)
                        # ready_arr = ready_arr + arr_
                        # break
                        if text_before_cursor[-1] == " ":
                            if not isinstance(arr[-1], str):
                                for r in arr[-1]:
                                    ready_arr.append(
                                        [f"{r[t.command]} [{r[t.help]}]", 0])
                            else:

                                # if i[t.compile_function] != "":
                                name_function = arr[-1]

                                temp_arr = functions[name_function](
                                )

                                # temp_arr = []

                                # for r in temp_arr_1:
                                #     temp_arr.append({
                                #         t.command: r,
                                #         t.help: "",
                                #         t.compile_function: "",
                                #         t.addon_with_compile_function: [],
                                #         t.next: [],
                                #         t.next_always: False
                                #     })

                                # if f"{temp_i}_c_addon" in arr:
                                # for r in i[t.addon_with_compile_function]:
                                #     temp_arr.append(r)
                                # temp_arr = temp_arr + \
                                #     i[t.addon_with_compile_function]
                                # if i[t.next_always]:
                                #     temp_arr = temp_arr + [i[t.next]]
                                #     temp_arr.insert(0,t.next_always)
                                for r in temp_arr:
                                    ready_arr.append([r, 0])

                        else:
                            pass
                            arr_ = code_generator(nesting, arr[1:-1], current_word,
                                                  text_before_cursor, words)
                            ready_arr = ready_arr + arr_
                        break

                    # elif nesting == len(words)-1:

                return ready_arr
            for i in arr:

                command = i[t.command]

                help = i[t.help]
                # if "_c_addon" in temp_i:

                #     continue

                if words[nesting-1] in command:
                    if words[nesting-1] != command:
                        temp_ready_arr.append(
                            [f"{command} [{help}]", -len(current_word)])
                    else:
                        find = True
                        if i[t.next] or i[t.compile_function]:

                            if len(words) == nesting:
                                if text_before_cursor[-1] == ' ':

                                    # if isinstance(arr[temp_i], dict):
                                    if i[t.compile_function] == "":

                                        for i1 in i[t.next]:
                                            # if "_c_addon" in i1:
                                            #     continue
                                            ready_arr.append(
                                                [f"{i1[t.command]} [{i1[t.help]}]", 0])
                                    else:
                                        name_function = i[t.compile_function]

                                        temp_arr = functions[name_function](
                                        )

                                        # if f"{temp_i}_c_addon" in arr:
                                        for r in i[t.addon_with_compile_function]:
                                            # if "c_all" == r or "c_all_c_addon" == r:
                                            #     continue
                                            temp_arr.append(
                                                f"{r[t.command]} [{r[t.help]}]")

                                        if temp_arr:
                                            for r in temp_arr:
                                                ready_arr.append(
                                                    [r, 0])

                                    # ready_arr = ready_arr+temp_arr

                            else:
                                # if isinstance(arr[temp_i], str):
                                if i[t.compile_function] != "":

                                    name_function = i[t.compile_function]

                                    temp_arr_1 = functions[name_function](
                                    )

                                    temp_arr = []

                                    for r in temp_arr_1:
                                        temp_arr.append({
                                            t.command: r,
                                            t.help: "",
                                            t.compile_function: "",
                                            t.addon_with_compile_function: [],
                                            t.next: [],
                                            t.next_always: False
                                        })

                                    # if f"{temp_i}_c_addon" in arr:
                                    # for r in i[t.addon_with_compile_function]:
                                    #     temp_arr.append(r)
                                    temp_arr = temp_arr + \
                                        i[t.addon_with_compile_function]

                                    if i[t.next_always]:
                                        temp_arr = temp_arr + [i[t.next]]
                                        temp_arr.insert(0, t.next_always)
                                    # temp_obj = {}
                                    # for r in temp_arr:
                                    #     if r == "c_all" or r == "c_all_c_addon":
                                    #         temp_obj[r] = arr[f"{temp_i}_c_addon"][r]
                                    #         continue

                                    #     temp_obj[r] = "N"
                                    arr_ = code_generator(nesting+1, temp_arr, current_word,
                                                          text_before_cursor, words)
                                    ready_arr = ready_arr + arr_
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

                                    arr_ = code_generator(nesting+1, i[t.next], current_word,
                                                          text_before_cursor, words)
                                    ready_arr = ready_arr + arr_
                        else:
                            pass

            if not find:
                ready_arr = temp_ready_arr
            return ready_arr
        if len(words) > 0:
            if words[0] == '?':
                for i in self.data:
                    yield Completion(i[t.command], start_position=-1, style='bg:#000 fg:#0099ff')

            # print(self.data)

            ready_arr = code_generator(1, self.data, current_word,
                                       text_before_cursor, words)
            temp_arr = []
            if text_before_cursor[-1] != "-":

                for i in ready_arr:

                    if i[0][0] != "-":
                        temp_arr.append(i)

                ready_arr = temp_arr
            if text_before_cursor[-1] != " ":

                ready_arr = sort_by_similarity(ready_arr, current_word)
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
