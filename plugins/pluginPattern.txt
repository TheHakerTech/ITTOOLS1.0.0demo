# -*- coding: utf-8 -*-
from __future__ import annotations
from rich.console import Console
# Import system ptools
import libs.ptools as ptools
# Create globals
AppData = None
console = Console()

modulesNames = ('errors', 'sqlCoder')

# Init fuction init AppData
def init(data):
    global AppData
    AppData = data

class p(ptools.Plugin):
    def __init__(
        self,
        data,
        modules: list = ...
    ) -> p:
        super().__init__(data, modules)