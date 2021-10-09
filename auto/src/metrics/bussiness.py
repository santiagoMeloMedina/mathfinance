from typing import Any, List

import numpy_financial as npf

from src import models
from src.metrics import money_by_time as mbt


class Project:
    def __init__(self, amounts: List[float] = [], TCO: float = 0, id: Any = None):
        self.amounts = amounts
        self.TCO = models.Percentage(TCO)
        self.__set_VDT(amounts)
        self.id = id

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


class MutuallyEsclusive:
    def __init__(self, projects: List[Project] = []):
        self.projects = projects

    def add_project(self, project: Project):
        self.projects.append(project)

    def __is_greater_viable(self, project_a: Project, project_b: Project) -> bool:
        pass

    @property
    def _rank(self):
        vps = sorted(self.projects, key=lambda x: x._VPN)
        tirs = sorted(self.projects, key=lambda x: x._TIR)

        self.ranking = []

        vpn_i, tir_i = 0, 0
        while vpn_i < len(vps) or tir_i < len(tirs):
            if vpn_i == len(vps):
                self.ranking.append(tirs[tir_i])
                tir_i += 1
            elif tir_i == len(tirs):
                self.ranking.append(vps[vpn_i])
                vpn_i += 1
            else:
                if vps[vpn_i].id == tirs[tir_i].id:
                    self.ranking.append(vps[vpn_i])
                    vpn_i += 1
                    tir_i += 1
