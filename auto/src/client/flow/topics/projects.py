from typing import Any, List
from src.client.question import Question, QuestionKind, QuestionEdge

from src.metrics.bussiness import Project


class FormProject:
    def __init__(self, last_state: Question):

        self.amounts = []

        confirm = Question(
            kind=QuestionKind.LINK,
            process=self.build_project,
        )

        add_id = Question(
            kind=QuestionKind.INPUT,
            content=("id", "Indique ID del proyecto:", str),
            process=self.set_id,
        )

        add_to_project = Question(
            kind=QuestionKind.SELECT, content="Que desea hacer en el proyecto?"
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

        add_id.add_edge(edge=QuestionEdge(target=add_to_project))
        add_to_project.add_edge(
            edge=QuestionEdge(target=add_amount, alias="Agregar monto")
        )
        add_to_project.add_edge(
            edge=QuestionEdge(
                target=add_multiple_amount, alias="Agregar montos iguales"
            )
        )
        add_to_project.add_edge(edge=QuestionEdge(target=add_tco, alias="Agregar TCO"))
        add_to_project.add_edge(edge=QuestionEdge(target=confirm, alias="Confirmar"))

        add_amount.add_edge(edge=QuestionEdge(target=add_to_project))
        add_multiple_amount.add_edge(edge=QuestionEdge(target=add_to_project))
        add_tco.add_edge(edge=QuestionEdge(target=add_to_project))
        confirm.add_edge(edge=QuestionEdge(target=last_state))

        add_id.ask()

    def set_id(self, id: str):
        self.id = id

    def set_amount(self, value: float):
        self.amounts.append(value)

    def set_amounts(self, quantity: int, amount: float):
        self.amounts.extend(quantity * [amount])

    def set_tco(self, value: str):
        self.tco = value

    def build_project(self) -> Project:
        self.project = Project(amounts=self.amounts, TCO=self.tco, id=self.id)
        return self.project
