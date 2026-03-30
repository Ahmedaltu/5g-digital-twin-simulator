import pytest
import pandas as pd
from simulator.metrics import (
    calculate_total_throughput,
    calculate_average_user_throughput,
    calculate_cell_utilization,
    calculate_congestion_ratio,
    calculate_jains_fairness_index
)

class DummyUser:
    def __init__(self, allocated_bandwidth):
        self.allocated_bandwidth = allocated_bandwidth

@pytest.mark.parametrize("bandwidths,expected", [
    ([10, 20, 30], 60),
    ([0, 0, 0], 0),
    ([5], 5),
])
def test_calculate_total_throughput_happy_path(bandwidths, expected):
    users = [DummyUser(bw) for bw in bandwidths]
    result = calculate_total_throughput(users)
    assert result == expected

@pytest.mark.parametrize("bandwidths,expected", [
    ([10, 20, 30], 20),
    ([0, 0, 0], 0),
    ([5], 5),
    ([], 0),
])
def test_calculate_average_user_throughput_happy_path(bandwidths, expected):
    users = [DummyUser(bw) for bw in bandwidths]
    result = calculate_average_user_throughput(users)
    assert result == expected

@pytest.mark.parametrize("throughput,bandwidth,expected", [
    (50, 100, 0.5),
    (0, 100, 0),
    (100, 0, 0),
])
def test_calculate_cell_utilization_happy_path(throughput, bandwidth, expected):
    result = calculate_cell_utilization(throughput, bandwidth)
    assert result == expected

@pytest.mark.parametrize("demand,bandwidth,expected", [
    (120, 100, 1.2),
    (0, 100, 0),
    (100, 0, 0),
])
def test_calculate_congestion_ratio_happy_path(demand, bandwidth, expected):
    result = calculate_congestion_ratio(demand, bandwidth)
    assert result == expected

@pytest.mark.parametrize("bandwidths,expected", [
    ([10, 10, 10], 1.0),
    ([10, 20, 30], pytest.approx(0.8571, rel=1e-3)),
    ([0, 0, 0], 0),
    ([], 0),
])
def test_calculate_jains_fairness_index_happy_path(bandwidths, expected):
    users = [DummyUser(bw) for bw in bandwidths]
    result = calculate_jains_fairness_index(users)
    assert result == expected

# Edge cases

def test_calculate_total_throughput_empty():
    assert calculate_total_throughput([]) == 0

def test_calculate_average_user_throughput_empty():
    assert calculate_average_user_throughput([]) == 0

def test_calculate_jains_fairness_index_empty():
    assert calculate_jains_fairness_index([]) == 0

def test_calculate_cell_utilization_zero_bandwidth():
    assert calculate_cell_utilization(100, 0) == 0

def test_calculate_congestion_ratio_zero_bandwidth():
    assert calculate_congestion_ratio(100, 0) == 0
