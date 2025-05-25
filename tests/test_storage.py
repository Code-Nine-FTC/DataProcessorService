from types import SimpleNamespace

import pytest

from src.schemas.alert import AlertData
from src.schemas.measure import MeasureData
from src.services.storage.business_logic import BusinessLogic


@pytest.mark.parametrize(
    ("signal", "measure_value", "alert_value", "expected"),
    [
        (">", 10, 5, True),
        ("<", 3, 7, True),
        ("==", 4, 4, True),
        (">=", 5, 5, True),
        ("<=", 2, 3, True),
        ("invalid", 1, 1, False),
    ],
)
def test_verify_alert(
    signal: str, measure_value: int, alert_value: int, expected: bool
) -> None:
    measure = SimpleNamespace(value=measure_value)
    type_alert = SimpleNamespace(math_signal=signal, value=alert_value)
    result = BusinessLogic.verify_alert(measure, type_alert)  # type: ignore
    assert result == expected


TYPE_ALERT_ID_EXPECTED = 2
CREATE_DATE_EXPECTED = 1234567890


def test_build_alert() -> None:
    result = BusinessLogic.build_alert(
        measure_id=1, type_alert_id=2, create_date=1234567890
    )
    assert isinstance(result, AlertData)
    assert result.measure_id == 1
    assert result.type_alert_id == TYPE_ALERT_ID_EXPECTED
    assert result.create_date == CREATE_DATE_EXPECTED


@pytest.mark.parametrize(
    ("factor", "offset", "expected"),
    [(None, None, 10), (2, None, 20), (None, 5, 15), (2, 5, 25)],
)
def test_build_measure(
    factor: int | None, offset: int | None, expected: int
) -> None:
    result = BusinessLogic.build_measure(
        parameter_id=1,
        create_date=1234567890,
        value=10,
        offset=offset,
        factor=factor,
    )
    assert isinstance(result, MeasureData)
    assert result.parameter_id == 1
    assert result.measure_date == CREATE_DATE_EXPECTED
    assert result.value == expected
