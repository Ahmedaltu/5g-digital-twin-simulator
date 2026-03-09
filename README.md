# 5G RAN Digital Twin Simulator

A research-grade Python simulation platform for 5G RAN digital twin modeling, radio access network (RAN) scheduling, AI-based traffic prediction, and dashboard visualization.

---

## Features

- Simulates 5G RAN with user equipment (UE), base stations, and traffic
- Implements Round Robin and Proportional Fair scheduling
- Maintains a digital twin (virtual network state/history)
- Tracks performance metrics: throughput, cell load, demand, users
- Predicts traffic demand using scikit-learn (LinearRegression)
- Visualizes results with a Streamlit dashboard

---

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

## Project Structure

```
5g-digital-twin-simulator/
  simulator/         # Core simulation modules
    base_station.py      # BaseStation class
    user_equipment.py    # UserEquipment class
    scheduler.py         # RoundRobinScheduler and scheduling logic
    simulation_engine.py # SimulationEngine (main simulation loop)
  digital_twin/
    twin_model.py        # DigitalTwin (network state/history)
  ai/
    traffic_prediction.py # TrafficPredictor (ML-based demand prediction)
  dashboard/
    dashboard.py         # Streamlit dashboard UI
  data/
    simulation_results.csv # Simulation output (auto-generated)
  main.py               # Main entry point
  requirements.txt      # Python dependencies
  README.md
```

---

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the simulation:**
   ```bash
   python main.py
   ```
   This will generate `data/simulation_results.csv` with simulation metrics.
3. **Launch the dashboard:**
   ```bash
   streamlit run dashboard/dashboard.py
   ```
   The dashboard visualizes throughput, demand, and cell load over time.

---

## Usage Example

After running the simulation, you’ll see summary statistics in the terminal:

```
--- Simulation Summary ---
Timesteps: 100
Total Users: 20
Average Throughput: 85.23 Mbps
Average Cell Load: 0.92
```

Open the dashboard to explore results interactively.

---

## Module Overview

- **simulator/user_equipment.py**: Models a mobile device generating traffic demand.
- **simulator/base_station.py**: Manages connected users and bandwidth allocation.
- **simulator/scheduler.py**: Implements scheduling algorithms (e.g., Round Robin).
- **simulator/simulation_engine.py**: Runs the simulation and collects metrics.
- **digital_twin/twin_model.py**: Stores network state history (digital twin).
- **ai/traffic_prediction.py**: Predicts future demand using machine learning.
- **dashboard/dashboard.py**: Streamlit dashboard for visualization.

---

## License

This project is released under the MIT License.

---

## Contributing

Pull requests and issues are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact

For questions or collaboration, please contact the project maintainer.
