"""
Dashboard for 5G RAN Digital Twin Simulator.
Visualizes network performance and predictions.
"""


import streamlit as st
import pandas as pd
import logging

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

# Load simulation results
@st.cache_data
def load_data():
	# Always resolve the path from the project root
	project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(project_root, "data", "simulation_results.csv")
	if not os.path.exists(file_path):
		st.warning("No simulation results found. Run the simulator first.")
		logger.warning("Simulation results file not found: %s", file_path)
		return pd.DataFrame()
	try:
		df = pd.read_csv(file_path)
	except pd.errors.EmptyDataError:
		st.warning("Simulation results file is empty.")
		logger.warning("Simulation results file is empty: %s", file_path)
		return pd.DataFrame()
	except Exception as e:
		st.error("Failed to load simulation data. The results file may be corrupted.")
		logger.error("Failed to load simulation data: %s | Error: %s", file_path, str(e))
		return pd.DataFrame()
	if df.empty:
		st.warning("Simulation results file is empty.")
		logger.warning("Simulation results file is empty after loading: %s", file_path)
		return pd.DataFrame()
	missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
	if missing_cols:
		st.error(f"Simulation results are missing required columns: {', '.join(missing_cols)}")
		logger.error("Missing required columns: %s", ', '.join(missing_cols))
		return pd.DataFrame()
	return df


df = load_data()
st.markdown("---")

# Only render charts and metrics if data is available
if not df.empty:
	# Display key metrics for the last timestep and cell
	last_row = df.iloc[-1]
	col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
	col1.metric("Number of Users", int(last_row["users"]))
	col2.metric("Throughput (Mbps)", f"{last_row['throughput']:.2f}")
	col3.metric("Cell Utilization", f"{last_row['cell_load']:.2f}")
	col4.metric("Avg User Throughput", f"{last_row['avg_user_throughput']:.2f}")
	col5.metric("Jain's Fairness", f"{last_row['jains_fairness_index']:.3f}")
	col6.metric("Congestion Ratio", f"{last_row['congestion_ratio']:.2f}")
	col7.metric("Traffic Demand (Mbps)", f"{last_row['demand']:.2f}")

	st.markdown("---")

	# Line charts for metrics over time (all cells)
	st.subheader("Throughput Over Time")
	st.line_chart(df.set_index("timestep")["throughput"])

	st.subheader("Avg User Throughput Over Time")
	st.line_chart(df.set_index("timestep")["avg_user_throughput"])

	st.subheader("Jain's Fairness Index Over Time")
	st.line_chart(df.set_index("timestep")["jains_fairness_index"])

	st.subheader("Congestion Ratio Over Time")
	st.line_chart(df.set_index("timestep")["congestion_ratio"])

	st.subheader("Traffic Demand Over Time")
	st.line_chart(df.set_index("timestep")["demand"])

	st.subheader("Cell Utilization Over Time")
	st.line_chart(df.set_index("timestep")["cell_load"])
