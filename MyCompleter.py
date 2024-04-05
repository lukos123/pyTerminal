

import json
from prompt_toolkit.completion import Completer, Completion
from compile_functions import functions

import os
with open('C:\\terminal\\command.json', 'r') as f:

    data = json.load(f)


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
            files = []
            folders = []

            for i in obj:

                if words[nesting-1] in i:
                    if words[nesting-1] != i:
                        ready_arr.append([i, -len(current_word)])
                    else:
                        if obj[i] != 'N':

                            if len(words) == nesting:
                                if text_before_cursor[-1] == ' ':

                                    if isinstance(obj[i], dict):

                                        for i1 in obj[i]:
                                            ready_arr.append([i1, 0])
                                    else:
                                        name_function = obj[i]

                                        temp_arr = functions[name_function](
                                        )
                                        if temp_arr:

                                            ready_arr = ready_arr+temp_arr

                            elif isinstance(obj[i], str):

                                name_function = obj[i]

                                temp_arr = functions[name_function](
                                )

                                for r in temp_arr:
                                    if current_word in r[0]:
                                        if current_word != r[0]:
                                            ready_arr.append(
                                                [r[0], -len(current_word)])
                            else:

                                arr = code_generator(nesting+1, obj[i], current_word,
                                                     text_before_cursor, words)[0]
                                ready_arr = ready_arr + arr
                        else:
                            pass
            return ready_arr, files, folders
        if len(words) > 0:
            if words[0] == '?':
                for i in self.data:
                    yield Completion(i, start_position=-1, style='bg:#000 fg:blue')

            # print(self.data)

            ready_arr, files, folders = code_generator(1, self.data, current_word,
                                                       text_before_cursor, words)
            for i in ready_arr:
                yield Completion(i[0], start_position=i[1], style='bg:#000 fg:blue')
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

            else:

                for i in files:
                    yield Completion(i[0], start_position=i[1], style='bg:#000 fg:cyan')
                for i in folders:
                    yield Completion(i[0], start_position=i[1], style='bg:#000 fg:yellow')
