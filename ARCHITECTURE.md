# CalibrationIQ Architecture

This document outlines the architecture and data flow of the CalibrationIQ pipeline. The system is designed as a series of modular, sequential blocks, each with a distinct responsibility.

## Core Principles

-   **Modularity:** Each block is self-contained, making the pipeline easy to understand, test, and modify.
-   **Automation:** The primary goal is to automate the manual, error-prone process of calibration impact analysis.
-   **Traceability:** All data, decisions, and reports are designed to be traceable back to the source, ensuring auditability.
-   **Scalability:** By leveraging PySpark, the analysis can scale from a few hundred measurements to millions.

## Pipeline Block-by-Block

The pipeline consists of a series of logical blocks, which are simulated in the portfolio version of this project.

#### **Block 1-2: Configuration & Data Retrieval (Simulated)**
-   **Responsibility:** Initialize parameters and retrieve the calibration certificate.
-   **Portfolio Implementation:** Uses hardcoded placeholders for ticket info and simulates the retrieval of a PDF certificate to ensure the script is runnable by anyone.

#### **Block 3: AI-Powered Data Extraction (Simulated)**
-   **Responsibility:** Extract key failure data from the PDF certificate using a vision-capable AI model.
-   **Portfolio Implementation:** A hardcoded JSON object simulates the AI's response, demonstrating the expected data structure without requiring a live API call.

#### **Block 4: Deviation Calculation**
-   **Responsibility:** Calculate the tool's systematic error (`Deviation = Measured - Nominal`) and interpret its physical meaning.
-   **Impact Analysis:** This step is crucial for determining if the tool's error is conservative (safer) or non-conservative (riskier).

#### **Block 5-6: Historical Impact Query (Simulated)**
-   **Responsibility:** Query a database to find all historical measurements taken with the out-of-tolerance tool.
-   **Portfolio Implementation:** A sample PySpark DataFrame is generated to simulate the output of a complex SQL query against a production data warehouse.

#### **Block 7: Adjusted Value Calculation & Impact Analysis**
-   **Responsibility:** Apply the tool's deviation to every historical measurement to calculate the "true" dimension of each part.
-   **Business Logic:** Implements a "20% tolerance allowance" rule, where the tolerance band for non-critical features is expanded, a common practice in manufacturing quality.

#### **Block 8: Failure Report Generation**
-   **Responsibility:** Identify the final set of non-conforming parts.
-   **Implementation:** Filters the results from Block 7 to find any `Adjusted Value` that still falls outside the (potentially expanded) tolerance limits. These are the confirmed failures requiring review.

#### **Block 9-12: Reporting & Cleanup (Simulated)**
-   **Responsibility:** The final steps would involve generating an HTML report, creating a Non-Conformance ticket in a system like Jules, and posting a summary back to the original Jira ticket. This is described but not executed in the portfolio script.
