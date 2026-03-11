from typing import List, Dict, Any
from .kpi_utils import (
    total_throughput,
    average_user_throughput,
    cell_utilization,
    jains_fairness_index,
    congestion_ratio,
)
import logging
from .base_station import BaseStation
from .user_equipment import UserEquipment

from .scheduler_factory import SchedulerFactory


class SimulationEngine:
    """
    Runs a multi-cell 5G RAN simulation with multiple base stations, users, and pluggable schedulers.
    Collects per-cell and global performance metrics at each timestep.
    """
    def __init__(self, num_cells: int = 3, total_bandwidth_mbps: float = 100.0, scheduler_name: str = "round_robin") -> None:
        """
        Initialize the simulation engine with multiple base stations and pluggable schedulers.
        Args:
            num_cells: Number of base stations (cells) in the simulation.
            total_bandwidth_mbps: Total available bandwidth per cell in Mbps.
            scheduler_name: Name of the scheduler to use for all cells.
        """
        self.num_cells = num_cells
        self.base_stations: List[BaseStation] = []
        self.schedulers: List[Any] = []
        self.metrics: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("SimulationEngine")
        for i in range(num_cells):
            bs = BaseStation(base_station_id=i+1, total_bandwidth_mbps=total_bandwidth_mbps)
            self.base_stations.append(bs)
            scheduler = SchedulerFactory.create(scheduler_name)
            self.schedulers.append(scheduler)
            self.logger.info(f"Initialized BaseStation {bs.base_station_id} with {total_bandwidth_mbps} Mbps.")

    def run_simulation(self, steps: int, users: int) -> List[Dict[str, Any]]:
        """
        Run the simulation for a given number of steps and users, supporting multiple cells.

        Args:
            steps: Number of simulation timesteps.
            users: Number of user equipment to simulate.
        Returns:
            List of metrics dictionaries collected at each timestep for each cell.
        """
        # Initialize users and distribute across cells
        for bs in self.base_stations:
            bs.connected_users.clear()
        user_objects = [UserEquipment(user_id) for user_id in range(1, users + 1)]
        # Distribute users round-robin across cells
        for idx, ue in enumerate(user_objects):
            cell_idx = idx % self.num_cells
            self.base_stations[cell_idx].add_user(ue)
            self.logger.info(f"Assigned UserEquipment {ue.user_id} to BaseStation {self.base_stations[cell_idx].base_station_id}")

        self.metrics.clear()

        for t in range(steps):
            for cell_idx, (bs, scheduler) in enumerate(zip(self.base_stations, self.schedulers)):
                # Generate traffic demand for each user in this cell
                for ue in bs.get_connected_users():
                    ue.generate_traffic_demand()
                # Run scheduler for this cell
                scheduler.allocate_bandwidth(bs)
                # Gather per-user allocated bandwidths
                allocated_bandwidths = [ue.allocated_bandwidth_mbps for ue in bs.get_connected_users()]
                # Collect per-cell metrics
                total_demand = bs.calculate_total_demand()
                tput = total_throughput(allocated_bandwidths)
                avg_user_tput = average_user_throughput(allocated_bandwidths)
                cell_bw = bs.total_bandwidth_mbps
                utilization = cell_utilization(tput, cell_bw)
                fairness = jains_fairness_index(allocated_bandwidths)
                congestion = congestion_ratio(total_demand, cell_bw)
                metric = {
                    "timestep": t + 1,
                    "base_station_id": bs.base_station_id,
                    "users": len(bs.get_connected_users()),
                    "demand": total_demand,
                    "throughput": tput,
                    "cell_load": utilization,
                    "avg_user_throughput": avg_user_tput,
                    "jains_fairness_index": fairness,
                    "congestion_ratio": congestion
                }
                self.metrics.append(metric)
                self.logger.info(
                    f"Timestep {t+1} | Cell {bs.base_station_id} | Users: {len(bs.get_connected_users())} | "
                    f"Demand: {total_demand:.2f} | Throughput: {tput:.2f} | Utilization: {utilization:.2f} | "
                    f"AvgUserTput: {avg_user_tput:.2f} | Jain: {fairness:.3f} | Congestion: {congestion:.2f}"
                )

        # Debug: print the first metric's keys at the end of simulation
        if self.metrics:
            print("DEBUG: Metric keys:", list(self.metrics[0].keys()))
        return self.metrics
