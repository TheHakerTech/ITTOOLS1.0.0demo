# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Callable
from rich.console import Console
import libs.errors as err
import libs.sqlCoder as sql
import threading
import time
import json
import os

# Consts
LOGO = """[cyan]
██ ██████ ██████ ███████ ███████ ██
██   ██     ██   ██   ██ ██   ██ ██
██   ██     ██   ██   ██ ██   ██ ██
██   ██     ██   ███████ ███████ ██████[/]
"""
CENTER = "center"
LEFT = "left"
RIGHT = "right"
YES = 'y'
NOT = 'n'
ALL = "*"
LVL1 = "[red]>[/]"
LVL2 = "[green]>>[/]"
LVL3 = "[yellow]>>>[/]"

DEVELOPERS_LIST = ['TheHakerTech', 'An72ty']
# Commands names consts
HELP = 'help'
RESTART = 'restart'
PINFO = 'pinfo'
ACTIVATE = 'activate'
DEACTIVATE = 'deactivate'
EXIT = 'exit'
E = 'e'
CREDITS = 'credits'
# Categories
PLUGIN_TOOLS = 'Plugin tools'

# Create console object
console = Console()


class TextInfo:
    def __init__(
        self,
        name: str,
        description: str,
        detailDescription: str = None
    ) -> TextInfo:
        # Init attributes
        self.name = name
        self.description = description
        # If detail is None, detail is description
        self.detailDescription = detailDescription or description


class Groups:
    def __init__(
        self,
        list: list = []
    ) -> Groups:
        self.list = {group.name: group for group in list}
        self.commands = {}
        for group in self.list.values():
            self.commands.update(group.list)

    def update(self) -> None:
        self.commands = {}
        for group in self.list.values():
            self.commands.update(group.list)

    def addGroup(self, group) -> None:
        self.list[group.name] = group
        self.update()

    def print(self) -> None:
        for (groupName, group) in self.list.items():
            console.print('[bold white]{0}[/]'.format(groupName))
            group.print()


class Group(TextInfo):
    def __init__(
        self,
        name: str,
        description: str,
        list: list = [],
        detailDescription: str = None
    ) -> Group:
        super().__init__(name, description, detailDescription)
        self.list = {command.name: command for command in list}

    def addCommand(self, args) -> None:
        for command in args:
            self.list[command.name] = command

    def print(self) -> None:
        for (commandName, command) in self.list.items():
            console.print(
                '[cyan]{0}[/] [white]- {1}[/]'.format(commandName, command.description))


class Command(TextInfo):
    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        detailDescription: str = None
    ) -> None:
        super().__init__(name, description, detailDescription)
        self.function = function

    def print(self) -> None:
        console.print(
            '[cyan]{0}[/] [white]- {1}[/]'.format(self.name, self.detailDescription))

    def invoke(self) -> None:
        self.function()


def printLogo():
    console.print('[cyan]Eternal Arts | All rights reserved[/]')
    console.print('[white]=======================================[/]')
    console.print(LOGO)
    console.print('[white]=======================================[/]')


class AppData:
    # Link to console
    console = console
    groups = Groups()


# Init AppData in libs
err.init(AppData)
sql.init(AppData)


