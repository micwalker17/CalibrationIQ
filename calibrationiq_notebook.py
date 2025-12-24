# ============================================================================
# Block 1: Configuration and Setup
# Purpose: Imports libraries, sets up configuration, and defines placeholders
# for parameters that would normally be extracted from a live system like Jira.
# ============================================================================
import pandas as pd
import requests
import json
import base64
import os
import re
from decimal import Decimal
from datetime import datetime

print("=" * 80)
print("BLOCK 1: CONFIGURATION & SETUP")
print("=" * 80)

# --- Configuration (Replaced with Secure Placeholders) ---
# In a real environment, these would be loaded from environment variables.
JIRA_SERVER_URL = "https://your-jira-instance.com"
AI_SERVICE_API_URL = "https://your-ai-service/api/v1/chat"

# --- Placeholder Parameters ---
# These simulate inputs that would be extracted from a Jira ticket.
jira_ticket = "QUALITY-12345"
bc_number = "BC1234567"
start_date = "01/01/2023"
end_date = "12/31/2023"

print("🚀 OOT ANALYSIS NOTEBOOK - CONFIGURATION")
print(f"Jira Ticket:                 {jira_ticket}")
print(f"BC Number:                   {bc_number}")
print(f"Start Date:                  {start_date}")
print(f"End Date:                    {end_date}")
print("=" * 80)

# --- Initialize Global Variables for the script ---
selected_pdf_base64 = ""
selected_pdf_filename = "sample_cal_cert.pdf"
caliper_data = {}
no_measurements_found = True

# ============================================================================
# Block 2: PDF Data Simulation
# Purpose: Simulates fetching a PDF calibration certificate and encoding it.
# This avoids needing a live connection to a ticket system.
# ============================================================================
print("\nBLOCK 2: PDF DATA SIMULATION")
try:
    fake_pdf_content = b"%PDF-1.4\nFake calibration certificate content."
    selected_pdf_base64 = base64.b64encode(fake_pdf_content).decode("utf-8")
    print(f"✅ PDF processing simulated for: '{selected_pdf_filename}'")
except Exception as e:
    print(f"❌ ERROR in Block 2: {e}")

# ============================================================================
# Block 3: AI-Powered Data Extraction Simulation
# Purpose: Simulates calling an AI model to extract data from the PDF.
# A hardcoded JSON response makes the project runnable without a live service.
# ============================================================================
print("\nBLOCK 3: AI-POWERED DATA EXTRACTION SIMULATION")
simulated_ai_response = {
    "parameter_name": "Inside Jaws at 1.0000 in",
    "max_error_as_found": 0.9985,
    "nominal_for_max_error": 1.0000,
    "lower_limit": 0.9990,
    "upper_limit": 1.0010,
    "units": "in",
}

try:
    caliper_data = simulated_ai_response
    measured_val = float(caliper_data["max_error_as_found"])
    nominal_val = float(caliper_data["nominal_for_max_error"])
    lower_limit = float(caliper_data["lower_limit"])
    upper_limit = float(caliper_data["upper_limit"])
    units = caliper_data["units"]
    parameter_name = caliper_data["parameter_name"]

    if measured_val < lower_limit:
        violated_limit = lower_limit
        limit_type = "LOW LIMIT"
    else:
        violated_limit = upper_limit
        limit_type = "HIGH LIMIT"

    print("✅ AI data extraction simulated successfully.")
    print(json.dumps(caliper_data, indent=2))
except (KeyError, ValueError) as e:
    print(f"❌ ERROR in Block 3: {e}")


# ============================================================================
# Block 4: Deviation Calculation & Validation
# Purpose: Calculates the tool's error (deviation) and interprets its
# physical impact on measurements.
# ============================================================================
print("\nBLOCK 4: DEVIATION CALCULATION & VALIDATION")


def calculate_deviation(measured, nominal):
    """Calculates the tool's deviation: Deviation = Measured - Nominal."""
    return float(Decimal(str(measured)) - Decimal(str(nominal)))


try:
    deviation_value_inches = calculate_deviation(measured_val, nominal_val)
    direction = "HIGH" if deviation_value_inches > 0 else "LOW"
    print(
        f"✅ Deviation calculated: {deviation_value_inches:+.6f} {units} "
        f"(Caliper reads {direction})"
    )
except Exception as e:
    print(f"❌ ERROR in Block 4: {e}")


# ============================================================================
# Block 5 & 6: Historical Data Simulation
# Purpose: Simulates querying a database for historical measurements.
# For this portfolio version, we generate a sample Pandas DataFrame.
# ============================================================================
print("\nBLOCK 5 & 6: HISTORICAL DATA SIMULATION")

try:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("CalibrationIQ_Portfolio").getOrCreate()
    print("✅ SparkSession created (or retrieved).")
except ImportError:
    print("⚠️ PySpark not found. This script should be run in a PySpark environment.")
    spark = None


