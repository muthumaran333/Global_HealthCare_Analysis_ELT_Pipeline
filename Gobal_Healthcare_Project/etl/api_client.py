import logging
import requests

logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        logging.info(f"APIClient initialized with base URL: {self.base_url}")

    def fetch_cases(self):
        url = f"{self.base_url}/cases"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info("Successfully fetched cases data.")
                return response.json()
            else:
                logging.warning(f"Failed to fetch cases. Status code: {response.status_code}")
                return []
        except Exception as e:
            logging.error(f"Error fetching cases: {e}")
            return []

    def fetch_vaccinations(self):
        url = f"{self.base_url}/vaccinations"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info("Successfully fetched vaccination data.")
                return response.json()
            else:
                logging.warning(f"Failed to fetch vaccinations. Status code: {response.status_code}")
                return []
        except Exception as e:
            logging.error(f"Error fetching vaccinations: {e}")
            return []
