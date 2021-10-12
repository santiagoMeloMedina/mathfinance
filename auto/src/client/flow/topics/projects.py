from src.client.flow.topics import form as topic_form
from src.client.question import Question, QuestionKind
from src.metrics.bussiness import Project


class FormProject(topic_form.Form):
    def __init__(self, last_state: Question):
        super().__init__(
            title="Que desea hacer en el proyecto?",
            last=last_state,
            back_title="Confirmar",
            back_process=self.build_project,
        )

        self.amounts = []
        self.id = None
        self.tco = None

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

        self.bidirect(target=add_amount, alias="Agregar monto")
        self.bidirect(target=add_multiple_amount, alias="Agregar montos iguales")
        self.bidirect(target=add_tco, alias="Agregar TCO")

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
