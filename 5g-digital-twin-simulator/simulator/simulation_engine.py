"""
SimulationEngine class for 5G RAN Digital Twin Simulator.
Coordinates the simulation of a base station, user equipment, and scheduler.
"""

from typing import List, Dict
from .base_station import BaseStation
from .user_equipment import UserEquipment
from .scheduler import RoundRobinScheduler

class SimulationEngine:
	"""
	Runs a simplified 5G RAN simulation with a base station, users, and scheduler.
	Collects performance metrics at each timestep.
	"""
	def __init__(self, base_station_id: int = 1, total_bandwidth_mbps: float = 100.0) -> None:
		"""
		Initialize the simulation engine with a base station.
		"""
		self.base_station = BaseStation(base_station_id, total_bandwidth_mbps)
		self.scheduler = RoundRobinScheduler(self.base_station)
		self.metrics: List[Dict[str, float]] = []

	def run_simulation(self, steps: int, users: int) -> List[Dict[str, float]]:
		"""
		Run the simulation for a given number of steps and users.

		Args:
			steps: Number of simulation timesteps.
			users: Number of user equipment to simulate.
		Returns:
			List of metrics dictionaries collected at each timestep.
		"""
		# Initialize users
		self.base_station.connected_users.clear()
		for user_id in range(1, users + 1):
			ue = UserEquipment(user_id)
			self.base_station.add_user(ue)

		self.metrics.clear()

		for t in range(steps):
			# Generate traffic demand for each user
			for ue in self.base_station.get_connected_users():
				ue.generate_traffic_demand()

			# Run scheduler
			self.scheduler.allocate_bandwidth()

			# Collect metrics
			total_demand = self.base_station.calculate_total_demand()
			total_throughput = self.scheduler.calculate_total_throughput()
			cell_load = self.base_station.calculate_cell_load()
			metric = {
				"timestep": t + 1,
				"num_users": len(self.base_station.get_connected_users()),
				"total_demand": total_demand,
				"total_throughput": total_throughput,
				"cell_load": cell_load
			}
			self.metrics.append(metric)

		return self.metrics
