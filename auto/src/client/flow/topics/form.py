from typing import Callable
from src.client.question import Question, QuestionKind


class Form:
    def __init__(
        self,
        title: str,
        back_title: str = "",
        last: Question = None,
        back_process: Callable = lambda: None,
        extra: Callable = None,
    ):
        self.main = Question(kind=QuestionKind.SELECT, content=title, extra=extra)
        self.back = Question(kind=QuestionKind.LINK, process=back_process)
        self.main.add_edge(target=self.back, alias=back_title)

        if last is not None:
            self.back.add_edge(target=last)

    def direct(self, target: Question, alias: str = None):
        self.main.add_edge(target=target, alias=alias)

    def bidirect(self, target: Question, alias: str = None, alias_second: str = None):
        self.main.add_edge(target=target, alias=alias)
        target.add_edge(target=self.main, alias=alias_second)

    def run_form(self):
        self.main.ask()
