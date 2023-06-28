from __future__ import annotations
from typing import Callable
from rich.console import Console
from rich.tree import Tree

AppData = None
console = Console()
NAME = 'commandManager'


def init(data):
    global AppData
    AppData = data


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
            group.print()

    def clear(self) -> None:
        self.list.clear()
        self.update()


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
        group_tree = Tree(f"[blue]{self.name}[/blue]")
        for (commandName, command) in self.list.items():
            group_tree.add(
                '[cyan]{0}[/] [white]- {1}[/]'.format(commandName, command.description))

        console.print(group_tree)


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
