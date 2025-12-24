"""
Advanced Usage Scenarios for CalibrationIQ

This example demonstrates complex real-world scenarios including:
- Conservative vs non-conservative OOT events
- Multi-tool analysis
- Statistical analysis of impact
"""

from calibrationiq_notebook import calculate_deviation
import statistics


def scenario_1_conservative_vs_nonconservative():
    """Scenario 1: Understanding conservative vs non-conservative OOT."""
    print("=" * 80)
    print("SCENARIO 1: Conservative vs Non-Conservative OOT Events")
    print("=" * 80)

    print("\n📘 BACKGROUND:")
    print("   Conservative OOT: Tool reads HIGH → Parts are actually SMALLER")
    print("   Non-Conservative OOT: Tool reads LOW → Parts are actually LARGER")
    print("   Non-conservative events are more critical!\n")

    # Conservative example (tool reads high)
    print("--- Conservative Example ---")
    tool_deviation_high = 0.0012  # Tool reads 0.0012" high
    part_measured = 0.5008
    part_upper = 0.5010
    part_lower = 0.4990

    adjusted = part_measured - tool_deviation_high
    print(f"Tool reads HIGH by:       {tool_deviation_high:+.4f}\"")
    print(f"Part measured at:         {part_measured:.4f}\"")
    print(f"Part true size:           {adjusted:.4f}\"")
    print(f"Result: Part is SMALLER than measured (conservative)")
    print(f"Status: {'✅ PASS' if part_lower <= adjusted <= part_upper else '❌ FAIL'}")

    # Non-conservative example (tool reads low)
    print("\n--- Non-Conservative Example ---")
    tool_deviation_low = -0.0012  # Tool reads 0.0012" low
    part_measured = 0.5008
    
    adjusted = part_measured - tool_deviation_low
    print(f"Tool reads LOW by:        {tool_deviation_low:+.4f}\"")
    print(f"Part measured at:         {part_measured:.4f}\"")
    print(f"Part true size:           {adjusted:.4f}\"")
    print(f"Result: Part is LARGER than measured (non-conservative)")
    print(f"Status: {'✅ PASS' if part_lower <= adjusted <= part_upper else '❌ FAIL'}")

    print("\n⚠️ Non-conservative events require immediate action!")
    print("\n" + "=" * 80 + "\n")


def scenario_2_multi_tool_analysis():
    """Scenario 2: Analyzing impact from multiple OOT tools."""
    print("=" * 80)
    print("SCENARIO 2: Multi-Tool OOT Analysis")
    print("=" * 80)

    # Multiple tools with different deviations
    tools = {
        "Caliper-001": -0.0015,  # Reads low
        "Caliper-002": 0.0008,   # Reads high
        "Micrometer-001": -0.0003,  # Reads slightly low
    }

    # Sample measurements made with different tools
    measurements = [
        {"part": "Part-A", "tool": "Caliper-001", "measured": 1.0005, "upper": 1.0010, "lower": 0.9990},
        {"part": "Part-B", "tool": "Caliper-002", "measured": 1.0008, "upper": 1.0010, "lower": 0.9990},
        {"part": "Part-C", "tool": "Micrometer-001", "measured": 0.5002, "upper": 0.5010, "lower": 0.4990},
        {"part": "Part-D", "tool": "Caliper-001", "measured": 1.0009, "upper": 1.0010, "lower": 0.9990},
    ]

    print("\n📊 Tool Deviations:")
    for tool, deviation in tools.items():
        print(f"   {tool:<20} {deviation:+.4f}\"")

    print("\n📋 Analysis Results:")
    print(f"{'Part':<10} {'Tool':<20} {'Measured':<10} {'Adjusted':<10} {'Status':<10}")
    print("-" * 70)

    results = []
    for m in measurements:
        tool_dev = tools[m["tool"]]
        adjusted = m["measured"] - tool_dev
        status = "✅ PASS" if m["lower"] <= adjusted <= m["upper"] else "❌ FAIL"
        results.append({"adjusted": adjusted, "status": status})
        
        print(f"{m['part']:<10} {m['tool']:<20} {m['measured']:<10.4f} {adjusted:<10.4f} {status:<10}")

    # Summary by tool
    print("\n📈 Impact Summary by Tool:")
    for tool in tools:
        tool_measurements = [m for m in measurements if m["tool"] == tool]
        tool_results = [r for m, r in zip(measurements, results) if m["tool"] == tool]
        failures = sum(1 for r in tool_results if r["status"] == "❌ FAIL")
        
        print(f"   {tool:<20} {len(tool_measurements)} parts, {failures} failures")

    print("\n" + "=" * 80 + "\n")


