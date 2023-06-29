# -*- coding: utf-8 -*-
from __future__ import annotations
from rich.console import Console
import requests
import os.path
# Import system ptools
import libs.ptools as ptools
# Create globals
AppData = None
console = Console()

modulesNames = ['errors', 'commandManager']
NAME = 'installer'

# Init fuction init AppData
def init(data):
    global AppData
    AppData = data

class NotAllModulesConnected(Exception): pass

def download(url, path='plugins'):
    if path == None:
        response = requests.get(url)
        open(filename, "wb").write(response.content)
    else:
        if os.path.exists(path):
            if os.path.exists(f"{path}\{filename}"):
                os.remove(f"{path}\{filename}")
            response = requests.get(url)
            open(filename, "wb").write(response.content)

    filename = 

    

class p(ptools.Plugin):
    def __init__(
        self,
        data,
        modules: list = ...
    ) -> p:
        super().__init__(data, modules)
        connectedModulesNames = [module.NAME for module in self.modules]
        if connectedModulesNames == modulesNames:
            self.errors.Functions.debug('Connected plugin {0}'.format(NAME))
        else:
            raise NotAllModulesConnected('Connected modules: {0} Not connected: {1}'.format(connectedModulesNames, modulesNames))
        
    def activate(self) -> bool:
        self.errors.Functions.debug('Plugin {0} activated'.format(NAME))

        AppData.groups.list['System tools'].addCommand([self.commandManager.Command('test', self.download, 'test plugin')])
        AppData.groups.update()

    def download(self) -> bool
        self.errors.Functions.debug('Invoked function download')

        console.print('[white]Enter plugin name (e - cancel)')
        while True:
            console.print('[red]>[/] ', end='')
            answer = input()
            pluginName = "ittoolplugin."+answer

        filename = 
