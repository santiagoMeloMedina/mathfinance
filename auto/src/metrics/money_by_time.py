import math
from typing import Any, List, Union

from src import models


class Metric:
    def __init__(
        self,
        Ip: Union[float, models.Percentage] = None,
        VF: float = None,
        VP: float = None,
        N: int = None,
        VA: float = None,
        VF_reinvested: float = None,
    ):
        self.Ip = Ip if type(Ip) == models.Percentage else models.Percentage(Ip)
        self.VF = VF
        self.VP = VP
        self.N = N
        self.VA = VA
        self.VF_reinvested = VF_reinvested

    def __have(self, values: List[Any]):
        return any([val is not None for val in values])

    @property
    def _Ip(self):
        if self.__have([self.VF, self.VP, self.N]):
            self.Ip = models.Percentage(((self.VF / self.VP) ** (1 / self.N)) - 1)
        return self.Ip if self.Ip else 0

    @property
    def _VF(self):
        if self.__have([self.VP, self.Ip, self.N]):
            self.VF = self.VP * (1 + self.Ip.real) ** self.N
        return self.VF if self.VF else 0

    def _VF_n(self, n: int):
        if self.__have([self.VF, self.Ip]):
            self.VF_reinvested = self.VF * (1 + self.Ip.real) ** n
        return self.VF_reinvested if self.VF_reinvested else 0

    @property
    def _VP(self):
        if self.__have([self.VF, self.Ip, self.N]):
            self.VP = self.VF / (1 + self.Ip.real) ** self.N
        return self.VP if self.VP else 0

    @property
    def _N(self):
        if self.__have([self.VF, self.VP, self.Ip]):
            f_p = math.log(self.VF / self.VP)
            i = math.log(1 + self.Ip.real)
            self.N = f_p / i
        return self.N if self.N else 0

    @property
    def _VA(self):
        if self.__have([self.Ip, self.N, self.VP]):
            tmp = ((1 + self.Ip.real) ** self.N) * self.Ip.real
            tmp = tmp / (((1 + self.Ip.real) ** self.N) - 1)
            self.VA = self.VP * tmp
        return self.VA if self.VA else 0


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

    def _VA(self, initial_pay: float = 0):
        Ip = self.metrics[0].Ip
        N = len(self.VPs)
        tmp = (((1 + Ip.real) ** N) * Ip.real) / (((1 + Ip.real) ** N) - 1)
        return (self._VPs + initial_pay) * tmp

    @property
    def _VFs(self):
        return sum(self.VFs)

    @property
    def _VFs_reinvested(self):
        return sum(self.VFs_reinvested)

    @property
    def _VPs_acum(self):
        return sum(self.VPs_acum)
