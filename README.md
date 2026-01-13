# Locust Performance Testing Guide

This project contains a Locust performance test script for OrangeHRM with enhanced logging and data generation.

## Prerequisites
- Python 3.x installed
- Install dependencies:
  ```bash
  pip install locust pandas
  ```

## Project Structure
- `locustfile.py`: Main test script (Login -> Add -> Create API -> View List -> Search API).
- `generate_data.py`: Script to generate dummy data.
- `employee_data.csv`: Generated employee data (200 rows).
- `search_data.csv`: Generated search keywords (100 rows).
- `reports/`:
    - `load/`: Load test reports.
    - `stress/`: Stress test reports.
    - `spike/`: Spike test reports.

## Setup Data
Before running tests, ensure data libraries are generated:
```bash
python3 generate_data.py
```

## Running the Tests

Use the following commands. Note that `mkdir -p` is included to ensure the report directories exist.

### 1. Load Test
**Goal**: Simulate normal expected traffic (e.g., 20 users).
```bash
mkdir -p reports/load && python3 -m locust -f locustfile.py --headless -u 20 -r 2 --run-time 2m --html reports/load/report.html --csv reports/load/data
```

### 2. Stress Test
**Goal**: Test the system limits (e.g., 100 users).
```bash
mkdir -p reports/stress && python3 -m locust -f locustfile.py --headless -u 100 -r 1 --run-time 5m --html reports/stress/report.html --csv reports/stress/data
```

### 3. Spike Test
**Goal**: Test sudden bursts of traffic (e.g., 50 users instantly).
```bash
mkdir -p reports/spike && python3 -m locust -f locustfile.py --headless -u 50 -r 50 --run-time 2m --html reports/spike/report.html --csv reports/spike/data
```

## Reports & Logging
- **Console Output**: The script now logs detailed information for every major step:
    - Login Success/Failure
    - Page Access Status
    - Created Employee Name & Status
    - Search Query & Result Count
- **HTML Reports**: Found in the respective folders (`reports/load/report.html`, etc.).
- **CSV Data**: Raw metrics found alongside the HTML reports.
