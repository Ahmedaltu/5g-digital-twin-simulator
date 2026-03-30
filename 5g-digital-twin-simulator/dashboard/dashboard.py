"""
Dashboard for 5G RAN Digital Twin Simulator.
Visualizes network performance and predictions.
"""


import streamlit as st
import pandas as pd
import logging
import sys

import os

# Required columns for simulation results
REQUIRED_COLUMNS = [
	"timestep", "base_station_id", "users", "demand", "throughput", "cell_load",
	"avg_user_throughput", "jains_fairness_index", "congestion_ratio"
]

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dashboard.log")
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
	handlers=[
		logging.FileHandler(log_file, mode='a', encoding='utf-8'),
		logging.StreamHandler()
	]
)
logger = logging.getLogger("Dashboard")

st.set_page_config(page_title="5G RAN Digital Twin Dashboard", layout="wide")


st.title("5G RAN Digital Twin Monitoring Dashboard")
st.markdown("Monitor your simulated 5G network in real time.")

# --- Sidebar: Simulation Configuration ---
st.sidebar.header("Simulation Configuration")
import json
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(project_root, "config.json")
default_config = {
	"simulation_steps": 100,
	"users": 20,
	"total_bandwidth_mbps": 100.0,
	"scheduler": "round_robin",
	"output_file": "data/simulation_results.csv"
}
try:
	with open(config_path, "r") as f:
		config_data = json.load(f)
except Exception:
	config_data = default_config.copy()
simulation_steps = st.sidebar.number_input("Simulation Steps", min_value=1, max_value=10000, value=int(config_data.get("simulation_steps", 100)), step=1)
users = st.sidebar.number_input("Number of Users", min_value=1, max_value=1000, value=int(config_data.get("users", 20)), step=1)
total_bandwidth_mbps = st.sidebar.number_input("Total Bandwidth (Mbps)", min_value=1.0, max_value=10000.0, value=float(config_data.get("total_bandwidth_mbps", 100.0)), step=1.0)
scheduler = st.sidebar.selectbox("Scheduler", ["round_robin", "proportional_fair"], index=0 if config_data.get("scheduler", "round_robin") == "round_robin" else 1)
output_file = st.sidebar.text_input("Output File", value=config_data.get("output_file", "data/simulation_results.csv"))

def run_simulation_logic():
	new_config = {
		"simulation_steps": simulation_steps,
		"users": users,
		"total_bandwidth_mbps": total_bandwidth_mbps,
		"scheduler": scheduler,
		"output_file": output_file
	}
	try:
		with open(config_path, "w") as f:
			json.dump(new_config, f, indent=2)
		st.sidebar.success("Configuration saved!")
		# Show debug info
		st.sidebar.info(f"[DEBUG] Config path: {config_path}")
		st.sidebar.info(f"[DEBUG] Output file: {output_file}")
		st.sidebar.info(f"[DEBUG] Simulation command: python {os.path.join(project_root, 'main.py')} --config {config_path} --scheduler {scheduler} --steps {simulation_steps} --users {users} --bandwidth {total_bandwidth_mbps}")
		# Automatically run simulation after saving config
		main_path = os.path.join(project_root, "main.py")
		import subprocess
		try:
			result = subprocess.run([
				sys.executable, main_path,
				"--config", config_path,
				"--scheduler", scheduler,
				"--steps", str(simulation_steps),
				"--users", str(users),
				"--bandwidth", str(total_bandwidth_mbps)
			], capture_output=True, text=True, check=False, cwd=project_root)
			st.sidebar.info(f"Simulation stdout:\n{result.stdout}")
			st.sidebar.info(f"Simulation stderr:\n{result.stderr}")
			if result.returncode == 0:
				st.sidebar.success("Simulation run with new configuration!")
			else:
				st.sidebar.error(f"Simulation failed (code {result.returncode}): {result.stderr}")
				st.sidebar.error(f"Check if the output file was written: {output_file}")
		except Exception as e:
			st.sidebar.error(f"Exception running simulation: {e}")
		st.cache_data.clear()
		st.rerun()
	except Exception as e:
		st.sidebar.error(f"Failed to save config or run simulation: {e}")

