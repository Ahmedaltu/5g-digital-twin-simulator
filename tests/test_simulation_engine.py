import os
import sys
import pandas as pd
import pytest

# Ensure the simulator package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.simulation_engine import SimulationEngine

def test_simulation_engine_run_simulation():
    engine = SimulationEngine(num_cells=1, total_bandwidth_mbps=100.0, scheduler_name="round_robin")
    metrics = engine.run_simulation(steps=10, users=5)
    assert isinstance(metrics, list)
    assert len(metrics) == 10  # 10 timesteps, 1 cell
    for entry in metrics:
        assert 'timestep' in entry
        assert 'base_station_id' in entry
        assert 'users' in entry
        assert 'throughput' in entry
        assert 'cell_load' in entry
        assert 'demand' in entry

def test_simulation_output_kpi_columns(tmp_path):
    # Arrange
    output_file = tmp_path / "simulation_results.csv"
    engine = SimulationEngine(num_cells=1, total_bandwidth_mbps=100.0, scheduler_name="round_robin")
    metrics = engine.run_simulation(steps=5, users=10)
    df = pd.DataFrame(metrics)
    df.to_csv(output_file, index=False)

    # Act
    df_loaded = pd.read_csv(output_file)
    required_columns = [
        "timestep", "base_station_id", "users", "demand", "throughput", "cell_load",
        "avg_user_throughput", "jains_fairness_index", "congestion_ratio"
    ]

    # Assert
    for col in required_columns:
        assert col in df_loaded.columns, f"Missing column: {col}"

def test_simulation_zero_users(tmp_path):
    output_file = tmp_path / "simulation_results.csv"
    engine = SimulationEngine(num_cells=1, total_bandwidth_mbps=100.0, scheduler_name="round_robin")
    metrics = engine.run_simulation(steps=3, users=0)
    df = pd.DataFrame(metrics)
    df.to_csv(output_file, index=False)
    df_loaded = pd.read_csv(output_file)
    assert df_loaded["users"].eq(0).all()
    assert (df_loaded["throughput"] == 0).all()

def test_simulation_high_bandwidth(tmp_path):
    output_file = tmp_path / "simulation_results.csv"
    engine = SimulationEngine(num_cells=1, total_bandwidth_mbps=1e6, scheduler_name="round_robin")
    metrics = engine.run_simulation(steps=2, users=5)
    df = pd.DataFrame(metrics)
    df.to_csv(output_file, index=False)
    df_loaded = pd.read_csv(output_file)
    assert (df_loaded["cell_load"] < 1).all()