class App(AppData):
    def __init__(self, startCode: str = None) -> App:
        err.Functions.debug('App created')
        # Init sql table
        sql.initTable()
        err.Functions.debug(
            'Table has been initializated in data/pluginsInfoDB.db')
        # Start code is code which will execute on start
        self.startCode = startCode
        # Add commands
        self.addCommands()

    def addCommands(self) -> None:
        AppData.groups.addGroup(
            Group('System tools', 'System functions', list=[
                Command(HELP, self.help, 'Show info about commands'),
                Command(CREDITS, self.credits, 'Shows developers nicknames')
            ]
            )
        )

    def updating(self) -> None:
        while self.isUpdating:
            time.sleep(1)
            sql.updateDB()

    def start(self) -> None:
        err.Functions.debug('App started')
        sql.updateDB()
        err.Functions.debug('Data base updated')
        self.isUpdating = True
        self.updatingThread = threading.Thread(target=self.updating)
        self.updatingThread.start()
        # Prints
        printLogo()
        console.print(
            '[white]Welcome to[/] [cyan]ITTOOLS[/][white]! Type command which you need (words register in nan)[/]')
        AppData.groups.print()
        while True:
            console.print(LVL1, end=' ')
            answer = input()
            if answer.lower() in list(AppData.groups.commands.keys()):
                AppData.groups.commands[answer.lower()].invoke()
            else:
                console.print('Unknow command')
                err.Functions.error(
                    'Unknow command {0}'.format(answer.lower()))

    # Commands fuctions

    def help(self) -> None:
        console.print(
            '[white]Type command which instruction you need. (e - cancel)[/]')
        console.print(
            '[white]Or type[/] [green]*[/] [white]to get instruction of all commands.[/]')
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer.lower() in list(AppData.groups.commands.keys()):
                AppData.groups.commands[answer.lower()].print()
                break

            elif answer == ALL:
                AppData.groups.print()
                break

            elif answer == E:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break

            else:
                err.Functions.error(
                    'Unknow command {0}'.format(answer.lower()))

    def restart(self) -> None:
        console.print('[white]Are you sure to restart program? (y/n)[/]')
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer.lower() == YES:
                self.isUpdating = False
                raise err.Restart()
            elif answer.lower() == NOT:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break
            else:
                err.Functions.error('You have to answer y or n')

    def pinfo(self) -> None:
        console.print(
            '[white]Type plugin name which info you need. (e - cancel)[/]')
        console.print(
            '[white]Or type[/] [green]*[/] [white]to get info of all plugins.[/]')
        plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer in plugins.keys():
                console.print("{0} v{1} - {2}".format(answer,
                              plugins[answer][0], plugins[answer][1]))
                break

            elif answer == ALL:
                console.print('[white]Your installed plugins:[/]')
                plugins = sql.getPluginsList()
                if plugins:
                    for (name, version, status) in plugins:
                        console.print(
                            "[white]{0}[/] [cyan]v[/][white]{1}[/] [cyan]status:[/] {2}".format(name, version, status))
                else:
                    console.print('[white]You have not installed plugins![/]')
                break

            elif answer == E:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break

            else:
                err.Functions.error(
                    'Unknow plugin name {0}'.format(answer.lower()))

    def activate(self) -> None:
        console.print(
            '[white]Type plugin name which you need to activate. (e - cancel)[/]')
        console.print(
            '[white]Or type[/] [green]*[/] [white]to activate all plugins.[/]')
        plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer in plugins.keys():
                pinfo = json.loads(open(f'plugins/{answer}/info.json').read())
                pinfo['status'] = 'yes'
                with open(f'plugins/{answer}/info.json', 'w') as f:
                    f.write(json.dumps(pinfo))
                console.print(
                    f'[white]Plugin[/] [cyan]{answer}[/] [white]activated[/]')
                break

            elif answer == ALL:
                for (name, info) in plugins.items():
                    pinfo = json.loads(
                        open(f'plugins/{name}/info.json').read())
                    pinfo['status'] = 'yes'
                    with open(f'plugins/{name}/info.json', 'w') as f:
                        f.write(json.dumps(pinfo))
                    console.print('[green]Succes[/]')
                break

            elif answer == E:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break

            else:
                err.Functions.error('Unknow plugin name {0}'.format(answer))

    def deactivate(self) -> None:
        console.print(
            '[white]Type plugin name which you need to deactivate. (e - cancel)[/]')
        console.print(
            '[white]Or type[/] [green]*[/] [white]to deactivate all plugins.[/]')
        plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer in plugins.keys():
                pinfo = json.loads(open(f'plugins/{answer}/info.json').read())
                pinfo['status'] = 'no'
                with open(f'plugins/{answer}/info.json', 'w') as f:
                    f.write(json.dumps(pinfo))
                console.print(
                    f'[white]Plugin[/] [cyan]{answer}[/] [white]deactivated[/]')
                break

            elif answer == ALL:
                for (name, info) in plugins.items():
                    pinfo = json.loads(
                        open(f'plugins/{name}/info.json').read())
                    pinfo['status'] = 'no'
                    with open(f'plugins/{name}/info.json', 'w') as f:
                        f.write(json.dumps(pinfo))
                    console.print('[green]Succes[/]')
                break

            elif answer == E:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break

            else:
                err.Functions.error('Unknow plugin name {0}'.format(answer))

    def exit(self) -> None:
        console.print('[white]Are you sure to exit? (y/n)[/]')
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer.lower() == YES:
                self.isUpdating = False
                raise err.Exit()
            elif answer.lower() == NOT:
                err.Functions.debug('Cancelled operation')
                console.print('You cancelled')
                break
            else:
                err.Functions.error('You have to answer y or n')

    def credits(self) -> None:
        console.print('[cyan]ITTOOLS[/cyan] [white]developers:[/white]')
        for developer in DEVELOPERS_LIST:
            console.print(f'\t[blue]{developer}[/blue]')


def startApp():
    os.system('cls||clear')
    app = App()  # Create obj
    try:
        app.start()  # Start app
    except err.Restart:
        startApp()
    except err.Exit:
        pass
    except KeyboardInterrupt:
        app.isUpdating = False


# Launch
if __name__ == "__main__":
    startApp()
