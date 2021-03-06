from typing import Any, Dict
from src.client.question import Question, QuestionKind
from src.models import Percentage
from src.rates import Rate, RateOperation
from src.client.flow.topics import form as topic_form


class FormRateTopic(topic_form.Form):
    def __init__(self, last_state: Question):
        super().__init__(title="Que deseas hacer?", last=last_state, back_title="Atras")

        self.rates: Dict[str, FormRate] = {}

        add_rate = Question(kind=QuestionKind.LINK, process=self.__add_rate)
        get_rates = Question(kind=QuestionKind.FINAL, process=self._get_rates)

        self.bidirect(target=add_rate, alias="Agregar tasa")
        self.bidirect(target=get_rates, alias="Ver tasas")

        self.run_form()
    
    def _add_named_rate(self, name):
        formed_rate = FormRate()
        self.rates[name] = "%s -> %s\n%s -> %s\n" % (
            formed_rate.rate_type, 
            formed_rate.value, 
            formed_rate.target, 
            formed_rate.rate
        )
    
    def __add_rate(self):
        rate = Question(
            kind=QuestionKind.ONLY_INPUT,
            content=("name", "Nombre:", str),
            process=self._add_named_rate,
        )
        rate.ask()
    
    def _get_rates(self):
        rates = ["%s\n%s" % (f"{'-'*10} {name} {'-'*10}", self.rates.get(name)) for name in self.rates]
        temp = Question(
            kind=QuestionKind.SELECT,
            content="Tasas\n%s\n%s" % ('#'*30, "\n".join(rates)),
        )
        temp.add_edge(target=self.main, alias="Atras")
        temp.ask()



class FormRate:
    def __init__(self):

        self.value = None
        self.rate_type = None
        self.target = None
        self.rate: float = None

        set_value = Question(
            kind=QuestionKind.INPUT,
            content=("value", "Valor:", float),
            process=self.set_value,
        )
        set_rate_type = Question(
            kind=QuestionKind.INPUT,
            content=(
                "value",
                "Tipo (Escriba en el formato de letras {n.p.{a,v}, e.a, p.{a,v}}):",
                str,
            ),
            process=self.set_rate_type,
        )
        set_target = Question(
            kind=QuestionKind.INPUT,
            content=(
                "value",
                "Tipo a convertir (Escriba en el formato de letras {n.p.{a,v}, e.a, p.{a,v}}):",
                str,
            ),
            process=self.set_target,
        )
        build = Question(kind=QuestionKind.FINAL, process=self.convert_rate)

        set_value.add_edge(target=set_rate_type)
        set_rate_type.add_edge(target=set_target)
        set_target.add_edge(target=build)

        set_value.ask()

    def set_value(self, value: float):
        self.value = value

    def set_rate_type(self, value: str):
        self.rate_type = value

    def set_target(self, value: str):
        self.target = value

    def _get_period(self, value: str) -> int:
        result = 1
        value = value.lower().split()[0]
        letters = value.split(".")
        periods = {
            "m": 12,
            "t": 4,
            "s": 2,
            "b": 6,
            "q": 24,
            "sm": 53,
            "d": 365,
        }

        if len(letters) == 2:
            if not value == "e.a":
                result = periods[letters[0]]
        elif len(letters) == 3:
            if letters[0] == "n":
                result = periods[letters[1]]

        return result

    def _get_rate_type(self, value: str) -> RateOperation:
        result = None
        value = value.lower().split()[0]
        letters = value.split(".")
        if len(letters) == 2:
            if value == "e.a":
                result = RateOperation.EFFECTIVE
            else:
                if letters[1] == "a":
                    result = RateOperation.IPA
                elif letters[1] == "v":
                    result = RateOperation.IPV
        elif len(letters) == 3:
            if letters[0] == "n":
                if letters[2] == "a":
                    result = RateOperation.NOMINAL_A
                elif letters[2] == "v":
                    result = RateOperation.NOMINAL_V

        return result

    def _get_rate(self, rate_type: RateOperation) -> Dict[str, Any]:
        result = {}
        rates = {
            RateOperation.NOMINAL_A: "nominal",
            RateOperation.EFFECTIVE: "effective",
            RateOperation.NOMINAL_V: "nominal",
            RateOperation.IPA: "ipa",
            RateOperation.IPV: "ipv",
        }
        result[rates[rate_type]] = self.value
        return result

    def convert_rate(self):
        nper = self._get_period(value=self.rate_type)
        dnper = self._get_period(value=self.target)
        source_type = self._get_rate_type(value=self.rate_type)
        target_type = self._get_rate_type(value=self.target)

        source_data = self._get_rate(rate_type=source_type)

        source_data["nper"] = nper
        source_data["d_nper"] = dnper

        if nper == dnper or RateOperation.EFFECTIVE in [source_type, target_type]:
            result = RateOperation.simple(
                rate=Rate(**source_data), source=source_type, target=target_type
            )
        else:
            result = RateOperation.complex(
                rate=Rate(**source_data), source=source_type, target=target_type
            )

        tmp: Percentage = result["result"]

        self.rate = tmp.value
