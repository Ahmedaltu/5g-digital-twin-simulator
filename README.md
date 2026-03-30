
# 5G RAN Digital Twin Simulator

A research-grade Python platform for simulating 5G Radio Access Networks (RAN), exploring scheduling algorithms, AI-based traffic prediction, and interactive dashboard visualization.

---


## Dashboard Plot Navigation (NEW)

The Streamlit dashboard now features modern, user-friendly navigation for all simulation plots:

- **Tabbed Plots:** All time-series charts (Throughput, User Throughput, Jain's Fairness, Congestion Ratio, Traffic Demand, Cell Utilization) are organized into clickable tabs. Users can simply click a tab to view the corresponding plot—no scrolling required.
- **Responsive UI:** The dashboard layout is clean and efficient, making it easy to focus on one metric at a time.

**Example:**

<img width="2351" height="1266" alt="image" src="https://github.com/user-attachments/assets/d6c10cba-c9e1-4058-8ada-9d44bd4f1a40" />


This improves usability for large result sets and matches the navigation style of modern analytics dashboards.

---

## Key Features

- Simulates 5G RAN with multiple base stations and user equipment (UE)
- Pluggable scheduler architecture (Round Robin, Proportional Fair, easily extensible)
- Digital twin: maintains virtual network state and history
- AI-based traffic demand prediction (scikit-learn)
- Robust error handling and logging
- Interactive Streamlit dashboard for results visualization
- Flexible configuration via JSON or CLI

---

## Architecture Overview

```
5g-digital-twin-simulator/
  simulator/
    base_station.py            # BaseStation logic
    user_equipment.py          # UserEquipment logic
    base_scheduler.py          # Abstract scheduler interface
    scheduler.py               # RoundRobinScheduler
    proportional_fair_scheduler.py # ProportionalFairScheduler
    scheduler_factory.py       # SchedulerFactory for pluggable schedulers
    simulation_engine.py       # SimulationEngine (multi-cell, metrics)
  digital_twin/
    twin_model.py              # DigitalTwin (state/history)
  ai/
    traffic_prediction.py      # ML-based demand prediction
  dashboard/
    dashboard.py               # Streamlit dashboard UI
  data/
    simulation_results.csv     # Simulation output (auto-generated)
  simulation_config.py         # Config loader
  logging_config.py            # Logging setup
  main.py                     # Entry point
  requirements.txt
  README.md
```

---

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/5g-digital-twin-simulator.git
   cd 5g-digital-twin-simulator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Simulator

**Default run (using built-in config):**
```bash
python main.py
```

**Custom configuration:**
```bash
python main.py --config path/to/config.json
```

This generates `data/simulation_results.csv` with simulation metrics.

---

## Configuration Example

Create a `config.json` file to customize simulation parameters:
```json
{
  "simulation_steps": 200,
  "users": 30,
  "total_bandwidth_mbps": 150.0,
  "scheduler": "proportional_fair",
  "output_file": "data/simulation_results.csv"
}
```

---

## Dashboard Usage

After running the simulation, launch the dashboard:
```bash
streamlit run dashboard/dashboard.py
```
- Visualizes throughput, demand, and cell load over time.
- Robust to missing or malformed data: shows warnings if results are unavailable.

---

## Scheduler Extensibility

Schedulers implement the `BaseScheduler` interface:
```python
class BaseScheduler(ABC):
    @abstractmethod
    def allocate_bandwidth(self, base_station: 'BaseStation') -> None:
        pass
```
- Add new schedulers by subclassing `BaseScheduler` and registering with `SchedulerFactory`.
- Example: `RoundRobinScheduler`, `ProportionalFairScheduler`.

---

## Logging

- Logs are written to `logs/simulator.log` and output to the console.
- Log level: INFO
- Log format: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
- Logging is configured via `logging_config.py`.

---

## Example Simulation Output

Terminal summary:
```
--- Simulation Summary ---
Timesteps: 100
Total Users: 20
Average Throughput: 85.23 Mbps
Average Cell Load: 0.92
```
Dashboard: Interactive charts for throughput, demand, and cell load.

---

## Future Work

- User mobility and handover modeling
- Inter-cell interference and advanced radio models
- Additional scheduling algorithms (e.g., Max C/I, ML-based)
- Real-time scenario editing via dashboard
- Integration with real network traces

---
