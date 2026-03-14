"""
UserEquipment class for 5G RAN Digital Twin Simulator.
Represents a mobile device generating traffic demand in a simplified 5G network simulation.
"""

import random

class UserEquipment:
    """
    Represents a mobile device (UE) in a 5G RAN simulation environment.
    """
    def __init__(self, user_id: int):
        """
        Initialize a UserEquipment instance.

        Args:
            user_id: Unique identifier for the user equipment.
        """
        self.user_id: int = user_id
        self.traffic_demand_mbps: float = 0.0
        self.allocated_bandwidth_mbps: float = 0.0

    def generate_traffic_demand(self, min_demand: float = 1.0, max_demand: float = 10.0) -> float:
        """
        Randomly generate traffic demand in Mbps for the UE.

        Args:
            min_demand: Minimum possible demand in Mbps.
            max_demand: Maximum possible demand in Mbps.
        Returns:
            The generated traffic demand in Mbps.
        """
        self.traffic_demand_mbps = random.uniform(min_demand, max_demand)
        return self.traffic_demand_mbps

    def update_allocated_bandwidth(self, bandwidth: float) -> None:
        """
        Update the allocated bandwidth for the UE.

        Args:
            bandwidth: Allocated bandwidth in Mbps.
        """
        self.allocated_bandwidth_mbps = bandwidth

    def get_utilization(self) -> float:
        """
        Calculate the utilization ratio of allocated bandwidth to traffic demand.

        Returns:
            Utilization as a float (0.0 if demand is zero).
        """
        if self.traffic_demand_mbps == 0:
            return 0.0
        return self.allocated_bandwidth_mbps / self.traffic_demand_mbps

    def __repr__(self) -> str:
        return (
            f"UserEquipment(id={self.user_id}, "
            f"demand={self.traffic_demand_mbps:.2f} Mbps, "
            f"allocated={self.allocated_bandwidth_mbps:.2f} Mbps)"
        )
