import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class TestDashboardWithResults(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.url = 'http://localhost:8501'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_results_displayed(self):
        self.driver.get(self.url)
        time.sleep(3)  # Wait for Streamlit to load
        body = self.driver.find_element(By.TAG_NAME, 'body').text
        # Check for key metrics and charts
        self.assertIn('Simulation results loaded successfully', body)
        self.assertIn('Number of Users', body)
        self.assertIn('Throughput (Mbps)', body)
        self.assertIn('Cell Utilization', body)
        self.assertIn('Avg User Throughput', body)
        self.assertIn("Jain's Fairness", body)
        self.assertIn('Congestion Ratio', body)
        self.assertIn('Traffic Demand (Mbps)', body)
        self.assertIn('Throughput Over Time', body)
        self.assertIn('Avg User Throughput Over Time', body)
        self.assertIn("Jain's Fairness Index Over Time", body)
        self.assertIn('Congestion Ratio Over Time', body)
        self.assertIn('Traffic Demand Over Time', body)
        self.assertIn('Cell Utilization Over Time', body)

if __name__ == '__main__':
    unittest.main()
