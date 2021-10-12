from src.client.flow.topics import form as topic_form
from src.client.question import Question, QuestionKind
from src.metrics import gradients
from src import util


class FormLinearGradient(topic_form.Form):
    def __init__(self, last_state: Question):
        super().__init__(title="Que deseas hacer?", last=last_state, back_title="Atras")

        self.B = None
        self.G = None
        self.VP = None
        self.N = None
        self.Ip = None

        set_B = Question(
            kind=QuestionKind.INPUT, content=("value", "B:", float), process=self.set_B
        )
        set_G = Question(
            kind=QuestionKind.INPUT, content=("value", "G:", float), process=self.set_G
        )
        set_Ip = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Ip:", float),
            process=self.set_Ip,
        )
        set_N = Question(
            kind=QuestionKind.INPUT, content=("value", "N:", int), process=self.set_N
        )
        set_VP = Question(
            kind=QuestionKind.INPUT,
            content=("value", "VP:", float),
            process=self.set_VP,
        )

        get_VP = Question(
            kind=QuestionKind.FINAL,
            process=self.get_vp,
        )

        self.bidirect(target=set_B, alias="Definir B")
        self.bidirect(target=set_G, alias="Definir G")
        self.bidirect(target=set_Ip, alias="Definir Ip")
        self.bidirect(target=set_N, alias="Definir N")
        self.bidirect(target=set_VP, alias="Definir VP")
        self.bidirect(target=get_VP, alias="Obtener VP")

        self.main.ask()

    def set_B(self, value: float):
        self.B = value

    def set_G(self, value: float):
        self.G = value

    def set_VP(self, value: float):
        self.VP = value

    def set_N(self, value: int):
        self.N = value

    def set_Ip(self, value: float):
        self.Ip = value

    def get_vp(self):
        linear = self.build_linear_gradient()
        can_doit, reason = linear.can_VP
        if can_doit:
            content = util.format_money(linear._VP)
        else:
            content = reason

        temp = Question(kind=QuestionKind.SELECT, content=content)

        temp.add_edge(target=self.main, alias="Atras")

        temp.ask()

    def build_linear_gradient(self):
        linear = gradients.LinearGradient(
            B=self.B, G=self.G, N=self.N, Ip=self.Ip, VP=self.VP
        )
        return linear
