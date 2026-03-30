"""
KPI calculation module for 5G RAN Digital Twin Simulator.
Provides functions to compute throughput, utilization, congestion, and fairness metrics.
"""

from typing import List

def calculate_total_throughput(users: List) -> float:
    """
    Sum of allocated bandwidth across all connected users.
    """
    return sum(getattr(u, 'allocated_bandwidth', 0.0) for u in users)

def calculate_average_user_throughput(users: List) -> float:
    """
    Total throughput divided by number of users.
    """
    n = len(users)
    if n == 0:
        return 0.0
    return calculate_total_throughput(users) / n

def calculate_cell_utilization(total_throughput: float, total_bandwidth_mbps: float) -> float:
    """
    Throughput divided by total cell bandwidth.
    """
    if total_bandwidth_mbps == 0:
        return 0.0
    return total_throughput / total_bandwidth_mbps

def calculate_congestion_ratio(total_demand: float, total_bandwidth_mbps: float) -> float:
    """
    Total demand divided by total cell bandwidth.
    """
    if total_bandwidth_mbps == 0:
        return 0.0
    return total_demand / total_bandwidth_mbps

def calculate_jains_fairness_index(users: List) -> float:
    """
    Jain’s fairness index for allocated user bandwidth values.
    """
    allocations = [getattr(u, 'allocated_bandwidth', 0.0) for u in users]
    n = len(allocations)
    if n == 0:
        return 0.0
    numerator = (sum(allocations)) ** 2
    denominator = n * sum(a ** 2 for a in allocations)
    if denominator == 0:
        return 0.0
    return numerator / denominator
