from __future__ import annotations

import click
import os

from enum import Enum
from typing import Any, Callable, List


class StrColors(Enum):
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"

    @classmethod
    def colored(cls, text: str, color: StrColors) -> str:
        return f"{color.value}{text}"


class LinuxKeys(Enum):
    _LINUX_UP_ARROW = "\x1b[A"
    _LINUX_DOWN_ARROW = "\x1b[B"
    _LINUX_ENTER_ARROW = "\r"


class Sign:
    def __init__(
        self, options: List[str], key: str, select_sign: str, unselect_sign: str
    ):
        self.i = 0
        self.key = key
        self.select_sign = select_sign
        self.unselect_sign = unselect_sign
        self.options = options
        self.done = False
        self.signs = self.__generate_map(n=len(options))
        self.signs[self.__key(0)] = self.select_sign

    def __key(self, i: int = None):
        if i is None:
            i = self.i
        return f"{self.key}{i}"

    def __generate_map(self, n: int):
        result = {}
        for i in range(n):
            result[self.__key(i)] = self.unselect_sign
        return result

    def forward(self):
        self.signs[self.__key()] = self.unselect_sign
        self.i = (self.i + 1) % len(self.signs)
        self.signs[self.__key()] = self.select_sign

    def backwards(self):
        self.signs[self.__key()] = self.unselect_sign
        self.i = self.i - 1 if self.i - 1 >= 0 else len(self.signs) - 1
        self.signs[self.__key()] = self.select_sign

    def _done(self, action: Callable):
        def call_action():
            self.done = True
            action(self.options[self.i])

        return call_action


class Console:

    SELECTED = ">"
    UNSELECTED = "-"
    KEY = "o"

    @classmethod
    def get_options(cls, question: str, options: List[str], action: Callable):
        sign = Sign(
            options=options,
            key=cls.KEY,
            select_sign=cls.SELECTED,
            unselect_sign=cls.UNSELECTED,
        )
        while not sign.done:
            format_option = (
                lambda option, i, selected: StrColors.colored(
                    text="{" + f"{cls.KEY}{i}" + "}" + f" {str(option)}",
                    color=StrColors.RESET,
                )
                if selected
                else StrColors.colored(
                    text="{" + f"{cls.KEY}{i}" + "}" + f" {str(option)}",
                    color=StrColors.BLUE,
                )
            )
            options_text = "\n".join(
                [
                    format_option(option=options[i], i=i, selected=not sign.i == i)
                    for i in range(len(options))
                ]
            )
            os.system("clear")
            print(StrColors.colored(text=f"{question}\n", color=StrColors.BOLD))
            print(options_text.format(**sign.signs))
            cls.__key_choose(sign=sign, action=action)

    @classmethod
    def get_input(cls, question: str, type_: Any):
        os.system("clear")
        data = input(
            StrColors.colored(
                text=StrColors.colored(text=f"{question} ", color=StrColors.BOLD),
                color=StrColors.REVERSE,
            )
        )
        return type_(data)

    @classmethod
    def __key_choose(cls, sign: Sign, action: Callable):
        key = click.getchar()
        actions = {
            LinuxKeys._LINUX_ENTER_ARROW.value: sign._done(action),
            LinuxKeys._LINUX_UP_ARROW.value: sign.backwards,
            LinuxKeys._LINUX_DOWN_ARROW.value: sign.forward,
        }
        actions[key]()
