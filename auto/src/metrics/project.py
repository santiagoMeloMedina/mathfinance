from __future__ import annotations

import datetime
import random

from typing import Any, List, Tuple, Union
from dateutil.relativedelta import relativedelta


import numpy_financial as npf

from src import models
from src.metrics import money_by_time as mbt
from src import util


class Project:
    def __init__(
        self,
        amounts: List[float] = [],
        TCO: Union[models.Percentage, float] = 1,
        TVR_ip: Union[models.Percentage, float] = 1,
        id: Any = None,
        reset: bool = False,
    ):
        self.amounts = [] if reset else amounts
        self.TCO = TCO if type(TCO) == models.Percentage else models.Percentage(TCO)
        self.TVR_Ip = (
            TVR_ip if type(TVR_ip) == models.Percentage else models.Percentage(TVR_ip)
        )
        self.set_VDT()
        self.id = id if id is not None else f"random{random.randint(0, 2**31)}"
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
            metric = mbt.Metric(Ip=self.TCO, VF=amount, N=i, TVR_ip=self.TVR_Ip)
            metric._VP
            self.vdt.add(metric)

    @property
    def _VPN(self) -> float:
        result = 0
        if len(self.amounts):
            result = self.amounts[0] + self.vdt._VPs
        return result

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

    def __str__(self):
        return f"""
            Project '{self.id}'
            TCO: {self.TCO}
            VPN: {self._VPN}
            TIR: {self._TIR}
            VIABLE: {'SI' if self._is_viable else 'NO'}
        """


class Index(Project):

    DATE_VALUES = {"years": 12, "months": 30, "days": 24}

    def __init__(self, project: Project, TVR_ip: float = None):
        super().__init__(
            amounts=project.amounts,
            TCO=project.TCO,
            id=project.id,
            TVR_ip=TVR_ip,
        )

    @property
    def _IR(self):
        result = 0
        if self.initial_pay:
            result = (self._VPN / self.initial_pay) + 1
        return result

    @property
    def _BC(self):
        result = 0
        if self.initial_pay:
            result = self.vdt._VPs / self.initial_pay
        return result

    @property
    def _PR(self):
        result = 0

        def find_middle() -> Tuple[float, float, int]:
            i = 0
            while (
                i < len(self.vdt.VPs_acum) and self.vdt.VPs_acum[i] < self.initial_pay
            ):
                i += 1

            before, after = 0, 0
            if len(self.vdt.VPs_acum):
                before, after = self.vdt.VPs_acum[i - 1], self.vdt.VPs_acum[i]
            return (before, after, i)

        try:
            before, after, n = find_middle()
            if after - before:
                result = n + ((self.initial_pay - before) / (after - before))
        except:
            pass
        return result

    @property
    def _PR_format(self):
        result = {}
        tmp = self._PR
        temp = self.DATE_VALUES
        for key in temp:
            multiplier = temp[key]
            value = int(tmp)
            tmp = (tmp - value) * multiplier
            result[key] = value
        return result

    def future_date(self, date: datetime.datetime):
        pr_date = self._PR_format
        return date + relativedelta(**pr_date)

    @property
    def _TVR(self):
        tmp = 0
        try:
            if self.initial_pay:
                n = len(self.vdt.VFs_reinvested)
                tmp = ((self.vdt._VFs_reinvested / self.initial_pay) ** (1 / n)) - 1
        except:
            pass
        return models.Percentage(tmp * 100)

    @property
    def _CPE(self):
        return self.vdt._VPs + self.initial_pay

    @property
    def _CAUE(self):
        return self.vdt._VA(initial_pay=self.initial_pay)

    def __str__(self):
        amounts_str = "\n".join(
            [
                f"{i}. {util.format_money(self.amounts[i])}"
                for i in range(len(self.amounts))
            ]
        )
        return f"""\n{amounts_str}

            TCO: {self.TCO}
            VPN: {self._VPN}
            TIR: {self._TIR}
            VIABLE: {'SI' if self._is_viable else 'NO'}

            IR: {self._IR}
            BC: {self._BC}
            PR: {self._PR} {self._PR_format}
            TVR: {self._TVR}

            CPE: {util.format_money(self._CPE)}
            CAUE: {util.format_money(self._CAUE)}
        """
