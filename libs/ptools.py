# -*- codinbg: utf-8 -*-
from __future__ import annotations

PLUGIN_FILES = {'plugin.py':None, 'info.json':None, 'README.md':None}

class Plugin:
    def __init__(
        self,
        data,
        modules: list = []
    ) -> Plugin:
        self.AppData = data
        self.modules = modules # There are modules which we need to connect
        # Connect
        self.connectModules()

    def connectModules(self) -> None:
        for module in self.modules:
            self.__dict__[module.NAME] = module