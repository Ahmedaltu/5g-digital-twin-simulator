"""
Dashboard for 5G RAN Digital Twin Simulator.
Visualizes network performance and predictions.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="5G RAN Digital Twin Dashboard", layout="wide")

st.title("5G RAN Digital Twin Monitoring Dashboard")
st.markdown("Monitor your simulated 5G network in real time.")

# Load simulation results
@st.cache_data
def load_data():
	return pd.read_csv("../data/simulation_results.csv")

df = load_data()

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Number of Users", int(df["num_users"].iloc[-1]))
col2.metric("Throughput (Mbps)", f"{df['total_throughput'].iloc[-1]:.2f}")
col3.metric("Cell Load", f"{df['cell_load'].iloc[-1]:.2f}")
col4.metric("Traffic Demand (Mbps)", f"{df['total_demand'].iloc[-1]:.2f}")

st.markdown("---")

# Line charts for metrics over time
st.subheader("Throughput Over Time")
st.line_chart(df.set_index("timestep")["total_throughput"])

st.subheader("Traffic Demand Over Time")
st.line_chart(df.set_index("timestep")["total_demand"])

st.subheader("Cell Load Over Time")
st.line_chart(df.set_index("timestep")["cell_load"])
