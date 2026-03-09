"""
TrafficPredictor module for 5G RAN Digital Twin Simulator.
Predicts future network traffic demand using machine learning.
"""

from typing import Any
import pandas as pd
from sklearn.linear_model import LinearRegression

class TrafficPredictor:
	"""
	Predicts future network demand using a simple linear regression model.
	"""
	def __init__(self) -> None:
		"""
		Initialize the TrafficPredictor with a LinearRegression model.
		"""
		self.model = LinearRegression()
		self.is_trained = False

	def train(self, dataframe: pd.DataFrame) -> None:
		"""
		Train the model on historical simulation data.

		Args:
			dataframe: Pandas DataFrame with features and target demand column.
		"""
		X = dataframe.drop(columns=["target_demand"])
		y = dataframe["target_demand"]
		self.model.fit(X, y)
		self.is_trained = True

	def predict(self, features: Any) -> float:
		"""
		Predict future network demand given input features.

		Args:
			features: Feature vector or DataFrame for prediction.
		Returns:
			Predicted demand as a float.
		"""
		if not self.is_trained:
			raise RuntimeError("Model must be trained before prediction.")
		prediction = self.model.predict([features])
		return float(prediction[0])
