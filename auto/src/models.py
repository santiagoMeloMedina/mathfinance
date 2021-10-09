from __future__ import annotations


class Percentage:
    def __init__(self, value, decimals=10):
        self.value = value if value else 0
        self.decimals = decimals

    @classmethod
    def from_real(cls, real: float):
        return cls(real * 100)

    @property
    def real(self):
        return round(
            self.value / 100, self.decimals + 2
        )  # +2 Because /100 takes away two.

    def same(self, x):
        result = [self.real, x]
        if type(x) == Percentage:
            result[1] = x.real
        return result

    def __add__(self, x):
        val, x = self.same(x)
        return val + x

    def __sub__(self, x):
        val, x = self.same(x)
        return val - x

    def __mul__(self, x):
        val, x = self.same(x)
        return val * x

    def __truediv__(self, x):
        val, x = self.same(x)
        return val / x

    def __pow__(self, x):
        val, x = self.same(x)
        return val ** x

    def __str__(self):
        return f"{round(self.value, self.decimals)}%"

    def __eq__(self, x: Percentage):
        return self.real == x.real

    def __gt__(self, x: Percentage):
        return self.real > x.real

    def __ge__(self, x: Percentage):
        return self.real >= x.real

    def __lt__(self, x: Percentage):
        return self.real < x.real

    def __le__(self, x: Percentage):
        return self.real <= x.real
