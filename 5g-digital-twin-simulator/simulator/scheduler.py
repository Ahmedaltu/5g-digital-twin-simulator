"""
RoundRobinScheduler module for 5G RAN Digital Twin Simulator.
Implements a simple round-robin radio resource allocation strategy.
"""

from typing import Optional
from .base_station import BaseStation
from .user_equipment import UserEquipment

class RoundRobinScheduler:
    """
    Allocates bandwidth equally among all connected users in a base station.
    """
    def __init__(self, base_station: BaseStation) -> None:
        """
        Initialize the scheduler with a BaseStation object.
        """
        self.base_station: BaseStation = base_station

    def reset_allocations(self) -> None:
        """
        Reset allocated bandwidth for all connected users to zero.
        """
        for ue in self.base_station.get_connected_users():
            ue.update_allocated_bandwidth(0.0)

    def allocate_bandwidth(self) -> None:
        """
        Allocate bandwidth equally among all connected users, without exceeding each user's demand.
        """
        users = self.base_station.get_connected_users()
        n_users = len(users)
        if n_users == 0:
            return
        equal_share = self.base_station.total_bandwidth_mbps / n_users
        for ue in users:
            allocation = min(equal_share, ue.traffic_demand_mbps)
            ue.update_allocated_bandwidth(allocation)

    def calculate_total_throughput(self) -> float:
        """
        Calculate the total throughput achieved by all users (sum of allocated bandwidths).
        Returns:
            Total throughput in Mbps.
        """
        return sum(ue.allocated_bandwidth_mbps for ue in self.base_station.get_connected_users())
