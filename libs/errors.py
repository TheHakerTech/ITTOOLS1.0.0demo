# -*- coding: utf-8 -*-
from rich.console import Console
# Create globals
AppData = None
console = Console()
NAME = 'errors'
# Init fuction init AppData
def init(data):
    global AppData
    AppData = data
    
class Functions:
    # Init debug fuction
    @staticmethod
    def debug(text):
        console.log('[cyan]DEBUG[/]: {0}'.format(text))
    @staticmethod
    def error(text):
        console.log('[red]ERROR[/]: {0}'.format(text))

class SystemSpecialErrors(Exception): pass
class Restart(SystemSpecialErrors): pass
class Exit(SystemSpecialErrors): pass