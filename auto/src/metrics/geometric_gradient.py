from src import terms, rates, models, util

import json

"""
    VP: Total value
    B: Base value
    J: Geometric gradient
    N: N term
    Ip: Interest rates.Rate
"""


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
        self.VP = self.B * p1 * p2
        return util.format_money(self.VP, decimal=self.decimal)

    @property
    def _B(self):
        p1 = 1 / (self.J - self.Ip)
        p2 = (((1 + self.J.real) / (1 + self.Ip.real)) ** self.N) - 1
        self.B = self.VP / (p1 * p2)
        return util.format_money(self.B, decimal=self.decimal)

    @property
    def _B_w_VP_Ip_J(self):
        tmp = self.Ip - self.J
        self.B = self.VP * tmp
        return util.format_money(self.B, decimal=self.decimal)


# ip = rates.rates.RateOperation.simple(
#     rates.Rate=rates.Rate(effective=4.20, nper=1, d_nper=12),
#     source=rates.rates.RateOperation.EFFECTIVE,
#     target=rates.rates.RateOperation.IPV,
# )

# term = terms.Terms.many(term=terms.Terms.MONTH, years=3)yt76hy8

# gg = GeometricGradient(VP=200000000, J=0.20, N=360, Ip=ip["result"].value)
# print("B", gg._B_w_VP_Ip_J)

# print(util.format_money(gg.get_n_fee(360), 3))

# print(json.dumps(gg.get_totals(), indent=2))
