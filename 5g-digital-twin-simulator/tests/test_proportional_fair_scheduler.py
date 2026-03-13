import pytest
from simulator.proportional_fair_scheduler import ProportionalFairScheduler
from simulator.base_station import BaseStation
from simulator.user_equipment import UserEquipment


def test_proportional_fair_scheduler_happy_path():
    # Arrange
    bs = BaseStation(base_station_id=1, total_bandwidth_mbps=100)
    users = [UserEquipment(i) for i in range(1, 6)]
    for ue in users:
        ue.traffic_demand_mbps = 20
        bs.add_user(ue)
    scheduler = ProportionalFairScheduler()
    # Act
    scheduler.allocate_bandwidth(bs)
    # Assert
    total_alloc = sum(ue.allocated_bandwidth_mbps for ue in users)
    assert total_alloc <= 100
    for ue in users:
        assert ue.allocated_bandwidth_mbps <= 20


def test_proportional_fair_scheduler_zero_bandwidth():
    # Arrange
    bs = BaseStation(base_station_id=1, total_bandwidth_mbps=0)
    users = [UserEquipment(i) for i in range(1, 3)]
    for ue in users:
        ue.traffic_demand_mbps = 10
        bs.add_user(ue)
    scheduler = ProportionalFairScheduler()
    # Act
    scheduler.allocate_bandwidth(bs)
    # Assert
    for ue in users:
        assert ue.allocated_bandwidth_mbps == 0
