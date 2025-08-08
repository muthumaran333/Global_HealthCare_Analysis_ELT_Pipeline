# etl/data_transformer.py

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataTransformer:

    def transform_cases(self, raw_data):
        logging.info("Starting transformation of cases data.")
        df = pd.DataFrame(raw_data)

        df = df.rename(columns={
            "report_date": "report_date",
            "country_name": "country_name",
            "total_cases": "total_cases",
            "new_cases": "new_cases",
            "total_deaths": "total_deaths",
            "new_deaths": "new_deaths",
            "etl_timestamp": "etl_timestamp"
        })

        initial_count = len(df)
        df = df.dropna(subset=["report_date", "country_name", "total_cases"])
        filtered_count = len(df)

        logging.info(f"Cases: Dropped {initial_count - filtered_count} records due to missing values.")

        try:
            df["report_date"] = pd.to_datetime(df["report_date"]).dt.date
            df["etl_timestamp"] = pd.to_datetime(df["etl_timestamp"])
        except Exception as e:
            logging.error(f"Cases: Error in date conversion: {e}")
            return []

        records = list(df[[
            "report_date", "country_name", "total_cases",
            "new_cases", "total_deaths", "new_deaths", "etl_timestamp"
        ]].itertuples(index=False, name=None))

        logging.info(f"Cases: Successfully transformed {len(records)} records.")
        return records

    def transform_vaccinations(self, raw_data):
        logging.info("Starting transformation of vaccination data.")
        df = pd.DataFrame(raw_data)

        df = df.rename(columns={
            "report_date": "report_date",
            "country_name": "country_name",
            "total_vaccinations": "total_vaccinations",
            "people_vaccinated": "people_vaccinated",
            "people_fully_vaccinated": "people_fully_vaccinated",
            "etl_timestamp": "etl_timestamp"
        })

        initial_count = len(df)
        df = df.dropna(subset=["report_date", "country_name", "total_vaccinations"])
        filtered_count = len(df)

        logging.info(f"Vaccinations: Dropped {initial_count - filtered_count} records due to missing values.")

        try:
            df["report_date"] = pd.to_datetime(df["report_date"]).dt.date
            df["etl_timestamp"] = pd.to_datetime(df["etl_timestamp"])
        except Exception as e:
            logging.error(f"Vaccinations: Error in date conversion: {e}")
            return []

        records = list(df[[
            "report_date", "country_name", "total_vaccinations",
            "people_vaccinated", "people_fully_vaccinated", "etl_timestamp"
        ]].itertuples(index=False, name=None))

        logging.info(f"Vaccinations: Successfully transformed {len(records)} records.")
        return records
