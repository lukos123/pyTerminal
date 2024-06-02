
import json
import os


from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.styles import Style as St
from data import PATH
import subprocess
import sys
from playsound import playsound
import colorama
from MyCompleter import MyCompleter, get_command_json
import importlib

import custom_functions
from get_stdout import branch


colorama.init()


args = sys.argv


cwd = os.getcwd()
drive, _ = os.path.splitdrive(cwd)

completer = MyCompleter()
path_to_python = f'python'
path_to_pyinstaller = f'pyinstaller'
path_to_pip = f'pip'
session = PromptSession(completer=MyCompleter())

path_to_git = f'git'
npm_bat = f'{drive}/runvueserver.bat'
first_directory = args[1]

os.chdir(first_directory)


def app():
    try:

        while True:

            text = branch()
            current_branch = ""
            if text != "":
                branches = text.split('\n')

                for i in branches:
                    if i[0] == '*':
                        current_branch = i
                        break

            now_directory = os.getcwd()

            def bottom_toolbar():
                return [('class:bottom-toolbar', '         Итс май апликатион!')]
            our_style = St.from_dict({
                '':   '#0099ff bold',
                'bottom-toolbar': 'fg:#ffffff bg:#ff0000',
                # 'sw':   '#fff bold',


            })

            completer.data = get_command_json()
            playsound(f"{PATH}/ok.mp3", False)
            if current_branch == "":
                command = session.prompt(
                    HTML(f"<b><yellow>{now_directory}</yellow><violet>?</violet></b>"), completer=completer,
                    style=our_style, bottom_toolbar=bottom_toolbar).split()
            else:
                command = session.prompt(
                    HTML(f"<b><yellow>{now_directory}</yellow>(<green>{current_branch}</green>)<violet>?</violet></b>"), completer=completer,
                    style=our_style, bottom_toolbar=bottom_toolbar).split()
            if len(command) > 0:
                now_directory = os.getcwd()
                if command[0] == 'ls':
                    custom_functions.ls(command, now_directory, '└───')
                elif command[0] == 'cd':
                    cd = ''

                    if len(command) > 2:
                        for i in range(len(command)-1):
                            cd += command[i+1]+' '

                    else:
                        cd = command[1]
                    cd = os.path.join(now_directory, cd)

                    try:
                        os.chdir(cd)
                    except:
                        print('error')
                elif command[0] == 'html':
                    custom_functions.html(command, now_directory, path_to_git)
                elif command[0] == 'create':
                    custom_functions.create(command, now_directory)

                elif command[0] == 'pip':
                    custom_functions.pip(command, path_to_pip)
                elif command[0] == 'git':
                    custom_functions.git(command, path_to_git)
                elif command[0] == 'new':
                    custom_functions.new(now_directory)
                elif command[0] == 'add':
                    custom_functions.add_new_command(command)
                elif command[0] == 'addf':
                    custom_functions.add_new_command_f(command)
                elif command[0] == 'settings':
                    custom_functions.open_settings()
                elif command[0] == 'exit':
                    quit()
                elif command[0] == 'reload':
                    MyCompleter.reload()

                elif command[0] == 'pyinstaller':

                    custom_functions.py_installer(
                        now_directory,  command, path_to_pyinstaller)
                else:
                    command_another = ''
                    for i in command:
                        command_another += f'{i} '
                    os.system(command_another)
    except KeyboardInterrupt:
        print('\nControl+C был нажат, но программа не выключается.')


if __name__ == '__main__':
    while True:
        try:
            app()
        except Exception as t:
            print("err")
            print(t)
