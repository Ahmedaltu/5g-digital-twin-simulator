# 5G RAN Digital Twin Simulator — Claude Context

## Project Structure

```
5G RAN Digital Twin Simulator/          # repo root
  5g-digital-twin-simulator/            # main package
    main.py                             # simulation entry point
    simulation_config.py                # config loader
    logging_config.py                   # logging setup
    config.json                         # default config
    simulator/                          # core simulation modules
      simulation_engine.py
      base_station.py
      user_equipment.py
      base_scheduler.py
      scheduler.py                      # RoundRobinScheduler
      proportional_fair_scheduler.py
      scheduler_factory.py
      kpi_utils.py
      metrics.py
    digital_twin/
      twin_model.py                     # DigitalTwin state/history
    ai/
      traffic_prediction.py             # ML-based demand prediction
    dashboard/
      dashboard.py                      # Streamlit UI (port 8501)
    tests/                              # pytest test suite
  simulator/                            # root-level simulator (parallel development)
  tests/                                # root-level tests
  requirements.txt                      # root deps (simpy, numpy, pandas, sklearn, streamlit)
  docker-compose.yml                    # backend (8000) + dashboard (8501)
  Dockerfile.backend
  Dockerfile.frontend
  .venv/                                # virtual environment
```

## Environment Setup

```bash
# Activate venv (Windows)
source .venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
# or for the sub-package
pip install -r 5g-digital-twin-simulator/requirements.txt
```

## Commands

### Run Simulation

```bash
cd 5g-digital-twin-simulator
python main.py
python main.py --config config.json
python main.py --scheduler proportional_fair --steps 200 --users 30 --bandwidth 150
```

### Debug

```bash
# Run with verbose Python output
cd 5g-digital-twin-simulator
python -u main.py 2>&1 | tee ../logs/debug.log

# Check logs (written to logs/simulator.log)
tail -f ../logs/dashboard.log

# Run dashboard in debug mode
cd 5g-digital-twin-simulator
streamlit run dashboard/dashboard.py --logger.level=debug

# Inspect simulation output
python -c "import pandas as pd; df = pd.read_csv('data/simulation_results.csv'); print(df.describe())"
```

### Test

```bash
# Run all tests from repo root
python -m pytest tests/ -v
python -m pytest simulator/tests/ -v

# Run sub-package tests
cd 5g-digital-twin-simulator
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_simulation_engine.py -v

# Run with coverage
python -m pytest tests/ --cov=simulator --cov-report=term-missing

# Run all tests across the whole repo
python -m pytest -v
```

### Dashboard

```bash
cd 5g-digital-twin-simulator
streamlit run dashboard/dashboard.py
# Opens at http://localhost:8501
```

### Update Context (regenerate simulation data)

```bash
# Re-run simulation to refresh data/simulation_results.csv
cd 5g-digital-twin-simulator
python main.py --config config.json

# Then restart the dashboard to pick up new data
streamlit run dashboard/dashboard.py
```

### Deploy (Docker)

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild a single service
docker-compose up --build backend
docker-compose up --build dashboard
```

Services after deploy:
- Backend simulation: `http://localhost:8000`
- Streamlit dashboard: `http://localhost:8501`

## Key Config (config.json)

```json
{
  "simulation_steps": 200,
  "users": 30,
  "total_bandwidth_mbps": 150.0,
  "scheduler": "proportional_fair",
  "output_file": "data/simulation_results.csv"
}
```

Scheduler options: `round_robin`, `proportional_fair`

## Architecture Notes

- `SimulationEngine` runs multi-cell discrete-event simulation via SimPy
- `SchedulerFactory` enables pluggable schedulers — add new ones by subclassing `BaseScheduler`
- `DigitalTwin` in `digital_twin/twin_model.py` maintains virtual network state and history
- AI traffic prediction uses scikit-learn models in `ai/traffic_prediction.py`
- Dashboard reads `data/simulation_results.csv` — run simulation first before launching it
- Logs go to `logs/simulator.log` (console + file, INFO level)
