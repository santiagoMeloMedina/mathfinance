import pytest

_MOCK_GET_VP_EXERCISE = {"B": 300000, "J": 1, "N": 72, "Ip": 2}
_MOCK_GET_VP_EXERCISE_RESULT = 15241310.36
_MOCK_GET_INTERESTS_EXERCISE_RESULT = 16171669.01
_MOCK_GET_PAYMENTS_EXERCISE_RESULT = 15241310.36
_MOCK_GET_FEES_EXERCISE_RESULT = 31412979.36

_MOCK_GET_BASE_EXERCISE = {"VP": 10000000, "J": 3, "N": 12, "Ip": 10}
_MOCK_GET_BASE_EXERCISE_RESULT = 1282735.78


@pytest.mark.unit
def test_get_vp():
    from src.metrics import geometric_gradient as subject

    gg = subject.GeometricGradient(**_MOCK_GET_VP_EXERCISE)

    assert round(gg._VP, 2) == _MOCK_GET_VP_EXERCISE_RESULT


@pytest.mark.unit
def test_get_balance_complete():
    from src.metrics import geometric_gradient as subject

    gg = subject.GeometricGradient(**_MOCK_GET_VP_EXERCISE)
    gg._VP

    last_metrics = gg._last_metrics

    assert round(last_metrics["balance"], 2) == 0.0


@pytest.mark.unit
def test_get_totals():
    from src.metrics import geometric_gradient as subject

    gg = subject.GeometricGradient(**_MOCK_GET_VP_EXERCISE)
    gg._VP

    totals = gg.get_totals

    assert round(totals["interest"], 2) == _MOCK_GET_INTERESTS_EXERCISE_RESULT
    assert round(totals["payments"], 2) == _MOCK_GET_PAYMENTS_EXERCISE_RESULT
    assert round(totals["fees"], 2) == _MOCK_GET_FEES_EXERCISE_RESULT


@pytest.mark.unit
def test_get_base():
    from src.metrics import geometric_gradient as subject

    gg = subject.GeometricGradient(**_MOCK_GET_BASE_EXERCISE)

    assert round(gg._B, 2) == _MOCK_GET_BASE_EXERCISE_RESULT
