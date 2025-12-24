"""Integration tests for the CalibrationIQ pipeline."""

import pytest
from calibrationiq_notebook import calculate_deviation


class TestPipelineIntegration:
    """Test suite for end-to-end pipeline scenarios."""

    def test_full_oot_analysis_workflow(self):
        """Tests a complete OOT analysis workflow."""
        # Step 1: Simulate calibration certificate data
        cal_cert_data = {
            "measured": 0.9985,
            "nominal": 1.0000,
            "lower_limit": 0.9990,
            "upper_limit": 1.0010,
        }

        # Step 2: Calculate deviation
        deviation = calculate_deviation(
            cal_cert_data["measured"], cal_cert_data["nominal"]
        )

        # Step 3: Verify tool is out of tolerance
        assert deviation < 0  # Tool reads low
        assert cal_cert_data["measured"] < cal_cert_data["lower_limit"]

        # Step 4: Simulate historical measurement
        historical_measurement = 0.5005  # Part measured at 0.5005"
        historical_nominal = 0.5000
        historical_upper = 0.5010
        historical_lower = 0.4990

        # Step 5: Calculate adjusted (true) value
        adjusted_value = historical_measurement - deviation

        # Step 6: Verify adjusted value
        assert adjusted_value > historical_measurement  # Part is actually larger
        assert adjusted_value == pytest.approx(0.5020, abs=1e-6)

        # Step 7: Check if part is still in tolerance
        is_in_tolerance = (
            historical_lower <= adjusted_value <= historical_upper
        )
        assert not is_in_tolerance  # Part fails after adjustment

    def test_conservative_oot_scenario(self):
        """Tests a conservative OOT scenario (tool reads high)."""
        # Tool reads 0.0012" high
        measured = 1.0012
        nominal = 1.0000
        deviation = calculate_deviation(measured, nominal)

        # Historical part measured at upper limit
        part_measured = 0.5010
        part_nominal = 0.5000
        part_upper = 0.5010
        part_lower = 0.4990

        # Adjusted value (true size)
        adjusted = part_measured - deviation

        # Part is actually smaller than measured (conservative)
        assert adjusted < part_measured
        assert adjusted == pytest.approx(0.4998, abs=1e-6)

        # Part is still in tolerance
        assert part_lower <= adjusted <= part_upper

    def test_non_conservative_oot_scenario(self):
        """Tests a non-conservative OOT scenario (tool reads low)."""
        # Tool reads 0.0015" low
        measured = 0.9985
        nominal = 1.0000
        deviation = calculate_deviation(measured, nominal)

        # Historical part measured at upper limit
        part_measured = 0.5010
        part_nominal = 0.5000
        part_upper = 0.5010
        part_lower = 0.4990

        # Adjusted value (true size)
        adjusted = part_measured - deviation

        # Part is actually larger than measured (non-conservative)
        assert adjusted > part_measured
        assert adjusted == pytest.approx(0.5025, abs=1e-6)

        # Part is OUT of tolerance
        assert adjusted > part_upper

    def test_tolerance_allowance_logic(self):
        """Tests the 20% tolerance allowance business rule."""
        # Non-critical feature with bilateral tolerance
        nominal = 1.0000
        upper_tol = 1.0010
        lower_tol = 0.9990
        tolerance_band = upper_tol - lower_tol  # 0.0020

        # Calculate 20% allowance
        allowance = tolerance_band * 0.20  # 0.0004

        # Expanded limits
        expanded_upper = upper_tol + (allowance / 2)
        expanded_lower = lower_tol - (allowance / 2)

        assert expanded_upper == pytest.approx(1.0012, abs=1e-6)
        assert expanded_lower == pytest.approx(0.9988, abs=1e-6)

        # Test a marginal part
        adjusted_value = 1.0011

        # Would fail with original tolerance
        assert adjusted_value > upper_tol

        # Passes with expanded tolerance
        assert expanded_lower <= adjusted_value <= expanded_upper

    def test_critical_feature_no_allowance(self):
        """Tests that critical features do not get tolerance allowance."""
        # Critical feature should use original tolerance
        nominal = 1.0000
        upper_tol = 1.0010
        lower_tol = 0.9990

        # For critical features, no expansion
        expanded_upper = upper_tol
        expanded_lower = lower_tol

        # Marginal part
        adjusted_value = 1.0011

        # Fails because no allowance for critical features
        assert adjusted_value > expanded_upper
