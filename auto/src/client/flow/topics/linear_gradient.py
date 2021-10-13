from src.client.flow.topics import form as topic_form
from src.client.question import Question, QuestionKind
from src.metrics import gradients
from src import util
from src.models import Percentage


class FormLinearGradient(topic_form.Form):
    def __init__(self, last_state: Question):

        super().__init__(
            title="Que desea hacer?",
            last=last_state,
            back_title="Atras",
            extra=self.get_extra,
        )

        self.B = None
        self.G = None
        self.VP = None
        self.N = None
        self.Ip = None
        self.VA = None
        self.A_star = None

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
        set_VA = Question(
            kind=QuestionKind.INPUT,
            content=("value", "VA:", float),
            process=self.set_VA,
        )
        set_A_star = Question(
            kind=QuestionKind.INPUT,
            content=("value", "A*:", float),
            process=self.set_A_star,
        )

        get_VP = Question(
            kind=QuestionKind.FINAL,
            process=self.get_vp,
        )
        get_VA = Question(
            kind=QuestionKind.FINAL,
            process=self.get_va,
        )
        get_Astar = Question(
            kind=QuestionKind.FINAL,
            process=self.get_a_star,
        )
        get_G = Question(
            kind=QuestionKind.FINAL,
            process=self.get_g,
        )
        get_totals = Question(
            kind=QuestionKind.FINAL,
            process=self.get_totals,
        )
        get_n_metrics = Question(
            kind=QuestionKind.ONLY_INPUT,
            process=self.get_n_metrics,
            content=("n", "Momento #:", int),
        )

        self.bidirect(target=set_B, alias="Definir B")
        self.bidirect(target=set_G, alias="Definir G")
        self.bidirect(target=set_Ip, alias="Definir Ip")
        self.bidirect(target=set_N, alias="Definir N")
        self.bidirect(target=set_VP, alias="Definir VP")
        self.bidirect(target=set_VA, alias="Definir VA")
        self.bidirect(target=set_A_star, alias="Definir A*")

        self.direct(target=get_VP, alias="Obtener VP")
        self.direct(target=get_VA, alias="Obtener VA")
        self.direct(target=get_Astar, alias="Obtener A*")
        self.direct(target=get_G, alias="Obtener G")
        self.direct(target=get_totals, alias="Obtener totales")
        self.direct(target=get_n_metrics, alias="Obtener Momento")

        self.run_form()

    def get_extra(self):
        return " ".join(
            [
                f"{val[0]}: {str(val[1])}"
                for val in [
                    ("B", self.B),
                    ("G", self.G),
                    ("VP", self.VP),
                    ("N", self.N),
                    ("Ip", self.Ip),
                    ("VA", self.VA),
                    ("A*", self.A_star),
                ]
                if val[1] is not None
            ]
        )

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

    def set_VA(self, value: float):
        self.VA = value

    def set_A_star(self, value: float):
        self.A_star = value

    def build_linear_gradient(self):
        linear = gradients.LinearGradient(
            B=self.B, G=self.G, N=self.N, Ip=self.Ip, VP=self.VP
        )
        return linear

    def get_vp(self):
        linear = self.build_linear_gradient()
        VP_solved = util.format_money(value=linear.solve(start=linear._VP))
        temp = Question(kind=QuestionKind.SELECT, content=VP_solved)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def get_va(self):
        linear = self.build_linear_gradient()
        VA_solved = util.format_money(value=linear.solve(start=linear._VA))
        temp = Question(kind=QuestionKind.SELECT, content=VA_solved)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def get_a_star(self):
        linear = self.build_linear_gradient()
        A_star_solved = util.format_money(value=linear.solve(start=linear._A_star))
        temp = Question(kind=QuestionKind.SELECT, content=A_star_solved)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def get_g(self):
        linear = self.build_linear_gradient()
        G_solved = util.format_money(value=linear.solve(start=linear._G))
        temp = Question(kind=QuestionKind.SELECT, content=G_solved)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def get_totals(self):
        linear = self.build_linear_gradient()
        linear.solve(start=linear._VP)
        totals = linear.get_totals
        interest = util.format_money(totals["interest"])
        payments = util.format_money(totals["payments"])
        fees = util.format_money(totals["fees"])
        content = f"intereses: {interest}\nabonos: {payments}\ncuotas: {fees}"
        temp = Question(kind=QuestionKind.SELECT, content=content)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()

    def get_n_metrics(self, n: int):
        linear = self.build_linear_gradient()
        linear.solve(start=linear._VP)
        n_metrics = linear._n_metrics(n=n)
        interest = util.format_money(n_metrics["interest"])
        payments = util.format_money(n_metrics["payment"])
        fees = util.format_money(n_metrics["fee"])
        balance = util.format_money(n_metrics["balance"])
        content = f"intereses: {interest}\nabonos: {payments}\ncuotas: {fees}\nsaldo: {balance}"
        temp = Question(kind=QuestionKind.SELECT, content=content)
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()
