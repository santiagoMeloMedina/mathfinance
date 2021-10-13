from src.client.flow.topics import form as topic_form
from src.client.flow.topics.rate import FormRate
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
            kind=QuestionKind.SELECT, content="Que desea hacer con la tasa?"
        )

        convert_tco = Question(kind=QuestionKind.LINK, process=self.set_convert_tco)

        add_tco_as_value = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Escriba el tco%:", float),
            process=self.set_tco_as_value,
        )

        add_multiple_amount = Question(
            kind=QuestionKind.INPUT,
            content=[("quantity", "Cantidad:", int), ("amount", "Monto $:", float)],
            process=self.set_amounts,
        )

        add_id.add_edge(target=self.main)

        self.bidirect(target=add_amount, alias="Agregar monto")
        self.bidirect(target=add_multiple_amount, alias="Agregar montos iguales")
        self.direct(target=add_tco, alias="Agregar TCO")

        add_tco.add_edge(target=add_tco_as_value, alias="Definir valor")
        add_tco.add_edge(target=convert_tco, alias="Convertir tasa")
        add_tco_as_value.add_edge(target=self.main)
        convert_tco.add_edge(target=self.main)

        add_id.ask()

    def set_id(self, id: str):
        self.id = id if id else None

    def set_amount(self, value: float):
        self.amounts.append(value)

    def set_amounts(self, quantity: int, amount: float):
        self.amounts.extend(quantity * [amount])

    def set_tco_as_value(self, value: str):
        self.tco = value

    def set_convert_tco(self):
        self.tco = FormRate().rate

    def build_project(self) -> Project:
        self.project = Project(amounts=self.amounts, TCO=self.tco, id=self.id)
        return self.project
