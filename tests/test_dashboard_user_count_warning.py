import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class TestDashboardUserCountWarning(unittest.TestCase):
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

    def test_user_count_warning(self):
        self.driver.get(self.url)
        time.sleep(3)  # Wait for Streamlit to load
        body = self.driver.find_element(By.TAG_NAME, 'body').text
        # The warning should appear if the config and results user counts differ
        self.assertIn('does not match the current configuration', body)
        self.assertIn('Run the simulation to update results', body)

if __name__ == '__main__':
    unittest.main()