from __future__ import annotations
from collections import deque
from typing import List
from src.metrics.project import Project


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
