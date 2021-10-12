from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple, Union
from enum import Enum
from src.client import console


def any_function(**kwargs: Any):
    pass


class QuestionKind(Enum):
    SELECT = "SELECT"
    INPUT = "INPUT"
    LINK = "LINK"
    FINAL = "FINAL"


class QuestionEdge:
    def __init__(self, target: Question, alias: str = None):
        self.target = target
        self.alias = alias


class Question:
    def __init__(
        self,
        kind: QuestionKind,
        content: Union[str, Tuple[str, str, Any], List[Tuple[str, str, Any]]] = None,
        process: Callable = any_function,
    ):
        self.kind = kind
        self.content = content
        self.edges: Dict[str, QuestionEdge] = {}
        self.process = process
        self.alias = {}

    def add_edge(self, target: Question, alias: str = ""):
        edge = QuestionEdge(target=target, alias=alias)
        self.edges[edge.target.__hash__] = edge
        self.alias[edge.alias] = edge.target.__hash__

    def run_select(self):
        def process_and_traverse(option: str):
            self.process()
            self.traverse(option=option)

        console.Console.get_options(
            question=self.content,
            options=[self.edges[option].alias for option in self.edges],
            action=process_and_traverse,
        )

    def run_input(self):
        result = {}
        if type(self.content) == tuple:
            param, txt, type_ = self.content
            tmp = console.Console.get_input(question=txt, type_=type_)
            result[param] = tmp
        else:
            for i in range(len(self.content)):
                param, txt, type_ = self.content[i]
                tmp = console.Console.get_input(question=txt, type_=type_)
                result[param] = tmp

        self.process(**result)
        self.traverse()

    def run_link(self):
        self.process()
        self.traverse()

    def run_final(self):
        self.process()

    def ask(self):
        runs = {
            QuestionKind.SELECT: self.run_select,
            QuestionKind.INPUT: self.run_input,
            QuestionKind.LINK: self.run_link,
            QuestionKind.FINAL: self.run_final,
        }
        runs[self.kind]()

    def traverse(self, option: str = None):
        if option is not None:
            id = self.alias[option]
            question = self.edges[id].target
            question.ask()
        else:
            question = list(self.edges.values())[0].target
            question.ask()
