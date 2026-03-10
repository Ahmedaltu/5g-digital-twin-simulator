from typing import TYPE_CHECKING, Dict
from .base_scheduler import BaseScheduler

if TYPE_CHECKING:
    from .base_station import BaseStation
    from .user_equipment import UserEquipment

class ProportionalFairScheduler(BaseScheduler):
    """
    Scheduler that allocates bandwidth based on proportional fairness.
    Users with higher demand relative to their past throughput receive higher priority.
    Implements the BaseScheduler interface for 5G network simulation.
    """
    def __init__(self) -> None:
        """
        Initialize the ProportionalFairScheduler with a throughput history tracker.
        """
        self.past_throughput: Dict[int, float] = {}

    def allocate_bandwidth(self, base_station: 'BaseStation') -> None:
        """
        Allocate bandwidth to users based on the ratio of demand to average past throughput.
        Args:
            base_station (BaseStation): The base station to allocate bandwidth for.
        """
        users = getattr(base_station, 'connected_users', [])
        total_bandwidth = getattr(base_station, 'total_bandwidth_mbps', 0.0)
        if not users or total_bandwidth <= 0:
            return
        # Calculate proportional fair metric for each user
        pf_metrics = []
        for ue in users:
            user_id = getattr(ue, 'user_id', None)
            demand = getattr(ue, 'traffic_demand_mbps', 0.0)
            past = self.past_throughput.get(user_id, 1e-6)  # Avoid division by zero
            pf_metric = demand / past
            pf_metrics.append((ue, pf_metric, demand))
        # Sort users by PF metric (descending)
        pf_metrics.sort(key=lambda x: x[1], reverse=True)
        remaining_bw = total_bandwidth
        for ue, _, demand in pf_metrics:
            alloc = min(demand, remaining_bw)
            ue.allocated_bandwidth_mbps = alloc
            remaining_bw -= alloc
            if remaining_bw <= 0:
                break

    def update_past_throughput(self, base_station: 'BaseStation') -> None:
        """
        Update the throughput history for each user after allocation.
        Args:
            base_station (BaseStation): The base station whose users' throughput to update.
        """
        users = getattr(base_station, 'connected_users', [])
        for ue in users:
            user_id = getattr(ue, 'user_id', None)
            throughput = getattr(ue, 'allocated_bandwidth_mbps', 0.0)
            # Use exponential moving average for past throughput
            prev = self.past_throughput.get(user_id, 0.0)
            self.past_throughput[user_id] = 0.8 * prev + 0.2 * throughput

    def calculate_total_throughput(self, base_station: 'BaseStation') -> float:
        """
        Calculate the total throughput for the given base station.
        Args:
            base_station (BaseStation): The base station to calculate throughput for.
        Returns:
            float: The total throughput in Mbps.
        """
        return sum(getattr(ue, 'allocated_bandwidth_mbps', 0.0) for ue in getattr(base_station, 'connected_users', []))
