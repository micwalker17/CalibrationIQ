import pytest
from calibrationiq_notebook import calculate_deviation

def test_calculate_deviation_low():
    """Tests deviation calculation for a tool reading low."""
    # Scenario: Caliper measured 0.9985 for a 1.0000 nominal part.
    measured = 0.9985
    nominal = 1.0000
    expected_deviation = -0.0015
    assert calculate_deviation(measured, nominal) == pytest.approx(expected_deviation)

def test_calculate_deviation_high():
    """Tests deviation calculation for a tool reading high."""
    # Scenario: Caliper measured 1.0012 for a 1.0000 nominal part.
    measured = 1.0012
    nominal = 1.0000
    expected_deviation = 0.0012
    assert calculate_deviation(measured, nominal) == pytest.approx(expected_deviation)

def test_calculate_deviation_zero():
    """Tests deviation calculation when there is no error."""
    measured = 1.0000
    nominal = 1.0000
    expected_deviation = 0.0
    assert calculate_deviation(measured, nominal) == pytest.approx(expected_deviation)