def generate_sample_dataframe(spark_session):
    """Generates a sample Spark DataFrame simulating historical measurements."""
    if not spark_session:
        print("   -> Skipping DataFrame generation as Spark is not available.")
        return None

    sample_data = [
        (
            "WO-001",
            "SN-101",
            "Char 1",
            "Hole Diameter",
            0.5005,
            0.5000,
            0.5010,
            0.4990,
            "BILATERAL",
            "Critical",
        ),
        (
            "WO-001",
            "SN-101",
            "Char 2",
            "Step Height",
            1.2510,
            1.2500,
            1.2520,
            1.2480,
            "BILATERAL",
            "Major",
        ),
        (
            "WO-002",
            "SN-201",
            "Char 5",
            "Outer Diameter",
            3.0001,
            3.0000,
            3.0005,
            2.9995,
            "BILATERAL",
            "NotSpecified",
        ),
        (
            "WO-002",
            "SN-201",
            "Char 6",
            "Groove Depth",
            0.1008,
            0.1000,
            0.1010,
            0.0990,
            "BILATERAL",
            "NotSpecified",
        ),
        (
            "WO-003",
            "SN-301",
            "Char 9",
            "Slot Width",
            0.7511,
            0.7500,
            0.7510,
            0.7490,
            "BILATERAL",
            "Minor",
        ),
    ]
    schema = [
        "job_number",
        "sample_serial_number",
        "dimension_id",
        "feature_name",
        "measured_value",
        "nominal_value",
        "original_upper_tol",
        "original_lower_tol",
        "tolerance_type",
        "criticality",
    ]
    df = spark_session.createDataFrame(sample_data, schema)
    global no_measurements_found
    no_measurements_found = False
    print("✅ Sample Spark DataFrame generated successfully.")
    return df


all_measurements_df = generate_sample_dataframe(spark)


# ============================================================================
# Block 7: Calculate Adjusted Values & Evaluate Impact
# Purpose: Applies the tool deviation to historical data to find the "true"
# part dimensions and determines the final pass/fail status.
# ============================================================================
print("\nBLOCK 7: ADJUSTED VALUE CALCULATION & IMPACT ANALYSIS")

if not no_measurements_found and all_measurements_df:
    from pyspark.sql.functions import col, lit, when

    all_measurements_df = all_measurements_df.withColumn(
        "adjusted_value", col("measured_value") - lit(deviation_value_inches)
    )

    all_measurements_df = all_measurements_df.withColumn(
        "allowance_eligible",
        when(col("criticality").isin(["Critical", "Major"]), lit("NO - KC")).otherwise(
            lit("YES")
        ),
    )

    all_measurements_df = all_measurements_df.withColumn(
        "expanded_upper_tol",
        when(
            col("allowance_eligible") == "YES",
            col("original_upper_tol")
            + ((col("original_upper_tol") - col("nominal_value")) * 0.20),
        ).otherwise(col("original_upper_tol")),
    )

    all_measurements_df = all_measurements_df.withColumn(
        "expanded_lower_tol",
        when(
            col("allowance_eligible") == "YES",
            col("original_lower_tol")
            - ((col("nominal_value") - col("original_lower_tol")) * 0.20),
        ).otherwise(col("original_lower_tol")),
    )

    all_measurements_df = all_measurements_df.withColumn(
        "final_status",
        when(
            (col("adjusted_value") >= col("expanded_lower_tol"))
            & (col("adjusted_value") <= col("expanded_upper_tol")),
            lit("✅ PASS"),
        ).otherwise(lit("❌ FAIL")),
    )

    print("✅ Adjusted values calculated and final status determined.")
    all_measurements_df.show(5)
else:
    print("⚠️ No measurements to analyze.")


# ============================================================================
# Block 8: Generate Failure Report
# Purpose: Filters the analysis to only show the measurements that are
# confirmed failures, which require engineering review.
# ============================================================================
print("\nBLOCK 8: FAILURE REPORT GENERATION")

if not no_measurements_found and all_measurements_df:
    failures_df = all_measurements_df.filter(col("final_status") == "❌ FAIL")
    failure_count = failures_df.count()

    if failure_count > 0:
        print(f"🔥 Found {failure_count} measurements requiring engineering review.")
        failures_df.show()
    else:
        print("✅ No failures found after analysis.")
else:
    failure_count = 0
    print("✅ No failures found as no measurements were analyzed.")


# ============================================================================
# Block 9-12: Reporting and Cleanup Simulation
# Purpose: Simulates the final steps of the process, such as creating
# reports, posting to a ticket system, and cleaning up resources.
# ============================================================================
print("\nBLOCK 9-12: FINAL REPORTING SIMULATION")

if failure_count > 0:
    print(f"✅ Simulation Complete: {failure_count} failures were identified.")
    print("   -> Next steps: generate HTML report, create NC, post to Jira.")
else:
    print("✅ Simulation Complete: No failures were identified.")
    print("   -> Next step: post 'All Clear' comment to Jira and close ticket.")

print("\n✅ Notebook execution finished.")

