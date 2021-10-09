import pytest

from src import models

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
