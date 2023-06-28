# -*- coding: utf-8 -*-
from __future__ import annotations
from rich.console import Console
from rich.tree import Tree
from libs.commandManager import *
import libs.commandManager as commandManager
import libs.errors as err
import plugins.installer.plugin as installer
import libs.sqlCoder as sql
import threading
import time
import json
import importlib
import os

# Consts
LOGO = """[cyan]
██ ██████ ██████ ███████ ███████ ██    ███████
██   ██     ██   ██   ██ ██   ██ ██    ██▄▄▄▄▄
██   ██     ██   ██   ██ ██   ██ ██    ▀▀▀▀▀██
██   ██     ██   ███████ ███████ █████ ███████[/]
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

libs = {'errors':err, 'sqlCoder':sql, 'commandManager':commandManager}
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

def printLogo():
    console.print('[cyan]Eternal Arts | All rights reserved[/]')
    console.print('[white]==============================================[/]')
    console.print(LOGO)
    console.print('[white]==============================================[/]')


class AppData:
    # Link to console
    console = console
    groups = Groups()


# Init AppData in libs
libs['errors'].init(AppData)
libs['sqlCoder'].init(AppData)
libs['commandManager'].init(AppData)


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
        # Plugins list
        self.plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
        self.activatedPlugins = {}


    def addCommands(self) -> None:
        AppData.groups.addGroup(
            Group('System tools', 'System functions', list=[
                Command(HELP, self.help, 'Show info about commands'),
                Command(RESTART, self.restart, 'Restart the programm'),
                Command(CREDITS, self.credits, 'Shows developers nicknames'),
                Command(EXIT, self.exit, 'Exit'),
            ])
        )
        AppData.groups.addGroup(
            Group('Plugin tools', 'Tools for plugins', list=[
                Command(PINFO, self.pinfo, 'Show info about plugin'),
                Command(ACTIVATE, self.activate, 'Activate plugin'),
                Command(DEACTIVATE, self.deactivate, 'Activate plugin')
            ])
        )

    def update(self) -> None:
        self.activatedPlugins = {}
        # Get activated plugin list
        activatedPluginsNames = []
        for (name, info) in self.plugins.items():
            if info[1] == 'yes':
                activatedPluginsNames.append(name)
        # Activate plugins
        for pname in activatedPluginsNames:
            pluginModule = importlib.import_module(f'plugins.{pname}.plugin')
            pluginModule.init(AppData)
            m = []
            for name in pluginModule.modulesNames:
                if name in libs.keys():
                    m.append(libs[name])

            self.p = pluginModule.p(AppData, m)
            self.activatedPlugins[pluginModule.NAME] = self.p
            self.p.activate()
        AppData.groups.clear()
        self.addCommands()

    def updating(self) -> None:
        while self.isUpdating:
            time.sleep(1)
            sql.updateDB()
            self.plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
            

    def start(self) -> None:
        err.Functions.debug('App started')
        sql.updateDB()
        err.Functions.debug('Data base updated')
        self.isUpdating = True
        self.updatingThread = threading.Thread(target=self.updating)
        self.updatingThread.start()
        # Prints
        printLogo()
        console.print('[white]Welcome to[/] [cyan]ITTOOLS[/][white]! Type command which you need (words register in nan)[/]')
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
        self.plugins = {t[0]: (t[1], t[2]) for t in sql.getPluginsList()}
        while True:
            console.print(LVL2, end=' ')
            answer = input()
            if answer in self.plugins.keys():
                # Write that plugin activated
                pinfo = json.loads(open(f'plugins/{answer}/info.json').read())
                pinfo['status'] = 'yes'
                with open(f'plugins/{answer}/info.json', 'w') as f:
                    f.write(json.dumps(pinfo))
                console.print(
                    f'[white]Plugin[/] [cyan]{answer}[/] [white]activated[/]')
                # Activate plugin
                pluginModule = importlib.import_module(f'plugins.{answer}.plugin')
                pluginModule.init(AppData)
                m = []
                for name in pluginModule.modulesNames:
                    if name in libs.keys():
                        m.append(libs[name])

                self.p = pluginModule.p(AppData, m)
                self.activatedPlugins[pluginModule.NAME] = self.p
                self.p.activate()
                break

            elif answer == ALL:
                for (name, info) in self.plugins.items():
                    pinfo = json.loads(
                        open(f'plugins/{name}/info.json').read())
                    pinfo['status'] = 'yes'
                    with open(f'plugins/{name}/info.json', 'w') as f:
                        f.write(json.dumps(pinfo))
                    # Activate plugin
                    pluginModule = importlib.import_module(f'plugins.{name}.plugin')
                    pluginModule.init(AppData)
                    m = []
                    for name in pluginModule.modulesNames:
                        if name in libs.keys():
                            m.append(libs[name])
                    self.p = pluginModule.p(AppData, m)
                    self.activatedPlugins[pluginModule.NAME] = self.p
                    self.p.activate()
                    self.update()
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
                if answer in self.activatedPlugins.keys():
                    pinfo = json.loads(open(f'plugins/{answer}/info.json').read())
                    pinfo['status'] = 'no'
                    with open(f'plugins/{answer}/info.json', 'w') as f:
                        f.write(json.dumps(pinfo))
                    # Deactivate
                    del self.activatedPlugins[answer]
                    console.print(
                        f'[white]Plugin[/] [cyan]{answer}[/] [white]deactivated[/]')
                    self.update()
                    
                else:
                    console.print('[white]This plugin is already deactivated![/]')
                break

            elif answer == ALL:
                for (name, info) in plugins.items():
                    pinfo = json.loads(
                        open(f'plugins/{name}/info.json').read())
                    pinfo['status'] = 'no'
                    with open(f'plugins/{name}/info.json', 'w') as f:
                        f.write(json.dumps(pinfo))
                    # Deactivate
                    del self.activatedPlugins[name]
                    self.update()
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
        developer_tree = Tree(
            '[cyan]ITTOOLS[/cyan] [white]developers:[/white]')
        for developer in DEVELOPERS_LIST:
            developer_tree.add(f'[blue]{developer}[/blue]')

        console.print(developer_tree)


def startApp():
    #os.system('cls||clear')
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
