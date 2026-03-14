"""
RoundRobinScheduler module for 5G RAN Digital Twin Simulator.
Implements a simple round-robin radio resource allocation strategy.
"""


from typing import TYPE_CHECKING
from .base_scheduler import BaseScheduler

if TYPE_CHECKING:
    from .base_station import BaseStation
    from .user_equipment import UserEquipment

class RoundRobinScheduler(BaseScheduler):
    """
    Scheduler that allocates equal bandwidth to all connected users (Round Robin).
    Implements the BaseScheduler interface for 5G network simulation.
    """
    def allocate_bandwidth(self, base_station: 'BaseStation') -> None:
        """
        Allocate equal bandwidth to all connected users, not exceeding their traffic demand.
        Updates each UserEquipment's allocated_bandwidth_mbps.
        Args:
            base_station (BaseStation): The base station to allocate bandwidth for.
        """
        users = getattr(base_station, 'connected_users', [])
        total_bandwidth = getattr(base_station, 'total_bandwidth_mbps', 0.0)
        num_users = len(users)
        if num_users == 0 or total_bandwidth <= 0:
            return
        equal_share = total_bandwidth / num_users
        for ue in users:
            demand = getattr(ue, 'traffic_demand_mbps', 0.0)
            allocated = min(equal_share, demand)
            ue.allocated_bandwidth_mbps = allocated

    def calculate_total_throughput(self, base_station: 'BaseStation') -> float:
        """
        Calculate the total throughput for the given base station.
        Args:
            base_station (BaseStation): The base station to calculate throughput for.
        Returns:
            float: The total throughput in Mbps.
        """
        return sum(getattr(ue, 'allocated_bandwidth_mbps', 0.0) for ue in getattr(base_station, 'connected_users', []))
