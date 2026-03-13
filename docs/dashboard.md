# Dashboard Frontend

## Overview
The dashboard is a Streamlit web app for visualizing simulation results in real time.

## Features
- Reads `simulation_results.csv` and displays:
  - Key metrics (users, throughput, fairness, congestion, etc.)
  - Time-series charts for each KPI
- If no results are found, guides the user to run the simulation (with a button to trigger the backend)
- Provides troubleshooting tips for missing/invalid results

## Usage
- Start the dashboard with Streamlit
- View results at http://localhost:8501
