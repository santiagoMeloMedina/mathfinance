from __future__ import annotations

from typing import Any, List, Union

import numpy_financial as npf

from collections import deque

from src import models
from src.metrics import money_by_time as mbt


class Project:
    def __init__(
        self,
        amounts: List[float] = [],
        TCO: Union[models.Percentage, float] = 0,
        id: Any = None,
    ):
        self.amounts = amounts
        self.TCO = TCO if type(TCO) == models.Percentage else models.Percentage(TCO)
        self.set_VDT()
        self.id = id
        self.set_initial_pay(amounts[0] if len(amounts) else 0)

    def set_initial_pay(self, value):
        self.initial_pay = abs(value)

    def reset(self):
        self.amounts = []
        self.vdt = []

    def set_VDT(self):
        self.vdt = mbt.VDT()
        for i in range(1, len(self.amounts)):
            amount = self.amounts[i]
            metric = mbt.Metric(Ip=self.TCO, VF=amount, N=i)
            metric._VP
            self.vdt.add(metric)

    @property
    def _N(self):
        tmp = len(self.amounts) - 1
        return max(tmp, 0)

    @property
    def _VPs(self):
        return self.vdt._VPs

    @property
    def _VFs(self):
        return self.vdt._VFs

    @property
    def _VPN(self) -> float:
        return self.amounts[0] + self._VPs

    @property
    def _TIR(self) -> models.Percentage:
        return models.Percentage(
            npf.irr(self.amounts) * 100, decimals=self.TCO.decimals
        )

    @property
    def _is_viable(self) -> bool:
        vpn_condition = self._VPN > 0
        tir_condition = self._TIR > self.TCO
        return vpn_condition and tir_condition

    def add_amount(self, value: float):
        self.amounts.append(value)
        if len(self.amounts) == 0:
            self.set_initial_pay(value)

    def __eq__(self, x: Union[Project, str]):
        if type(x) == Project:
            result = self.id == x.id
        elif type(x) == str:
            result = self.id == x
        return result


class Rank:
    def __init__(self, order: List[Project] = [], pair_rank: Rank = None):
        self.order = order
        self.data = deque(order)
        self.selected = set()
        self.pair_rank = pair_rank

    @property
    def _see(self):
        tmp = self.data.popleft()
        while tmp is not None and tmp.id in self.pair_rank.selected:
            if not self._is_empty:
                tmp = self.data.popleft()
            else:
                tmp = None
        if tmp is not None:
            self.data.appendleft(tmp)
        return tmp

    @property
    def _get(self):
        tmp = self.data.popleft()
        while tmp is not None and tmp.id in self.pair_rank.selected:
            if not self._is_empty:
                tmp = self.data.popleft()
            else:
                tmp = None
        if tmp is not None:
            self.selected.add(tmp.id)
        return tmp

    @property
    def not_selected(self) -> int:
        counter = 0
        for project in self.data:
            if project.id not in self.pair_rank.selected:
                counter += 1
        return counter

    @property
    def _is_empty(self):
        zero_to_select = self.not_selected == 0
        return len(self.data) == 0 or zero_to_select

    def __str__(self):
        return f"{self.order}"


class MutuallyEsclusive:
    def __init__(self, projects: List[Project] = []):
        self.projects = projects
        self.__rank()

    def add_project(self, project: Project):
        self.projects.append(project)
        self.__rank()

    @classmethod
    def comparison_project(cls, smaller: Project, greater: Project) -> Project:
        comparison = Project(TCO=greater.TCO)
        for i in range(max(len(smaller.amounts), len(greater.amounts))):
            sm, gt = smaller.amounts[i], greater.amounts[i]
            comparison.add_amount(gt - sm)
        comparison.set_VDT()
        return comparison

    @classmethod
    def is_greater_viable(cls, smaller: Project, greater: Project) -> bool:
        comparison = cls.comparison_project(smaller=smaller, greater=greater)
        return comparison._is_viable

    def __rank(self):
        vps_rank = Rank(sorted(self.projects, key=lambda x: x._VPN))
        tirs_rank = Rank(
            sorted(self.projects, key=lambda x: x._TIR), pair_rank=vps_rank
        )
        vps_rank.pair_rank = tirs_rank

        self.vps = vps_rank
        self.tirs = tirs_rank

        self.ranking: List[Project] = []

        while not vps_rank._is_empty or not tirs_rank._is_empty:
            if vps_rank._is_empty:
                self.ranking.append(tirs_rank._get)
            elif tirs_rank._is_empty:
                self.ranking.append(vps_rank._get)
            else:
                if vps_rank._see == tirs_rank._see:
                    self.ranking.append(vps_rank._get)
                else:
                    if self.is_greater_viable(
                        smaller=tirs_rank._see,
                        greater=vps_rank._see,
                    ):
                        self.ranking.append(vps_rank._get)
                    else:
                        self.ranking.append(tirs_rank._get)

    def budget_best_option(self, budget: float):
        """Returns data in the following order:
        1. Projects bought
        2. Projects not bought
        3. How muchc it needs in credit to buy (1)
        """
        acum = 0
        in_projects, out_projects = [], []
        for project in self.ranking:
            if acum < budget:
                acum += project.initial_pay
                in_projects.append(project)
            else:
                out_projects.append(project)
        return (in_projects, out_projects, acum - budget)