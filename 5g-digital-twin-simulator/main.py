"""
Main entry point for 5G RAN Digital Twin Simulator.
Runs the simulation, saves results, and prints summary statistics.
"""



import argparse
import os
import pandas as pd
from simulator.simulation_engine import SimulationEngine
from simulation_config import SimulationConfig


def main():
	parser = argparse.ArgumentParser(description="5G RAN Digital Twin Simulator")
	parser.add_argument('--config', type=str, default='config.json', help='Path to config file (JSON)')
	parser.add_argument('--scheduler', type=str, help='Scheduler type (round_robin, proportional_fair)')
	parser.add_argument('--steps', type=int, help='Number of simulation steps')
	parser.add_argument('--users', type=int, help='Number of users')
	parser.add_argument('--bandwidth', type=float, help='Total bandwidth in Mbps')
	args = parser.parse_args()

	# Load config from file
	config = SimulationConfig.load_from_file(args.config)

	# Override config with CLI arguments if provided
	scheduler = args.scheduler if args.scheduler else getattr(config, 'scheduler', 'round_robin')
	steps = args.steps if args.steps is not None else getattr(config, 'simulation_steps', 100)
	users = args.users if args.users is not None else getattr(config, 'users', 20)
	bandwidth = args.bandwidth if args.bandwidth is not None else getattr(config, 'total_bandwidth_mbps', 100.0)
	output_file = getattr(config, 'output_file', 'data/simulation_results.csv')

	# Initialize and run simulation
	engine = SimulationEngine(num_cells=1, total_bandwidth_mbps=bandwidth, scheduler_name=scheduler)
	metrics = engine.run_simulation(steps=steps, users=users)

	# Save results to CSV with error handling (robust: delete file first)
	df = pd.DataFrame(metrics)
	try:
		os.makedirs(os.path.dirname(output_file), exist_ok=True)
		df.to_csv(output_file, index=False)
		print(f"DEBUG: Wrote simulation results to {os.path.abspath(output_file)}")
	except Exception as e:
		print(f"Error saving simulation results: {e}")
		return

	# Print summary statistics (updated column names)
	if df.empty:
		print("No metrics recorded during simulation.")
		return

	avg_throughput = df["throughput"].mean()
	avg_cell_load = df["cell_load"].mean()
	total_users = int(df["users"].iloc[-1])

	print("--- Simulation Summary ---")
	print(f"Timesteps: {steps}")
	print(f"Total Users: {total_users}")
	print(f"Average Throughput: {avg_throughput:.2f} Mbps")
	print(f"Average Cell Load: {avg_cell_load:.2f}")

if __name__ == "__main__":
	main()
