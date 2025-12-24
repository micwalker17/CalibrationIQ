# CalibrationIQ: Out-of-Tolerance Impact Analysis

[![CI Pipeline](https://github.com/YOUR_USERNAME/CalibrationIQ/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/CalibrationIQ/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A portfolio project demonstrating a data analysis pipeline for Out-of-Tolerance (OOT) calibration impact, built with Python and PySpark.

## 🚀 Project Overview

CalibrationIQ is a framework designed to automate the impact analysis of a failed calibration event for a measurement tool (e.g., a caliper). When a tool is found to be out-of-tolerance, quality engineers must determine which previously measured parts might be non-conforming. This project simulates that entire workflow in a structured, repeatable, and scalable manner.

The pipeline demonstrates skills in data engineering, process automation, data analysis, and professional software development practices.

## ✨ Key Features

-   **Modular Architecture:** The process is broken down into logical, sequential blocks, from configuration to final reporting.
-   **Data Simulation:** Includes scripts to generate sample measurement data, making the project fully self-contained and runnable without access to a production database.
-   **AI Integration (Simulated):** Demonstrates how a Large Language Model (like Google's Gemini) would be used to extract failure data from a PDF certificate.
-   **Deviation Analysis:** Calculates the tool's measurement error and applies it to historical data to determine the "true" dimensions of measured parts.
-   **Tolerance Evaluation:** Implements business logic for a "20% tolerance allowance" for non-critical features, a common practice in manufacturing quality.
-   **Professional Tooling:** Includes unit tests, a CI/CD pipeline for automated testing, and comprehensive documentation.

## 🏗️ Project Structure

A detailed explanation of the pipeline's design can be found in the [ARCHITECTURE.md](ARCHITECTURE.md) file.

## 🛠️ Getting Started

### Prerequisites

-   Python 3.9+
-   An environment with PySpark available (such as Databricks, or a local setup).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/CalibrationIQ.git
    cd CalibrationIQ
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Analysis

The main script is designed to be run in a PySpark environment. The simulation blocks allow it to execute and demonstrate the logic even without live data connections.

```bash
# In a Databricks notebook, you would run the calibrationiq_notebook.py script.
# For local execution, you can run it as a standard Python script.
# Spark-dependent parts will be skipped gracefully if PySpark is not fully configured.
python calibrationiq_notebook.py
