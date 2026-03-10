import json
from typing import Optional

class SimulationConfig:
    """
    Loads and stores configuration parameters for the 5G Digital Twin Simulator.
    Provides default values if fields are missing in the config file.
    """
    def __init__(
        self,
        simulation_steps: int = 100,
        users: int = 20,
        total_bandwidth_mbps: float = 100.0,
        scheduler: str = "round_robin",
        output_file: str = "data/simulation_results.csv"
    ) -> None:
        self.simulation_steps = simulation_steps
        self.users = users
        self.total_bandwidth_mbps = total_bandwidth_mbps
        self.scheduler = scheduler
        self.output_file = output_file

    @staticmethod
    def load_from_file(path: str) -> 'SimulationConfig':
        """
        Load configuration from a JSON file, providing defaults for missing fields.
        Args:
            path (str): Path to the JSON config file.
        Returns:
            SimulationConfig: Loaded configuration object.
        """
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
        return SimulationConfig(
            simulation_steps=data.get('simulation_steps', 100),
            users=data.get('users', 20),
            total_bandwidth_mbps=data.get('total_bandwidth_mbps', 100.0),
            scheduler=data.get('scheduler', 'round_robin'),
            output_file=data.get('output_file', 'data/simulation_results.csv')
        )
