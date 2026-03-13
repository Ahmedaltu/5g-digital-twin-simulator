# Simulation Logic Details

## 1. Initialization
- Loads simulation parameters from `config.json` (steps, users, bandwidth, scheduler type).
- Instantiates user equipment (UE) and base station objects.
- Selects the scheduler algorithm (e.g., proportional fair).

## 2. Time Step Loop
For each time step:
- **User Demand Update:**
  - Each UE generates a new traffic demand (random or based on a model).
- **Resource Scheduling:**
  - The scheduler allocates available bandwidth among users based on their demand and the chosen algorithm.
  - Example: Proportional fair scheduler balances throughput and fairness.
- **KPI Calculation:**
  - Throughput: Actual data delivered to each user and total.
  - Cell Load: Fraction of total bandwidth used.
  - Jain’s Fairness Index: Measures how evenly resources are distributed.
  - Congestion Ratio: Demand vs. available resources.
- **Logging:**
  - All KPIs and state variables are recorded for this time step.

## 3. Output
- After all steps, results are written to `simulation_results.csv` for dashboard visualization.

## 4. Modularity
- Schedulers and user models are modular—new algorithms or behaviors can be added easily.
- The simulation engine is decoupled from the dashboard (integration via CSV file).

## 5. Example Pseudocode
```
for t in range(simulation_steps):
    for ue in users:
        ue.update_demand()
    scheduler.allocate(users, base_station)
    kpis = calculate_kpis(users, base_station)
    log_results(t, kpis)
write_results_to_csv()
```

---

This logic enables experimentation with different network scenarios, user behaviors, and scheduling strategies.
