class Percentage:
    def __init__(self, value, decimals=10):
        self.value = value if value else 0
        self.decimals = decimals

    @property
    def real(self):
        return round(self.value / 100, self.decimals)

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
        return f"{self.value}%"
