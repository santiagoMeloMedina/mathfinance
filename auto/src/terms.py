from __future__ import annotations
from enum import Enum


class Terms(Enum):
    MONTH = 12
    YEAR = 1
    QUATER = 4
    SEMESTER = 2
    BIMONTH = 6
    WEEK = 52
    FIFTEEN = 24
    DAY = 365

    @classmethod
    def many(cls, term: Terms, years: int):
        return years * term.value
