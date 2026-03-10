import pytest
import pandas as pd
from ai.traffic_prediction import TrafficPredictor


def test_traffic_predictor_train_and_predict():
    # Create dummy data
    df = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target_demand': [10, 20, 30, 40, 50]
    })
    predictor = TrafficPredictor()
    predictor.train(df)
    # Predict using a known feature vector
    prediction = predictor.predict([3, 3])
    assert isinstance(prediction, float)
    # Model should be trained
    assert predictor.is_trained


def test_traffic_predictor_predict_without_training():
    predictor = TrafficPredictor()
    with pytest.raises(RuntimeError):
        predictor.predict([1, 2])
