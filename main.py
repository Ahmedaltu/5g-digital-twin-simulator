"""
Main entry point for 5G RAN Digital Twin Simulator.
Runs the simulation, saves results, and prints summary statistics.
"""

import pandas as pd
from simulator.simulation_engine import SimulationEngine

def main() -> None:
	# Simulation parameters
	steps = 100
	users = 20

	# Initialize and run simulation
	engine = SimulationEngine(base_station_id=1, total_bandwidth_mbps=100.0)
	metrics = engine.run_simulation(steps=steps, users=users)

	# Save results to CSV
	df = pd.DataFrame(metrics)
	df.to_csv("data/simulation_results.csv", index=False)

	# Print summary statistics
	avg_throughput = df["total_throughput"].mean()
	avg_cell_load = df["cell_load"].mean()
	total_users = int(df["num_users"].iloc[-1])

	print("--- Simulation Summary ---")
	print(f"Timesteps: {steps}")
	print(f"Total Users: {total_users}")
	print(f"Average Throughput: {avg_throughput:.2f} Mbps")
	print(f"Average Cell Load: {avg_cell_load:.2f}")

if __name__ == "__main__":
	main()
