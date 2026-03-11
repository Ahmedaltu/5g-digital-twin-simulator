import os
import sys
import pytest

# Ensure the simulator package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.kpi_utils import total_throughput, average_user_throughput, cell_utilization, jains_fairness_index, congestion_ratio

def test_total_throughput():
    assert total_throughput([1, 2, 3]) == 6
    assert total_throughput([]) == 0

def test_average_user_throughput():
    assert average_user_throughput([2, 4, 6]) == 4
    assert average_user_throughput([]) == 0

def test_cell_utilization():
    assert cell_utilization(50, 100) == 0.5
    assert cell_utilization(0, 0) == 0

def test_jains_fairness_index():
    assert jains_fairness_index([10, 10, 10]) == 1.0
    assert round(jains_fairness_index([10, 0]), 2) == 0.5
    assert jains_fairness_index([]) == 0

def test_congestion_ratio():
    assert congestion_ratio(100, 200) == 0.5
    assert congestion_ratio(0, 0) == 0
