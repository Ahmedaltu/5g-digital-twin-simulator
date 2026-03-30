import unittest
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess

class TestDashboardUserCountWarningResolves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set config to 4 users
        config_path = os.path.join(os.path.dirname(__file__), '..', '5g-digital-twin-simulator', 'config.json')
        config_path = os.path.abspath(config_path)
        with open(config_path, 'r') as f:
            config = json.load(f)
        config['users'] = 4
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        # Run simulation
        main_py = os.path.join(os.path.dirname(__file__), '..', '5g-digital-twin-simulator', 'main.py')
        main_py = os.path.abspath(main_py)
        subprocess.run(['python', main_py, '--config', config_path], check=True)
        # Wait for simulation to finish and results to be written
        time.sleep(2)
        # Start browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.url = 'http://localhost:8501'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_warning_gone_after_simulation(self):
        self.driver.get(self.url)
        time.sleep(4)  # Wait for Streamlit to reload and cache to clear
        body = self.driver.find_element(By.TAG_NAME, 'body').text
        # The warning should NOT appear now
        self.assertNotIn('does not match the current configuration', body)
        self.assertNotIn('Run the simulation to update results', body)
        # The user count metric should match 4
        self.assertIn('Number of Users', body)
        self.assertIn('4', body)

if __name__ == '__main__':
    unittest.main()