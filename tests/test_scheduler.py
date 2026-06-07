import pytest
from simulator.scheduler import RoundRobinScheduler
from simulator.base_station import BaseStation
from simulator.user_equipment import UserEquipment


def test_scheduler_allocate_bandwidth_happy_path():
    # Arrange
    bs = BaseStation(base_station_id=1, total_bandwidth_mbps=100)
    users = [UserEquipment(i) for i in range(1, 6)]
    for ue in users:
        ue.traffic_demand_mbps = 20
        bs.add_user(ue)
    scheduler = RoundRobinScheduler()
    # Act
    scheduler.allocate_bandwidth(bs)
    # Assert
    for ue in users:
        assert ue.allocated_bandwidth_mbps == 20


def test_scheduler_allocate_bandwidth_zero_users():
    # Arrange
    bs = BaseStation(base_station_id=1, total_bandwidth_mbps=100)
    scheduler = RoundRobinScheduler()
    # Act
    scheduler.allocate_bandwidth(bs)
    # Assert
    assert len(bs.connected_users) == 0


def test_scheduler_allocate_bandwidth_low_bandwidth():
    # Arrange
    bs = BaseStation(base_station_id=1, total_bandwidth_mbps=10)
    users = [UserEquipment(i) for i in range(1, 6)]
    for ue in users:
        ue.traffic_demand_mbps = 20
        bs.add_user(ue)
    scheduler = RoundRobinScheduler()
    # Act
    scheduler.allocate_bandwidth(bs)
    # Assert
    for ue in users:
        assert ue.allocated_bandwidth_mbps <= 10 / 5
