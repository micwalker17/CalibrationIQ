# Contributing to CalibrationIQ

Thank you for your interest in this project. Following these guidelines helps maintain code quality and clarity.

## Development Setup

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

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running Quality Checks

Before committing code, please run the following checks locally.

1.  **Run Unit Tests:** `pytest -v`
2.  **Format Code:** `black .`
3.  **Lint Code:** `flake8 .`

## Commit Message Convention

Please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification (e.g., `feat:`, `fix:`, `docs:`).
