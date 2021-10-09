from typing import List
from numpy import greater
import pytest

from src import models
from src.metrics.bussiness import Project

_MOCK_TCO = 20
_MOCK_VIABLE_TCO = 10

_MOCK_PROJECT_AMOUNTS = [
    -1000,
    100,
    400,
    400,
    500,
    100,
]

_MOCK_VPN = -126.09
_MOCK_TIR = 14.52

_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TCO = 10
_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE = [
    [
        -500000,
        200000,
        200000,
        200000,
        200000,
        200000,
    ],
    [
        -3200000,
        990000,
        990000,
        990000,
        990000,
        990000,
    ],
]
_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_VPNI = 294721.55
_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TIRI = 14.19


@pytest.mark.unit
def test_correct_vpn():
    from src.metrics import bussiness as subject

    project = subject.Project(amounts=_MOCK_PROJECT_AMOUNTS, TCO=_MOCK_TCO)

    assert round(project._VPN, 2) == _MOCK_VPN


@pytest.mark.unit
def test_correct_tir():
    from src.metrics import bussiness as subject

    project = subject.Project(amounts=_MOCK_PROJECT_AMOUNTS, TCO=_MOCK_TCO)

    tir_result = project._TIR
    tir_result.decimals = 2

    assert tir_result == models.Percentage(_MOCK_TIR)


@pytest.mark.unit
def test_project_is_viable():
    from src.metrics import bussiness as subject

    project = subject.Project(amounts=_MOCK_PROJECT_AMOUNTS, TCO=_MOCK_VIABLE_TCO)

    assert project._is_viable


@pytest.mark.unit
def test_rank_with_correct_flow():
    from src.metrics import bussiness as subject

    rank_1 = subject.Rank(
        [subject.Project([1, 2, 3], id="A"), subject.Project([2, 3, 4], id="B")]
    )
    rank_2 = subject.Rank(
        [
            subject.Project([3, 4, 5], id="C"),
            subject.Project([4, 5, 6], id="B"),
            subject.Project([4, 5, 6], id="A"),
        ],
        pair_rank=rank_1,
    )
    rank_1.pair_rank = rank_2

    assert rank_1._see == "A" and rank_2._see == "C"

    assert rank_1._get == "A" and rank_2._get == "C"

    assert len(rank_1.selected) == 1 and "A" in rank_1.selected
    assert len(rank_2.selected) == 1 and "C" in rank_2.selected

    assert rank_1.not_selected == 1
    assert rank_2.not_selected == 1

    assert rank_1._get == "B" and not rank_2._get == "B"


@pytest.mark.unit
def test_mutually_esclusive_vpni_and_tiri():
    from src.metrics import bussiness as subject

    projects: List[Project] = []
    for i in range(len(_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE)):
        project = subject.Project(
            amounts=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE[i],
            TCO=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TCO,
            id=str(i),
        )
        projects.append(project)

    comparison = subject.MutuallyEsclusive.comparison_project(
        smaller=projects[0], greater=projects[1]
    )

    assert round(comparison._VPN, 2) == _MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_VPNI
    assert round(comparison._TIR.value, 2) == _MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TIRI


@pytest.mark.unit
def test_mutually_esclusive_is_greater_comparison_viable():
    from src.metrics import bussiness as subject

    projects: List[Project] = []
    for i in range(len(_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE)):
        project = subject.Project(
            amounts=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE[i],
            TCO=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TCO,
            id=str(i),
        )
        projects.append(project)

    assert subject.MutuallyEsclusive.is_greater_viable(
        smaller=projects[0], greater=projects[1]
    )


@pytest.mark.unit
def test_mutually_esclusive_correct_ranking():
    from src.metrics import bussiness as subject

    projects: List[Project] = []
    for i in range(len(_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE)):
        project = subject.Project(
            amounts=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE[i],
            TCO=_MOCK_PROJECTS_MUTUALLY_ESCLUSIVE_TCO,
            id=str(i),
        )
        projects.append(project)

    mutually = subject.MutuallyEsclusive(projects)

    assert [pro.id for pro in mutually.ranking] == ["1", "0"]
