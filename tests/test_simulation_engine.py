import pytest
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
