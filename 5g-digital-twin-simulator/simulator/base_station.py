"""
BaseStation class for 5G RAN Digital Twin Simulator.
"""

from typing import List
from .user_equipment import UserEquipment


class BaseStation:
    """
    Represents a simplified 5G base station (gNodeB) managing connected user equipment.
    """

    def __init__(self, base_station_id: int, total_bandwidth_mbps: float) -> None:
        """
        Initialize the base station.

        Args:
            base_station_id: Unique identifier for the base station
            total_bandwidth_mbps: Total available bandwidth in Mbps
        """
        self.base_station_id: int = base_station_id
        self.total_bandwidth_mbps: float = total_bandwidth_mbps
        self.connected_users: List[UserEquipment] = []

    def add_user(self, ue: UserEquipment) -> None:
        """
        Add a UserEquipment object to the base station if not already connected.
        """
        if ue not in self.connected_users:
            self.connected_users.append(ue)

    def remove_user(self, ue: UserEquipment) -> None:
        """
        Remove a UserEquipment object from the base station.
        """
        if ue in self.connected_users:
            self.connected_users.remove(ue)

    def get_connected_users(self) -> List[UserEquipment]:
        """
        Return the list of connected users.
        """
        return self.connected_users

    def calculate_total_demand(self) -> float:
        """
        Calculate total traffic demand from all connected users.

        Returns:
            Total demand in Mbps
        """
        return sum(user.traffic_demand_mbps for user in self.connected_users)

    def calculate_cell_load(self) -> float:
        """
        Calculate the current cell load.

        Returns:
            Load ratio (0–1+)
        """
        if self.total_bandwidth_mbps == 0:
            return 0.0

        total_demand = self.calculate_total_demand()
        return total_demand / self.total_bandwidth_mbps

    def __repr__(self) -> str:
        return (
            f"BaseStation(id={self.base_station_id}, "
            f"users={len(self.connected_users)}, "
            f"bandwidth={self.total_bandwidth_mbps} Mbps)"
        )