def scenario_3_statistical_analysis():
    """Scenario 3: Statistical analysis of OOT impact."""
    print("=" * 80)
    print("SCENARIO 3: Statistical Analysis of OOT Impact")
    print("=" * 80)

    tool_deviation = -0.0015

    # Large dataset of measurements
    measured_values = [
        0.5001, 0.5003, 0.5005, 0.5007, 0.5009,
        0.5002, 0.5004, 0.5006, 0.5008, 0.5010,
        0.4998, 0.5000, 0.5002, 0.5004, 0.5006,
        0.5003, 0.5005, 0.5007, 0.5009, 0.5011,
    ]

    upper_tol = 0.5010
    lower_tol = 0.4990

    # Calculate adjusted values
    adjusted_values = [m - tool_deviation for m in measured_values]

    # Statistical analysis
    print("\n📊 Measurement Statistics:")
    print(f"\nOriginal Measurements:")
    print(f"   Mean:    {statistics.mean(measured_values):.4f}\"")
    print(f"   Median:  {statistics.median(measured_values):.4f}\"")
    print(f"   Std Dev: {statistics.stdev(measured_values):.4f}\"")
    print(f"   Min:     {min(measured_values):.4f}\"")
    print(f"   Max:     {max(measured_values):.4f}\"")

    print(f"\nAdjusted (True) Values:")
    print(f"   Mean:    {statistics.mean(adjusted_values):.4f}\"")
    print(f"   Median:  {statistics.median(adjusted_values):.4f}\"")
    print(f"   Std Dev: {statistics.stdev(adjusted_values):.4f}\"")
    print(f"   Min:     {min(adjusted_values):.4f}\"")
    print(f"   Max:     {max(adjusted_values):.4f}\"")

    # Pass/Fail analysis
    original_passes = sum(1 for m in measured_values if lower_tol <= m <= upper_tol)
    adjusted_passes = sum(1 for a in adjusted_values if lower_tol <= a <= upper_tol)

    print(f"\n📈 Pass/Fail Analysis:")
    print(f"   Total Parts:              {len(measured_values)}")
    print(f"   Original Passes:          {original_passes} ({original_passes/len(measured_values)*100:.1f}%)")
    print(f"   Adjusted Passes:          {adjusted_passes} ({adjusted_passes/len(measured_values)*100:.1f}%)")
    print(f"   New Failures:             {original_passes - adjusted_passes}")

    # Distribution shift
    mean_shift = statistics.mean(adjusted_values) - statistics.mean(measured_values)
    print(f"\n📉 Distribution Shift:")
    print(f"   Mean shifted by:          {mean_shift:+.4f}\"")
    print(f"   Direction:                {'Higher' if mean_shift > 0 else 'Lower'}")

    print("\n" + "=" * 80 + "\n")


def scenario_4_risk_assessment():
    """Scenario 4: Risk-based prioritization of failures."""
    print("=" * 80)
    print("SCENARIO 4: Risk-Based Failure Prioritization")
    print("=" * 80)

    tool_deviation = -0.0015

    # Parts with different criticality levels
    parts = [
        {"id": "Part-001", "measured": 0.5011, "upper": 0.5010, "lower": 0.4990, "criticality": "Critical", "qty": 50},
        {"id": "Part-002", "measured": 0.5012, "upper": 0.5010, "lower": 0.4990, "criticality": "Major", "qty": 30},
        {"id": "Part-003", "measured": 0.5013, "upper": 0.5010, "lower": 0.4990, "criticality": "Minor", "qty": 100},
        {"id": "Part-004", "measured": 0.5015, "upper": 0.5010, "lower": 0.4990, "criticality": "NotSpecified", "qty": 200},
    ]

    print("\n🎯 Risk Assessment Matrix:\n")
    print(f"{'Part ID':<12} {'Criticality':<15} {'Qty':<6} {'Adjusted':<10} {'Over Limit':<12} {'Risk':<10}")
    print("-" * 75)

    for part in parts:
        adjusted = part["measured"] - tool_deviation
        over_limit = adjusted - part["upper"]
        
        # Risk scoring
        if part["criticality"] == "Critical":
            risk_score = "🔴 HIGH"
        elif part["criticality"] == "Major":
            risk_score = "🟡 MEDIUM"
        else:
            risk_score = "🟢 LOW"

        print(f"{part['id']:<12} {part['criticality']:<15} {part['qty']:<6} {adjusted:<10.4f} {over_limit:+.4f}\"     {risk_score:<10}")

    print("\n📋 Recommended Actions:")
    print("   🔴 HIGH Risk:   Immediate containment, 100% inspection, engineering review")
    print("   🟡 MEDIUM Risk: Sample inspection, disposition by quality engineer")
    print("   🟢 LOW Risk:    Apply tolerance allowance, document and release")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    """Run all advanced scenarios."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "CalibrationIQ Advanced Scenarios" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    scenario_1_conservative_vs_nonconservative()
    scenario_2_multi_tool_analysis()
    scenario_3_statistical_analysis()
    scenario_4_risk_assessment()

    print("=" * 80)
    print("All advanced scenarios completed successfully!")
    print("=" * 80)
