"""
Basic Usage Example for CalibrationIQ

This example demonstrates the core functionality of CalibrationIQ:
calculating tool deviation and understanding its impact on measurements.
"""

from calibrationiq_notebook import calculate_deviation


def example_1_basic_deviation():
    """Example 1: Calculate basic tool deviation."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Deviation Calculation")
    print("=" * 80)

    # Scenario: A caliper was calibrated against a 1.0000" standard
    # The caliper measured the standard as 0.9985"
    measured_value = 0.9985
    nominal_value = 1.0000

    # Calculate the deviation
    deviation = calculate_deviation(measured_value, nominal_value)

    print(f"\nCalibration Standard (Nominal): {nominal_value:.4f} inches")
    print(f"Caliper Reading (Measured):     {measured_value:.4f} inches")
    print(f"Tool Deviation:                 {deviation:+.4f} inches")

    # Interpret the result
    if deviation < 0:
        print(f"\n✅ Interpretation: The caliper reads LOW by {abs(deviation):.4f}\"")
        print("   This means parts are actually LARGER than the caliper indicates.")
    elif deviation > 0:
        print(f"\n✅ Interpretation: The caliper reads HIGH by {deviation:.4f}\"")
        print("   This means parts are actually SMALLER than the caliper indicates.")
    else:
        print("\n✅ Interpretation: The caliper is perfectly accurate!")

    print("\n" + "=" * 80 + "\n")


def example_2_adjust_measurement():
    """Example 2: Adjust a historical measurement using tool deviation."""
    print("=" * 80)
    print("EXAMPLE 2: Adjusting Historical Measurements")
    print("=" * 80)

    # Tool deviation from calibration certificate
    tool_deviation = -0.0015  # Tool reads 0.0015" low

    # Historical measurement from production
    measured_diameter = 0.5005  # inches
    nominal_diameter = 0.5000
    upper_tolerance = 0.5010
    lower_tolerance = 0.4990

    # Calculate the TRUE part size
    true_diameter = measured_diameter - tool_deviation

    print(f"\nOriginal Measurement:     {measured_diameter:.4f}\"")
    print(f"Tool Deviation:           {tool_deviation:+.4f}\"")
    print(f"Adjusted (True) Size:     {true_diameter:.4f}\"")
    print(f"\nTolerance Range:          {lower_tolerance:.4f}\" to {upper_tolerance:.4f}\"")

    # Check if part is in tolerance
    if lower_tolerance <= true_diameter <= upper_tolerance:
        print(f"✅ PASS: Part is within tolerance")
    else:
        print(f"❌ FAIL: Part is OUT of tolerance")
        if true_diameter > upper_tolerance:
            print(f"   Part is {true_diameter - upper_tolerance:.4f}\" OVER maximum")
        else:
            print(f"   Part is {lower_tolerance - true_diameter:.4f}\" UNDER minimum")

    print("\n" + "=" * 80 + "\n")


def example_3_multiple_measurements():
    """Example 3: Analyze multiple measurements at once."""
    print("=" * 80)
    print("EXAMPLE 3: Batch Analysis of Multiple Measurements")
    print("=" * 80)

    # Tool deviation
    tool_deviation = -0.0015

    # Multiple historical measurements
    measurements = [
        {"id": "Part-001", "measured": 0.5005, "nominal": 0.5000, "upper": 0.5010, "lower": 0.4990},
        {"id": "Part-002", "measured": 0.5008, "nominal": 0.5000, "upper": 0.5010, "lower": 0.4990},
        {"id": "Part-003", "measured": 0.4995, "nominal": 0.5000, "upper": 0.5010, "lower": 0.4990},
        {"id": "Part-004", "measured": 0.5010, "nominal": 0.5000, "upper": 0.5010, "lower": 0.4990},
    ]

    print(f"\nAnalyzing {len(measurements)} parts with tool deviation of {tool_deviation:+.4f}\"\n")
    print(f"{'Part ID':<12} {'Measured':<10} {'Adjusted':<10} {'Status':<10}")
    print("-" * 50)

    pass_count = 0
    fail_count = 0

    for part in measurements:
        adjusted = part["measured"] - tool_deviation
        
        if part["lower"] <= adjusted <= part["upper"]:
            status = "✅ PASS"
            pass_count += 1
        else:
            status = "❌ FAIL"
            fail_count += 1

        print(f"{part['id']:<12} {part['measured']:<10.4f} {adjusted:<10.4f} {status:<10}")

    print("-" * 50)
    print(f"\nSummary: {pass_count} passed, {fail_count} failed")
    print(f"Failure Rate: {(fail_count / len(measurements) * 100):.1f}%")

    print("\n" + "=" * 80 + "\n")


def example_4_tolerance_allowance():
    """Example 4: Apply 20% tolerance allowance for non-critical features."""
    print("=" * 80)
    print("EXAMPLE 4: Tolerance Allowance for Non-Critical Features")
    print("=" * 80)

    # Part measurement
    adjusted_value = 0.5012  # After applying tool deviation
    nominal = 0.5000
    upper_tol = 0.5010
    lower_tol = 0.4990
    is_critical = False  # Non-critical feature

    print(f"\nAdjusted Part Size:       {adjusted_value:.4f}\"")
    print(f"Original Tolerance:       {lower_tol:.4f}\" to {upper_tol:.4f}\"")
    print(f"Feature Criticality:      {'Critical' if is_critical else 'Non-Critical'}")

    # Check with original tolerance
    original_pass = lower_tol <= adjusted_value <= upper_tol
    print(f"\nWith Original Tolerance:  {'✅ PASS' if original_pass else '❌ FAIL'}")

    if not is_critical:
        # Calculate 20% allowance
        tolerance_band = upper_tol - lower_tol
        allowance = tolerance_band * 0.20

        expanded_upper = upper_tol + (allowance / 2)
        expanded_lower = lower_tol - (allowance / 2)

        print(f"\n20% Tolerance Allowance:  ±{allowance / 2:.4f}\"")
        print(f"Expanded Tolerance:       {expanded_lower:.4f}\" to {expanded_upper:.4f}\"")

        # Check with expanded tolerance
        expanded_pass = expanded_lower <= adjusted_value <= expanded_upper
        print(f"With Expanded Tolerance:  {'✅ PASS' if expanded_pass else '❌ FAIL'}")

        if not original_pass and expanded_pass:
            print("\n💡 Part PASSES with tolerance allowance!")
    else:
        print("\n⚠️ No tolerance allowance for critical features")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CalibrationIQ Usage Examples" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    example_1_basic_deviation()
    example_2_adjust_measurement()
    example_3_multiple_measurements()
    example_4_tolerance_allowance()

    print("=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)
