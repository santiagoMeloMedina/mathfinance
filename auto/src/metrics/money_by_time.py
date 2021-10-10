import math
from typing import List, Union

from src import models


class Metric:
    def __init__(
        self,
        Ip: Union[float, models.Percentage] = 0,
        VF: float = 0,
        VP: float = 0,
        N: int = 0,
    ):
        self.Ip = Ip if type(Ip) == models.Percentage else models.Percentage(Ip)
        self.VF = VF
        self.VP = VP
        self.N = N

    @property
    def _Ip(self):
        self.Ip = models.Percentage(((self.VF / self.VP) ** (1 / self.N)) - 1)
        return self.Ip

    @property
    def _VF(self):
        self.VF = self.VP * (1 + self.Ip.real) ** self.N
        return self.VF

    def _VF_n(self, n: int):
        self.VF_reinvested = self.VF * (1 + self.Ip.real) ** n
        return self.VF_reinvested

    @property
    def _VP(self):
        self.VP = self.VF / (1 + self.Ip.real) ** self.N
        return self.VP

    @property
    def _N(self):
        f_p = math.log(self.VF / self.VP)
        i = math.log(1 + self.Ip.real)
        self.N = f_p / i
        return self.N


class VDT:
    def __init__(self):
        self.VPs = []
        self.VFs = []
        self.VFs_reinvested = []
        self.VPs_acum = []
        self.metrics: List[Metric] = []

    def add_VP(self, value: Union[Metric, float]):
        self.VPs.append(value.VP if type(value) == Metric else value)
        self.set_VPs_acum()
        return self.VPs

    def add_VF(self, value: Union[Metric, float]):
        self.VFs.append(value.VF if type(value) == Metric else value)
        return self.VFs

    def set_VFs_reinvested(self):
        tmp = []
        for i in range(len(self.metrics)):
            metric = self.metrics[i]
            n = len(self.metrics) - (i + 1)
            tmp.append(metric._VF_n(n))
        self.VFs_reinvested = tmp
        return self.VFs_reinvested

    def add(self, value: Metric):
        self.add_VF(value)
        self.add_VP(value)
        self.metrics.append(value)
        self.set_VFs_reinvested()
        return self

    def set_VPs_acum(self):
        acum = 0
        tmp = []
        for vp in self.VPs:
            acum += vp
            tmp.append(acum)
        self.VPs_acum = tmp
        return self.VPs_acum

    @property
    def _VPs(self):
        return sum(self.VPs)

    @property
    def _VFs(self):
        return sum(self.VFs)

    @property
    def _VFs_reinvested(self):
        return sum(self.VFs_reinvested)

    @property
    def _VPs_acum(self):
        return sum(self.VPs_acum)
