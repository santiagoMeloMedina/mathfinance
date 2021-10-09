from typing import List

import numpy_financial as npf

from src import models
from src.metrics import money_by_time as mbt


class Project:
    def __init__(self, amounts: List[float] = [], TCO: float = 0):
        self.amounts = amounts
        self.TCO = models.Percentage(TCO)
        self.__set_VDT(amounts)

    def reset(self):
        self.amounts = []
        self.VDT = []

    def __set_VDT(self, amounts: List[float]):
        self.VDT = mbt.VDT()
        for i in range(1, len(amounts)):
            amount = amounts[i]
            metric = mbt.Metric(Ip=self.TCO, VF=amount, N=i)
            metric._VP
            self.VDT.add(metric)

    @property
    def _N(self):
        tmp = len(self.amounts) - 1
        return max(tmp, 0)

    @property
    def _VPs(self):
        return self.VDT._VPs

    @property
    def _VFs(self):
        return self.VDT._VFs

    @property
    def _VPN(self) -> float:
        return self.amounts[0] + self._VPs

    @property
    def _TIR(self) -> models.Percentage:
        return models.Percentage(npf.irr(self.amounts) * 100)

    @property
    def _is_viable(self) -> bool:
        vpn_condition = self._VPN > 0
        tir_condition = self._TIR > self.TCO
        return vpn_condition and tir_condition

    def add_amount(self, value: float):
        self.amounts.append(value)
