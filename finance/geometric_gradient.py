import json
from models import Percentage


"""
    VP: Total value
    B: Base value
    J: Geometric gradient
    N: N term
    Ip: Interest rate
"""


class GeometricGradient:
    def __init__(
        self,
        B: float = None,
        J: float = None,
        N: int = None,
        Ip: float = None,
        VP: float = None,
    ):
        self.B = B
        self.J = Percentage(J)
        self.N = N
        self.Ip = Percentage(Ip)
        self.VP = VP
        self.decimal = 3
        self.fees = dict()
        self.balances = dict()
        self.interests = dict()
        self.payments = dict()

    def format(self, value: float):
        expression = f":,.{self.decimal}f"
        return ("{" + expression + "}").format(value)

    def get_n_fee(self, n):
        if n in self.fees:
            result = self.fees[n]
        elif n == 1:
            result = self.B
        else:
            result = self.get_n_fee(n - 1) * (1 + self.J.real)
        self.fees[n] = result
        return result

    def get_n_interest(self, n):
        self.interests[n] = self.get_n_balance(n - 1) * self.Ip.real
        return self.interests[n]

    def get_n_payment(self, n):
        self.payments[n] = self.get_n_fee(n) - self.get_n_interest(n)
        return self.payments[n]

    def get_n_balance(self, n):
        if n in self.balances:
            result = self.balances[n]
        elif n == 0:
            result = self.VP
        else:
            result = self.get_n_balance(n - 1) - self.get_n_payment(n)
        self.balances[n] = result
        return result

    def round_values(self, values):
        if type(values) == dict:
            for key in values:
                values[key] = round(values[key], self.decimal)
        elif type(values) == list:
            for n in range(len(values)):
                values[n] = round(values[n], self.decimal)

    def get_totals(self):
        last_metrics = {
            "interest": self.get_n_interest(self.N),
            "payment": self.get_n_payment(self.N),
            "fee": self.get_n_fee(self.N),
            "balance": self.get_n_balance(self.N),
        }
        total = {
            "interest": sum(self.interests.values()),
            "payments": sum(self.payments.values()),
            "fees": sum(self.fees.values()),
        }
        self.round_values(last_metrics)
        self.round_values(total)
        return {
            "last_metrics": last_metrics,
            "total_metrics": total,
        }

    @property
    def _VP(self):
        p1 = 1 / (self.J - self.Ip)
        p2 = (((1 + self.J.real) / (1 + self.Ip.real)) ** self.N) - 1
        print(p2)
        self.VP = self.B * p1 * p2
        return self.format(self.VP)

    @property
    def _B(self):
        p1 = 1 / (self.J - self.Ip)
        p2 = (((1 + self.J.real) / (1 + self.Ip.real)) ** self.N) - 1
        self.B = self.VP / (p1 * p2)
        return self.format(self.B)


gg = GeometricGradient(B=1320000, J=2, N=3 * 12, Ip=2.2104)
print("VP", gg._VP)

print(gg.format(gg.get_n_fee(4)))

print(json.dumps(gg.get_totals()))
