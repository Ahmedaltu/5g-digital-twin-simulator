import pytest
from simulator.user_equipment import UserEquipment

def test_user_equipment_generate_traffic_demand():
    # Arrange
    ue = UserEquipment(1)
    # Act
    demand = ue.generate_traffic_demand(min_demand=5, max_demand=5)
    # Assert
    assert demand == 5
    assert ue.traffic_demand_mbps == 5


def test_user_equipment_update_allocated_bandwidth():
    # Arrange
    ue = UserEquipment(2)
    # Act
    ue.update_allocated_bandwidth(15)
    # Assert
    assert ue.allocated_bandwidth_mbps == 15


def test_user_equipment_get_utilization():
    # Arrange
    ue = UserEquipment(3)
    ue.traffic_demand_mbps = 10
    ue.allocated_bandwidth_mbps = 5
    # Act
    utilization = ue.get_utilization()
    # Assert
    assert utilization == 0.5


def test_user_equipment_get_utilization_zero_demand():
    # Arrange
    ue = UserEquipment(4)
    ue.traffic_demand_mbps = 0
    ue.allocated_bandwidth_mbps = 10
    # Act
    utilization = ue.get_utilization()
    # Assert
    assert utilization == 0.0
