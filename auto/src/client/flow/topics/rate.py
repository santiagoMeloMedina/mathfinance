from typing import Any, Dict
from src.client.question import Question, QuestionKind
from src.rates import Rate, RateOperation


class FormRate:
    def __init__(self):

        self.value = None
        self.rate_type = None
        self.target = None
        self.rate = None

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
        value = value.split()[0]
        letters = value.split(".")
        periods = {
            "m": 12,
            "t": 3,
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
        value = value.split()[0]
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

        self.rate = result["result"]
