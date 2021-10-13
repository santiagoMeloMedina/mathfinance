from typing import Callable, Dict, List, Set, Tuple
from src import models


class GeometricGradient:
    def __init__(
        self,
        B: float = None,
        J: float = None,
        N: int = None,
        Ip: float = None,
        VP: float = None,
        decimal: int = 3,
    ):
        """
        VP: Total value
        B: Base value
        J: Geometric gradient
        N: N term
        Ip: Interest rates.Rate
        """
        self.B = B
        self.J = models.Percentage(J)
        self.N = N
        self.Ip = models.Percentage(Ip)
        self.VP = VP
        self.decimal = decimal
        self.new_system()

    def new_system(self):
        self.fees = dict()
        self.balances = dict()
        self.interests = dict()
        self.payments = dict()

    def _fee(self, n):
        if n in self.fees:
            result = self.fees[n]
        elif n == 1:
            result = self.B
        else:
            result = self._fee(n - 1) * (1 + self.J.real)
        self.fees[n] = result
        return result

    def _interest(self, n):
        self.interests[n] = self._balance(n - 1) * self.Ip.real
        return self.interests[n]

    def _payment(self, n):
        self.payments[n] = self._fee(n) - self._interest(n)
        return self.payments[n]

    def _balance(self, n):
        if n in self.balances:
            result = self.balances[n]
        elif n == 0:
            result = self.VP
        else:
            result = self._balance(n - 1) - self._payment(n)
        self.balances[n] = result
        return result

    def round_values(self, values):
        if type(values) == dict:
            for key in values:
                values[key] = round(values[key], self.decimal)
        elif type(values) == list:
            for n in range(len(values)):
                values[n] = round(values[n], self.decimal)

    @property
    def _last_metrics(self):
        last_metrics = {
            "interest": self._interest(self.N),
            "payment": self._payment(self.N),
            "fee": self._fee(self.N),
            "balance": self._balance(self.N),
        }
        self.round_values(last_metrics)
        return last_metrics

    @property
    def get_totals(self):
        self._last_metrics
        total = {
            "interest": sum(self.interests.values()),
            "payments": sum(self.payments.values()),
            "fees": sum(self.fees.values()),
        }
        self.round_values(total)
        return total

    def _VP(self):
        p1 = 1 / (self.J - self.Ip)
        p2 = (((1 + self.J.real) / (1 + self.Ip.real)) ** self.N) - 1
        self.VP = self.B * p1 * p2
        return self.VP

    def _B(self):
        p1 = 1 / (self.J - self.Ip)
        p2 = (((1 + self.J.real) / (1 + self.Ip.real)) ** self.N) - 1
        self.B = self.VP / (p1 * p2)
        return self.B

    def _B_w_VP_Ip_J(self):
        tmp = self.Ip - self.J
        self.B = self.VP * tmp
        return self.B


