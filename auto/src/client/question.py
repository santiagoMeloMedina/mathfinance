from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple, Union
from enum import Enum
from src.client import console


def any_function(**kwargs: Any):
    pass


class QuestionKind(Enum):
    SELECT = "SELECT"
    INPUT = "INPUT"


class QuestionEdge:
    def __init__(self, target: Question, alias: str = None):
        self.target = target
        self.alias = alias


class Question:
    def __init__(
        self,
        id: str,
        kind: QuestionKind,
        content: Union[str, Tuple[str, str, Any], List[Tuple[str, str, Any]]],
        process: Callable = any_function,
    ):
        self.id = id
        self.kind = kind
        self.content = content
        self.edges: Dict[str, QuestionEdge] = {}
        self.process = process
        self.alias = {}

    def add_edge(self, edge: QuestionEdge):
        self.edges[edge.target.id] = edge
        self.alias[edge.alias] = edge.target.id

    def ask(self):
        result = {}
        if self.kind == QuestionKind.SELECT:
            console.Console.get_options(
                question=self.content,
                options=[self.edges[option].alias for option in self.edges],
                action=self.traverse,
            )
        elif self.kind == QuestionKind.INPUT:
            if type(self.content) == tuple:
                param, txt, type_ = self.content
                tmp = console.Console.get_input(
                    question=txt, type_=type_, action=self.traverse
                )
                result[param] = tmp
            else:
                for i in range(len(self.content)):
                    param, txt, type_ = self.content[i]
                    tmp = console.Console.get_input(
                        question=txt,
                        type_=type_,
                        action=self.traverse,
                        call_action=i == len(self.content) - 1,
                    )
                    result[param] = tmp

        self.process(**result)

    def traverse(self, option: str = None):
        if option is not None:
            id = self.alias[option]
            question = self.edges[id].target
            question.ask()
        else:
            question = list(self.edges.values())[0].target
            question.ask()
