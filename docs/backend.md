# Backend Simulation Engine

## Overview
The backend simulates a 5G Radio Access Network (RAN), modeling users, base stations, and network resource allocation over time.

## Key Components
- **User Equipment (UE):** Simulates mobile users/devices.
- **Base Station:** Simulates a 5G cell site serving users.
- **Scheduler:** Allocates bandwidth/resources to users (supports multiple algorithms).
- **Simulation Engine:** Orchestrates the simulation, advances time steps, updates state, and collects KPIs.

## Simulation Flow
1. Loads configuration from `config.json`.
2. For each time step:
   - Updates user demand and network state.
   - Runs the scheduler.
   - Calculates KPIs (throughput, fairness, congestion, etc.).
   - Logs results.
3. Writes results to `data/simulation_results.csv`.

## KPIs Tracked
- Number of users
- Throughput
- Cell load
- Jain’s fairness index
- Congestion ratio
- Traffic demand
