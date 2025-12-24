"""Unit tests for CalibrationIQ core logic."""

import pytest
from decimal import Decimal
from calibrationiq_notebook import calculate_deviation


class TestDeviationCalculation:
    """Test suite for deviation calculation function."""

    def test_calculate_deviation_low(self):
        """Tests deviation calculation for a tool reading low."""
        measured = 0.9985
        nominal = 1.0000
        expected_deviation = -0.0015
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_high(self):
        """Tests deviation calculation for a tool reading high."""
        measured = 1.0012
        nominal = 1.0000
        expected_deviation = 0.0012
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_zero(self):
        """Tests deviation calculation when there is no error."""
        measured = 1.0000
        nominal = 1.0000
        expected_deviation = 0.0
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_large_positive(self):
        """Tests deviation with a large positive error."""
        measured = 5.0250
        nominal = 5.0000
        expected_deviation = 0.0250
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_large_negative(self):
        """Tests deviation with a large negative error."""
        measured = 2.9750
        nominal = 3.0000
        expected_deviation = -0.0250
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_precision(self):
        """Tests that deviation maintains high precision using Decimal."""
        measured = 0.123456789
        nominal = 0.123456780
        expected_deviation = 0.000000009
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-9)

    def test_calculate_deviation_with_strings(self):
        """Tests that function handles string inputs correctly."""
        measured = "1.0015"
        nominal = "1.0000"
        expected_deviation = 0.0015
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_returns_float(self):
        """Tests that the function always returns a float type."""
        measured = 1.0015
        nominal = 1.0000
        result = calculate_deviation(measured, nominal)
        assert isinstance(result, float)

    def test_calculate_deviation_negative_values(self):
        """Tests deviation calculation with negative nominal values."""
        measured = -0.5005
        nominal = -0.5000
        expected_deviation = -0.0005
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)

    def test_calculate_deviation_very_small_numbers(self):
        """Tests deviation with very small measurement values."""
        measured = 0.00015
        nominal = 0.00010
        expected_deviation = 0.00005
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-8)


class TestDeviationEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_zero_measured_value(self):
        """Tests deviation when measured value is zero."""
        measured = 0.0
        nominal = 1.0
        expected_deviation = -1.0
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation)

    def test_zero_nominal_value(self):
        """Tests deviation when nominal value is zero."""
        measured = 1.0
        nominal = 0.0
        expected_deviation = 1.0
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation)

    def test_both_zero(self):
        """Tests deviation when both values are zero."""
        measured = 0.0
        nominal = 0.0
        expected_deviation = 0.0
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation)

    def test_large_values(self):
        """Tests deviation with large measurement values."""
        measured = 1000.0015
        nominal = 1000.0000
        expected_deviation = 0.0015
        result = calculate_deviation(measured, nominal)
        assert result == pytest.approx(expected_deviation, abs=1e-6)


class TestRealWorldScenarios:
    """Test suite for realistic calibration scenarios."""

    def test_caliper_reading_low_scenario(self):
        """Simulates a real caliper reading 0.0015 inches low."""
        # Caliper measured a 1.0000" standard as 0.9985"
        measured = 0.9985
        nominal = 1.0000
        deviation = calculate_deviation(measured, nominal)

        # The caliper reads LOW, so actual parts are LARGER than measured
        assert deviation < 0
        assert abs(deviation) == pytest.approx(0.0015, abs=1e-6)

    def test_caliper_reading_high_scenario(self):
        """Simulates a real caliper reading 0.0012 inches high."""
        # Caliper measured a 1.0000" standard as 1.0012"
        measured = 1.0012
        nominal = 1.0000
        deviation = calculate_deviation(measured, nominal)

        # The caliper reads HIGH, so actual parts are SMALLER than measured
        assert deviation > 0
        assert deviation == pytest.approx(0.0012, abs=1e-6)

    def test_micrometer_precision_scenario(self):
        """Simulates a micrometer with 0.0001" precision."""
        measured = 0.5003
        nominal = 0.5000
        deviation = calculate_deviation(measured, nominal)
        assert deviation == pytest.approx(0.0003, abs=1e-6)

    def test_metric_caliper_scenario(self):
        """Simulates a metric caliper (mm) reading."""
        # Caliper measured a 25.00mm standard as 24.96mm
        measured = 24.96
        nominal = 25.00
        deviation = calculate_deviation(measured, nominal)
        assert deviation == pytest.approx(-0.04, abs=1e-6)
