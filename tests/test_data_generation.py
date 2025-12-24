"""Unit tests for sample data generation."""

import pytest
import pandas as pd
from generate_sample_data import generate_data
import os


class TestDataGeneration:
    """Test suite for the sample data generator."""

    def test_generate_data_creates_file(self, tmp_path):
        """Tests that generate_data creates a CSV file."""
        # Change to temporary directory
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            assert os.path.exists("sample_measurements.csv")
        finally:
            os.chdir(original_dir)

    def test_generated_data_structure(self, tmp_path):
        """Tests that generated CSV has correct column structure."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            df = pd.read_csv("sample_measurements.csv")

            expected_columns = [
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

            assert list(df.columns) == expected_columns
        finally:
            os.chdir(original_dir)

    def test_generated_data_not_empty(self, tmp_path):
        """Tests that generated data contains rows."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            df = pd.read_csv("sample_measurements.csv")
            assert len(df) > 0
        finally:
            os.chdir(original_dir)

    def test_generated_data_types(self, tmp_path):
        """Tests that generated data has correct data types."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            df = pd.read_csv("sample_measurements.csv")

            # Check numeric columns
            assert df["measured_value"].dtype in ["float64", "float32"]
            assert df["nominal_value"].dtype in ["float64", "float32"]
            assert df["original_upper_tol"].dtype in ["float64", "float32"]
            assert df["original_lower_tol"].dtype in ["float64", "float32"]

            # Check string columns
            assert df["job_number"].dtype == "object"
            assert df["feature_name"].dtype == "object"
        finally:
            os.chdir(original_dir)

    def test_tolerance_values_logical(self, tmp_path):
        """Tests that upper tolerance is greater than lower tolerance."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            df = pd.read_csv("sample_measurements.csv")

            for _, row in df.iterrows():
                assert row["original_upper_tol"] > row["original_lower_tol"]
        finally:
            os.chdir(original_dir)

    def test_nominal_within_tolerance(self, tmp_path):
        """Tests that nominal values are within tolerance bounds."""
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            generate_data()
            df = pd.read_csv("sample_measurements.csv")

            for _, row in df.iterrows():
                assert row["original_lower_tol"] <= row["nominal_value"]
                assert row["nominal_value"] <= row["original_upper_tol"]
        finally:
            os.chdir(original_dir)
