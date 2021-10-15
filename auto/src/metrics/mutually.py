from __future__ import annotations
from typing import List, Tuple
from src.metrics.project import Project
from src import util
from src.metrics.rank import Rank


class MutuallyEsclusive:
    def __init__(self, projects: List[Project] = []):
        self.projects = projects
        self.__rank()

    def add_project(self, project: Project):
        self.projects.append(project)
        self.__rank()

    def str_ranking(self):
        return "\n".join([str(pro) for pro in self.ranking])

    def budget_rank(self, budget: float):
        in_projects, out_projects, credit = self.budget_best_option(budget=budget)
        considered = "\n".join([str(pro) for pro in in_projects])
        return f"{considered}\nCredito: {util.format_money(value=credit, decimal=2)}"

    def print_vpns(self):
        print("\n".join([str(pro) for pro in self.vpns.order]))

    def print_tirs(self):
        print("\n".join([str(pro) for pro in self.tirs.order]))

    @classmethod
    def comparison_project(cls, smaller: Project, greater: Project) -> Project:
        comparison = Project(TCO=greater.TCO, reset=True)
        for i in range(max(len(smaller.amounts), len(greater.amounts))):
            sm, gt = smaller.amounts[i], greater.amounts[i]
            comparison.add_amount(gt - sm)
        comparison.set_VDT()
        return comparison

    @classmethod
    def is_greater_viable(cls, smaller: Project, greater: Project) -> bool:
        comparison = cls.comparison_project(smaller=smaller, greater=greater)
        return comparison._is_viable

    @classmethod
    def _TIRI(cls, smaller: Project, greater: Project) -> float:
        comparison = cls.comparison_project(smaller=smaller, greater=greater)
        return comparison._TIR

    @classmethod
    def _VPNI(cls, smaller: Project, greater: Project) -> float:
        comparison = cls.comparison_project(smaller=smaller, greater=greater)
        return comparison._VPN

    def __rank(self):
        vpns_rank = Rank(sorted(self.projects, key=lambda x: x._VPN, reverse=True))
        tirs_rank = Rank(
            sorted(self.projects, key=lambda x: x._TIR, reverse=True),
            pair_rank=vpns_rank,
        )
        vpns_rank.pair_rank = tirs_rank

        self.vpns = vpns_rank
        self.tirs = tirs_rank

        self.ranking: List[Project] = []

        while not vpns_rank._is_empty or not tirs_rank._is_empty:
            if vpns_rank._is_empty:
                self.ranking.append(tirs_rank._get)
            elif tirs_rank._is_empty:
                self.ranking.append(vpns_rank._get)
            else:
                if vpns_rank._see == tirs_rank._see:
                    self.ranking.append(vpns_rank._get)
                else:
                    if self.is_greater_viable(
                        smaller=tirs_rank._see,
                        greater=vpns_rank._see,
                    ):
                        self.ranking.append(vpns_rank._get)
                    else:
                        self.ranking.append(tirs_rank._get)

    def budget_best_option(
        self, budget: float
    ) -> Tuple[List[Project], List[Project], float]:
        """Returns data in the following order:
        1. Projects bought
        2. Projects not bought
        3. How much it needs in credit to buy (1)
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
