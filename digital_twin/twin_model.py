"""
DigitalTwin class for 5G RAN Digital Twin Simulator.
Maintains a virtual representation of network state over time.
"""

from typing import List, Dict

class DigitalTwin:
    """
    Stores the history of network state metrics for a 5G simulation.
    """
    def __init__(self) -> None:
        """
        Initialize the DigitalTwin with an empty history.
        """
        self.history: List[Dict] = []

    def update(self, metrics: Dict) -> None:
        """
        Add a new set of metrics to the digital twin's history.

        Args:
            metrics: Dictionary containing simulation metrics (e.g., timestep, users, throughput, cell load, total demand).
        """
        self.history.append(metrics.copy())

    def get_history(self) -> List[Dict]:
        """
        Retrieve the full history of stored metrics.

        Returns:
            List of metrics dictionaries.
        """
        return self.history
