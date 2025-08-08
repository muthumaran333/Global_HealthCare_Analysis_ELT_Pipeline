# etl/load_data.py

import logging

logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataLoader:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def load_cases(self, cases_data):
        record_count = len(cases_data)
        logging.info(f"Loading {record_count} records into 'daily_cases' table.")
        try:
            self.db_handler.insert_data("daily_cases", cases_data)
            logging.info("Successfully loaded cases data.")
        except Exception as e:
            logging.error(f"Error loading cases data: {e}")

    def load_vaccinations(self, vacc_data):
        record_count = len(vacc_data)
        logging.info(f"Loading {record_count} records into 'vaccination_data' table.")
        try:
            self.db_handler.insert_data("vaccination_data", vacc_data)
            logging.info("Successfully loaded vaccination data.")
        except Exception as e:
            logging.error(f"Error loading vaccination data: {e}")
