"""
KPI calculation utilities for 5G RAN Digital Twin Simulator.
"""
from typing import List
import math

def total_throughput(allocated_bandwidths: List[float]) -> float:
    """Sum of allocated bandwidth across all users."""
    return sum(allocated_bandwidths)

def average_user_throughput(allocated_bandwidths: List[float]) -> float:
    """Total throughput divided by number of users."""
    if not allocated_bandwidths:
        return 0.0
    return sum(allocated_bandwidths) / len(allocated_bandwidths)

def cell_utilization(throughput: float, total_bandwidth: float) -> float:
    """Throughput divided by total cell bandwidth."""
    if total_bandwidth == 0:
        return 0.0
    return throughput / total_bandwidth

def jains_fairness_index(allocated_bandwidths: List[float]) -> float:
    """Jain's Fairness Index for allocated bandwidths."""
    n = len(allocated_bandwidths)
    if n == 0:
        return 0.0
    numerator = sum(allocated_bandwidths) ** 2
    denominator = n * sum(b ** 2 for b in allocated_bandwidths)
    if denominator == 0:
        return 0.0
    return numerator / denominator

def congestion_ratio(total_demand: float, total_bandwidth: float) -> float:
    """Total demand divided by total bandwidth."""
    if total_bandwidth == 0:
        return 0.0
    return total_demand / total_bandwidth
