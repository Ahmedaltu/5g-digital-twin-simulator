from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_station import BaseStation

class BaseScheduler(ABC):
    """
    Abstract base class for schedulers in a 5G network simulator.
    Allows different scheduling algorithms to be interchangeable.
    """

    @abstractmethod
    def allocate_bandwidth(self, base_station: 'BaseStation') -> None:
        """
        Allocate bandwidth to user equipment connected to the base station.
        Must be implemented by subclasses.
        Args:
            base_station (BaseStation): The base station to allocate bandwidth for.
        """
        pass

    def calculate_total_throughput(self, base_station: 'BaseStation') -> float:
        """
        Calculate the total throughput for the given base station.
        Args:
            base_station (BaseStation): The base station to calculate throughput for.
        Returns:
            float: The total throughput in Mbps.
        """
        return sum(ue.throughput for ue in base_station.connected_ues)