if st.sidebar.button("Save & Run Simulation"):
	run_simulation_logic()


# Load simulation results

# Load simulation results from the output_file specified in config
@st.cache_data(show_spinner="Loading simulation results...")
def load_data(current_config: dict):
	project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	# Use the output_file from config_data (already loaded above)
	output_file_path = current_config.get("output_file", "data/simulation_results.csv")
	# If not absolute, resolve relative to project root
	if not os.path.isabs(output_file_path):
		file_path = os.path.join(project_root, output_file_path)
	else:
		file_path = output_file_path
	if not os.path.exists(file_path):
		return None, file_path
	try:
		df = pd.read_csv(file_path)
	except pd.errors.EmptyDataError:
		logger.warning("Simulation results file is empty: %s", file_path)
		return pd.DataFrame(), file_path
	except Exception as e:
		logger.error("Failed to load simulation data: %s | Error: %s", file_path, str(e))
		return pd.DataFrame(), file_path
	if df.empty:
		logger.warning("Simulation results file is empty after loading: %s", file_path)
		return pd.DataFrame(), file_path
	missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
	if missing_cols:
		logger.error("Missing required columns: %s", ', '.join(missing_cols))
		return pd.DataFrame(), file_path
	return df, file_path


df, file_path = load_data(config_data)
st.markdown("---")

# If simulation results are missing, show help and run button
if df is None or (isinstance(df, pd.DataFrame) and df.empty):
	st.warning("No simulation results found.")
	st.markdown(
		"""
		**How to generate simulation results:**
		- Click the **Run Simulation** button below to generate results directly from this dashboard.
		- Or, run the following command in your terminal:
		  ```
		  python 5g-digital-twin-simulator/main.py
		  ```
		- The results file is expected at: `data/simulation_results.csv`

		**Troubleshooting:**
		- If the file is still missing after running the simulation, check for errors in the backend output.
		- If the file is empty or cannot be read, ensure the simulation completed successfully and produced valid output.
		"""
	)
	if st.button("Run Simulation with Current Settings"):
		run_simulation_logic()
else:
	# Display key metrics for the last timestep and cell
	last_row = df.iloc[-1]
	# --- Warn if config and results differ ---
	if int(last_row["users"]) != int(users):
		st.warning(f"⚠️ The number of users in the simulation results ({int(last_row['users'])}) does not match the current configuration ({int(users)}). Run the simulation to update results.")
	col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
	col1.metric("Number of Users", int(last_row["users"]))
	col2.metric("Throughput (Mbps)", f"{last_row['throughput']:.2f}")
	col3.metric("Cell Utilization", f"{last_row['cell_load']:.2f}")
	col4.metric("Avg User Throughput", f"{last_row['avg_user_throughput']:.2f}")
	col5.metric("Jain's Fairness", f"{last_row['jains_fairness_index']:.3f}")
	col6.metric("Congestion Ratio", f"{last_row['congestion_ratio']:.2f}")
	col7.metric("Traffic Demand (Mbps)", f"{last_row['demand']:.2f}")

	st.markdown("---")

	# Plots as clickable tabs
	tab_labels = [
		"Throughput Over Time",
		"Avg User Throughput Over Time",
		"Jain's Fairness Index Over Time",
		"Congestion Ratio Over Time",
		"Traffic Demand Over Time",
		"Cell Utilization Over Time"
	]
	tabs = st.tabs(tab_labels)

	with tabs[0]:
		st.line_chart(df.set_index("timestep")["throughput"])
	with tabs[1]:
		st.line_chart(df.set_index("timestep")["avg_user_throughput"])
	with tabs[2]:
		st.line_chart(df.set_index("timestep")["jains_fairness_index"])
	with tabs[3]:
		st.line_chart(df.set_index("timestep")["congestion_ratio"])
	with tabs[4]:
		st.line_chart(df.set_index("timestep")["demand"])
	with tabs[5]:
		st.line_chart(df.set_index("timestep")["cell_load"])
