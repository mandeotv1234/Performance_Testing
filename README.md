# Locust Performance Testing Guide

This project contains performance test scripts for OrangeHRM using Locust.

## Prerequisites
- Python 3.x installed
- Install dependencies:
  ```bash
  pip install locust pandas
  ```

## Project Structure
- `locust_pim.py`: Scenario: Login -> Add Employee -> View List -> Search (Uses `search_data.csv`).
- `locust_leave.py`: Scenario: Login -> View Leave List -> Get Leave Requests API.
- `generate_data.py`: Script to generate dummy data.
- `reports/`:
    - `pim/`: Reports for PIM scenario.
    - `leave/`: Reports for Leave scenario.

## Setup Data
Before running tests, ensure data libraries are generated:
```bash
python3 generate_data.py
```

## Running the Tests

Use the commands below for each scenario.

### A. PIM Scenario (`locust_pim.py`)

#### 1. Load Test (20 Users)
**Goal**: Simulate moderate load.
```bash
mkdir -p reports/pim/load && python3 -m locust -f locust_pim.py --headless -u 20 -r 2 --run-time 5m --html reports/pim/load/report.html --csv reports/pim/load/data
```

#### 2. Stress Test (200 Users)
**Goal**: Test system limits with high user count.
```bash
mkdir -p reports/pim/stress && python3 -m locust -f locust_pim.py --headless -u 200 -r 2 --run-time 5m --html reports/pim/stress/report.html --csv reports/pim/stress/data
```

#### 3. Spike Test (100 Users Burst)
**Goal**: Test sudden burst of 100 users.
```bash
mkdir -p reports/pim/spike && python3 -m locust -f locust_pim.py --headless -u 100 -r 100 --run-time 2m --html reports/pim/spike/report.html --csv reports/pim/spike/data
```

---

### B. Leave Scenario (`locust_leave.py`)

#### 1. Load Test (20 Users)
```bash
mkdir -p reports/leave/load && python3 -m locust -f locust_leave.py --headless -u 20 -r 2 --run-time 5m --html reports/leave/load/report.html --csv reports/leave/load/data
```

#### 2. Stress Test (200 Users)
```bash
mkdir -p reports/leave/stress && python3 -m locust -f locust_leave.py --headless -u 200 -r 2 --run-time 5m --html reports/leave/stress/report.html --csv reports/leave/stress/data
```

#### 3. Spike Test (100 Users Burst)
```bash
mkdir -p reports/leave/spike && python3 -m locust -f locust_leave.py --headless -u 100 -r 100 --run-time 2m --html reports/leave/spike/report.html --csv reports/leave/spike/data
```
