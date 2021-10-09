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

    def add_VP(self, value: Union[Metric, float]):
        self.VPs.append(value.VP if type(value) == Metric else value)
        return self.VPs

    def add_VF(self, value: Union[Metric, float]):
        self.VFs.append(value.VF if type(value) == Metric else value)
        return self.VFs

    def add(self, value: Metric):
        self.add_VF(value)
        self.add_VP(value)
        return self

    @property
    def _VPs(self):
        return sum(self.VPs)

    @property
    def _VFs(self):
        return sum(self.VFs)
