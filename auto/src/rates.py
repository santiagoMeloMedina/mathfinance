from __future__ import annotations

from typing import Any, List, Tuple
from enum import Enum
from collections import deque

from src import models

class Rate:
    def __init__(
        self,
        ipa: float = 0,
        ipv: float = 0,
        nominal: float = 0,
        effective: float = 0,
        nper: int = 1,
        d_nper: int = 1,
    ):
        self.ipa = models.Percentage(ipa)
        self.ipv = models.Percentage(ipv)
        self.nominal = models.Percentage(nominal)
        self.effective = models.Percentage(effective)
        self.nper = nper
        self.d_nper = d_nper

    def __str__(self):
        return f"""
            IPA: {self.ipa}
            IPV: {self.ipv}
            NOMINAL: {self.nominal}
            EFFECTIVE: {self.effective}
            NPER: {self.nper}
            DNPER: {self.d_nper}
        """

    def to_percentage(self, value: float):
        return models.Percentage.from_real(value)

    def nominal_ipa(self) -> models.Percentage:
        self.ipa = self.to_percentage(self.nominal / self.nper)
        return self.ipa

    def nominal_ipv(self) -> models.Percentage:
        self.ipv = self.to_percentage(self.nominal / self.nper)
        return self.ipv

    def ipa_ipv(self) -> models.Percentage:
        value = self.ipa
        tmp = 1 - value.real
        self.ipv = self.to_percentage(value / tmp)
        return self.ipv

    def ipv_ipa(self) -> models.Percentage:
        value = self.ipv
        tmp = 1 + value.real
        self.ipa = self.to_percentage(value / tmp)
        return self.ipa

    def ipv_effective(self) -> models.Percentage:
        tmp = 1 + self.ipv.real
        self.effective = self.to_percentage((tmp ** self.nper) - 1)
        return self.effective

    def effective_ipv(self) -> models.Percentage:
        p1 = 1 + self.effective.real
        p2 = 1 / self.d_nper
        self.ipv = self.to_percentage((p1 ** p2) - 1)
        self.nper = self.d_nper
        return self.ipv

    def ipa_nominal(self) -> models.Percentage:
        self.nominal = self.to_percentage(self.ipa * self.nper)
        return self.nominal

    def ipv_nominal(self) -> models.Percentage:
        self.nominal = self.to_percentage(self.ipv * self.nper)
        return self.nominal


class RateOperation(Enum):
    IPA = "PERIODIC_ANTICIPATED"
    IPV = "PERIODIC_EXPIRED"
    NOMINAL_V = "NOMINAL_EXPIRED"
    NOMINAL_A = "NOMINAL_ANTICIPATED"
    EFFECTIVE = "ANUAL_EFFECTIVE"

    @classmethod
    def graph(cls, rate: Rate):
        return {
            cls.IPA: [(cls.NOMINAL_A, rate.ipa_nominal), (cls.IPV, rate.ipa_ipv)],
            cls.IPV: [
                (cls.NOMINAL_V, rate.ipv_nominal),
                (cls.IPA, rate.ipv_ipa),
                (cls.EFFECTIVE, rate.ipv_effective),
            ],
            cls.NOMINAL_A: [(cls.IPA, rate.nominal_ipa)],
            cls.NOMINAL_V: [(cls.IPV, rate.nominal_ipv)],
            cls.EFFECTIVE: [(cls.IPV, rate.effective_ipv)],
        }

    @classmethod
    def convert(cls, rate: Rate, source: RateOperation, target: RateOperation):
        G = cls.graph(rate)
        queue = deque([(source, [])])
        visited = set()
        while len(queue):
            current, path = queue.popleft()
            if current == target:
                return path
            visited.add(current)
            for child, value in G[current]:
                queue.append((child, path + [(current, value)]))
        return []

    @classmethod
    def use_path(cls, path: List[Tuple[RateOperation, Any]]):
        names, values = list(), list()
        for name, formula in path:
            values.append(formula())
            names.append(name.value)
        return (values[-1], " - ".join(names))

    @classmethod
    def simple(cls, rate: Rate, source: RateOperation, target: RateOperation):
        result, path = cls.use_path(
            cls.convert(rate=rate, source=source, target=target)
        )
        return {"result": result, "path": f"{path} - {target.value}"}

    @classmethod
    def complex(cls, rate: Rate, source: RateOperation, target: RateOperation):
        first, path1 = cls.use_path(
            cls.convert(rate=rate, source=source, target=RateOperation.EFFECTIVE)
        )

        second, path2 = cls.use_path(
            cls.convert(
                rate=Rate(effective=first.value, nper=rate.nper, d_nper=rate.d_nper),
                source=RateOperation.EFFECTIVE,
                target=target,
            )
        )

        return {"result": second, "path": f"{path1} - {path2} - {target.value}"}


# print(
#     RateOperation.simple(
#         Rate(nominal=18, nper=2),
#         source=RateOperation.NOMINAL_A,
#         target=RateOperation.IPV,
#     )
# )


# result = RateOperation.complex(
#     Rate(nominal=18, nper=2, d_nper=4),
#     source=RateOperation.NOMINAL_A,
#     target=RateOperation.IPV,
# )

# print(result["result"], result["path"])
