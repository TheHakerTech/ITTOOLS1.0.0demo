# -*- coding: utf-8 -*-
from __future__ import annotations
from rich.console import Console
import requests
import os.path
import zipfile
import re

import os
# Import system ptools
import libs.ptools as ptools
# Create globals
AppData = None
console = Console()

modulesNames = ['errors', 'commandManager', 'network']
NAME = 'installer'

# Init fuction init AppData
def init(data):
    global AppData
    AppData = data

class NotAllModulesConnected(Exception): pass
    

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

        AppData.groups.list['System tools'].addCommand([self.commandManager.Command('download', self.download, 'Download plugin')])
        AppData.groups.update()

    def download(self) -> bool:
        self.errors.Functions.debug('Invoked function download')
        # Cheack network connection
        if self.network.networkCheck():
            while True:
                console.print('[white]Enter <developer_name_on_github>\<plugin_name> (e - cancel)')
                console.print('[red]>[/] ', end='')
                answer = input()
                # if answer if following pattern...
                if answer == '*':
                    break
                else:
                    if re.compile(r"""[A-Za-zА-Яа-яёЁ0-9]+\\[A-Za-zА-Яа-яёЁ0-9]+""").fullmatch(answer):
                        # if plugin is not downloaded...
                        repName = "ittoolplugin."+answer.split('\\')[1]
                        pluginName = answer.split('\\')[1]
                        developerName = answer.split('\\')[0]
                        if not os.path.exists(f'plugins/{repName}'):
                        
                            url = f"https://raw.githubusercontent.com/{developerName}/{repName}/main/info.json"
                            if self.network.networkConnectionCheck(url):
                                os.mkdir(f'plugins/{pluginName}')
                                # read info.json
                                response = requests.get(url)
                                with open(f'plugins/{pluginName}/info.json', 'wb') as file:
                                    file.write(response.content)
                                response = requests.get(f"https://raw.githubusercontent.com/{developerName}/{repName}/main/README.md")
                                with open(f'plugins/{pluginName}/README.md', 'wb') as file:
                                    file.write(response.content)
                                response = requests.get(f"https://raw.githubusercontent.com/{developerName}/{repName}/main/main.zip")
                                with open(f'plugins/{pluginName}/main.zip', 'wb') as file:
                                    file.write(response.content)
                                # Unpack zip
                                with zipfile.ZipFile(f'plugins/{pluginName}/main.zip', mode='a') as file:
                                    file.extractall(path=f'plugins/{pluginName}')
                                os.remove(f'plugins/{pluginName}/main.zip')
                                console.print('[green]Succes')
                                break
                                
                            else:
                                console.print('[red]Unknow rep or user name[/]')
                        else:
                            if os.path.exists(f'plugins/{pluginName}/info.json') and os.path.exists(f'plugins/{pluginName}/README.md') and os.path.exists(f'plugins/{pluginName}/plugin.py'):
                                pass
                            else:
                                console.print('[red]Plugin is uncorrect! Reinstall it? (y/n)')
                                while True:
                                    console.print('[red]>[/] ', end=' ')
                                    answer = input()
                                    if answer.lower() == 'y':
                                        # Reinstall
                                        pass
                                    elif answer.lower() == 'n':
                                        console.print('You cancelled')
                                        break
                                    else:
                                        console.print('You have to answer y or n')
                                    
                    else:
                        console.print('[red]Uncorrect format[/]')
                
        else:
            console.print('[red]You have not network connection![/]')



