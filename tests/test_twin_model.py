import pytest
from digital_twin.twin_model import DigitalTwin

def test_digital_twin_update_and_history():
    # Arrange
    twin = DigitalTwin()
    metrics = {"timestep": 1, "users": 5, "throughput": 100.0}
    # Act
    twin.update(metrics)
    # Assert
    history = twin.get_history()
    assert isinstance(history, list)
    assert history[0]["timestep"] == 1
    assert history[0]["users"] == 5
    assert history[0]["throughput"] == 100.0


def test_digital_twin_multiple_updates():
    # Arrange
    twin = DigitalTwin()
    for i in range(3):
        twin.update({"timestep": i+1, "users": i*2, "throughput": i*10.0})
    # Act
    history = twin.get_history()
    # Assert
    assert len(history) == 3
    assert history[2]["timestep"] == 3
    assert history[2]["users"] == 4
    assert history[2]["throughput"] == 20.0
