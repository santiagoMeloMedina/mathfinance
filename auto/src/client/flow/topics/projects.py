from typing import Any, List
from src.client.question import Question, QuestionKind, QuestionEdge

from src.metrics.bussiness import Project


class FormProject:
    def __init__(self, last_state: Question):

        self.amounts = []
        self.id = None
        self.tco = None

        self.main = Question(
            kind=QuestionKind.SELECT, content="Que desea hacer en el proyecto?"
        )
        self.back = Question(
            kind=QuestionKind.LINK,
            process=self.build_project,
        )
        self.main.add_edge(target=self.back, alias="Confirmar")

        add_id = Question(
            kind=QuestionKind.INPUT,
            content=("id", "Indique ID del proyecto:", str),
            process=self.set_id,
        )

        add_amount = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Escriba el monto $:", float),
            process=self.set_amount,
        )

        add_tco = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Escriba el tco%:", float),
            process=self.set_tco,
        )

        add_multiple_amount = Question(
            kind=QuestionKind.INPUT,
            content=[("quantity", "Cantidad:", int), ("amount", "Monto $:", float)],
            process=self.set_amounts,
        )

        add_id.add_edge(target=self.main)
        self.main.add_edge(target=add_amount, alias="Agregar monto")
        self.main.add_edge(target=add_multiple_amount, alias="Agregar montos iguales")
        self.main.add_edge(target=add_tco, alias="Agregar TCO")

        add_amount.add_edge(target=self.main)
        add_multiple_amount.add_edge(target=self.main)
        add_tco.add_edge(target=self.main)
        self.back.add_edge(target=last_state)

        add_id.ask()

    def set_id(self, id: str):
        self.id = id if id else None

    def set_amount(self, value: float):
        self.amounts.append(value)

    def set_amounts(self, quantity: int, amount: float):
        self.amounts.extend(quantity * [amount])

    def set_tco(self, value: str):
        self.tco = value

    def build_project(self) -> Project:
        self.project = Project(amounts=self.amounts, TCO=self.tco, id=self.id)
        return self.project
