from typing import Any
import click
import os

_LINUX_UP_ARROW = "\x1b[A"
_LINUX_DOWN_ARROW = "\x1b[B"
_LINUX_ENTER_ARROW = "\r"


class Sign:
    def __init__(self, n: int, key: str, select_sign: str, unselect_sign: str):
        self.i = 0
        self.key = key
        self.select_sign = select_sign
        self.unselect_sign = unselect_sign
        self.done = False
        self.signs = self.__generate_map(n=n)
        self.signs[self.__key(0)] = self.select_sign

    def __key(self, i: int):
        return f"{self.key}{i}"

    def __generate_map(self, n: int):
        result = {}
        for i in range(n):
            result[self.__key(i)] = self.unselect_sign
        return result

    def forward(self):
        self.signs[self.__key(self.i)] = self.unselect_sign
        self.i = (self.i + 1) % len(self.signs)
        self.signs[self.__key(self.i)] = self.select_sign

    def backwards(self):
        self.signs[self.__key(self.i)] = self.unselect_sign
        self.i = self.i - 1 if self.i - 1 >= 0 else len(self.signs) - 1
        self.signs[self.__key(self.i)] = self.select_sign

    def _done(self):
        self.done = True


def print_options(options):
    key = "o"
    sign = Sign(n=len(options), key=key, select_sign=">", unselect_sign="-")
    while not sign.done:
        options_text = "\n".join(
            ["{" + f"{key}{i}" + "}" + f" {options[i]}" for i in range(len(options))]
        )
        os.system("clear")
        print(options_text.format(**sign.signs))
        key_choose(sign=sign)


def key_choose(sign: Sign):
    key = click.getchar()
    actions = {
        _LINUX_ENTER_ARROW: sign._done,
        _LINUX_UP_ARROW: sign.backwards,
        _LINUX_DOWN_ARROW: sign.forward,
    }
    actions[key]()


print_options(["mi titi patito", "chichi pototo", "tatiiiito"])