class LinearGradient:
    def __init__(
        self,
        B: float = None,
        G: float = None,
        N: int = None,
        Ip: float = None,
        VP: float = None,
        VA: float = None,
        A_star: float = None,
        decimal: int = 3,
    ):
        """
        VP: Total value
        B: Base value
        G: Linear gradient
        N: N term
        Ip: Interest rates.Rate
        """
        self.B = B
        self.G = G
        self.N = N
        self.Ip = models.Percentage(Ip)
        self.VP = VP
        self.VA = VA
        self.A_star = A_star
        self.decimal = decimal
        self.new_system()

    def new_system(self):
        self.fees = dict()
        self.balances = dict()
        self.interests = dict()
        self.payments = dict()

    def _fee(self, n):
        if n in self.fees:
            result = self.fees[n]
        elif n == 1:
            result = self.B
        else:
            result = self._fee(n - 1) + self.G
        self.fees[n] = result
        return result

    def _interest(self, n):
        self.interests[n] = self._balance(n - 1) * self.Ip.real
        return self.interests[n]

    def _payment(self, n):
        self.payments[n] = self._fee(n) - self._interest(n)
        return self.payments[n]

    def _balance(self, n):
        if n in self.balances:
            result = self.balances[n]
        elif n == 0:
            result = self.VP
        else:
            result = self._balance(n - 1) - self._payment(n)
        self.balances[n] = result
        return result

    def round_values(self, values):
        if type(values) == dict:
            for key in values:
                values[key] = round(values[key], self.decimal)
        elif type(values) == list:
            for n in range(len(values)):
                values[n] = round(values[n], self.decimal)

    def _n_metrics(self, n: int):
        last_metrics = {
            "interest": self._interest(n),
            "payment": self._payment(n),
            "fee": self._fee(n),
            "balance": self._balance(n),
        }
        self.round_values(last_metrics)
        return last_metrics

    @property
    def _last_metrics(self):
        last_metrics = {
            "interest": self._interest(self.N),
            "payment": self._payment(self.N),
            "fee": self._fee(self.N),
            "balance": self._balance(self.N),
        }
        self.round_values(last_metrics)
        return last_metrics

    @property
    def get_totals(self):
        self._last_metrics
        total = {
            "interest": sum(self.interests.values()),
            "payments": sum(self.payments.values()),
            "fees": sum(self.fees.values()),
        }
        self.round_values(total)
        return total

    def _G(self):
        if all([val is not None for val in [self.Ip, self.N, self.A_star]]):
            tmp = 1 / self.Ip.real
            tmp -= self.N / (((1 + self.Ip.real) ** self.N) - 1)
            self.G = self.A_star / tmp
        return self.G if self.G else 0

    def _A_star(self):
        if all([val is not None for val in [self.Ip, self.N, self.G]]):
            tmp = 1 / self.Ip.real
            tmp -= self.N / (((1 + self.Ip.real) ** self.N) - 1)
            self.A_star = self.G * tmp
        return self.A_star if self.A_star else 0

    def _A_star_w_VA(self):
        if all([val is not None for val in [self.VA, self.B]]):
            self.A_star = self.VA - self.B
        return self.A_star if self.A_star else 0

    def _B(self):
        if all([val is not None for val in [self.VA, self.A_star]]):
            self.B = self.VA - self.A_star
        return self.B if self.B else 0

    def _VA_w_A(self):
        if all([val is not None for val in [self.B, self.A_star]]):
            self.VA = self.B + self.A_star
        return self.VA if self.VA else 0

    def _VA(self):
        if all([val is not None for val in [self.Ip, self.N, self.VP]]):
            tmp = ((1 + self.Ip.real) ** self.N) - 1
            tmp /= ((1 + self.Ip.real) ** self.N) * self.Ip.real
            self.VA = self.VP / tmp
        return self.VA if self.VA else 0

    def _VP(self):
        if all([val is not None for val in [self.Ip, self.N, self.VA]]):
            tmp = ((1 + self.Ip.real) ** self.N) - 1
            tmp /= ((1 + self.Ip.real) ** self.N) * self.Ip.real
            self.VP = self.VA * tmp
        return self.VP if self.VP else 0

    def solve(self, start: Callable):
        graph = {
            self._G: [self._A_star, self._A_star_w_VA],
            self._A_star: [self._G],
            self._A_star_w_VA: [self._VA],
            self._VA: [self._VP],
            self._VA_w_A: [self._A_star, self._A_star_w_VA],
            self._VP: [self._VA, self._VA_w_A],
            self._B: [
                self._A_star,
                self._A_star_w_VA,
                self._VA,
                self._VA_w_A,
            ],
        }

        def traverse(start: Callable, visited: Set[Callable]):
            print(start)
            children = graph[start]
            visited.add(start)
            for child in children:
                if child not in visited:
                    traverse(start=child, visited=visited)
            start()

        traverse(start=start, visited=set())
        return start()
