import pytest

_MOCK_METRICS = {"Ip": 20, "VF": 400, "VP": 277.8, "N": 2}


@pytest.mark.unit
def test_get_correct_vp():
    from src.metrics import money_by_time as subject

    metrics_mock = _MOCK_METRICS.copy()
    metrics_mock["VP"] = 0

    metric = subject.Metric(**metrics_mock)

    assert round(metric._VP, 1) == _MOCK_METRICS["VP"]


@pytest.mark.unit
def test_get_correct_vf():
    from src.metrics import money_by_time as subject

    metrics_mock = _MOCK_METRICS.copy()
    metrics_mock["VF"] = 0

    metric = subject.Metric(**metrics_mock)

    assert round(metric._VF, 1) == _MOCK_METRICS["VF"]


@pytest.mark.unit
def test_get_correct_n():
    from src.metrics import money_by_time as subject

    metrics_mock = _MOCK_METRICS.copy()
    metrics_mock["N"] = 0

    metric = subject.Metric(**metrics_mock)

    assert round(metric._N, 1) == _MOCK_METRICS["N"]
