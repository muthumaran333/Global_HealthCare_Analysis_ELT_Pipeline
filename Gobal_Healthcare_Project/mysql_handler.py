import mysql.connector
from utils.logger import get_logger 

logger = get_logger("MySQLHandler") 
class MySQLHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            logger.info(" Database connection established.")
        except mysql.connector.Error as err:
            logger.error(" Failed to connect to database.", exc_info=True)
            raise

    def run_query(self, sql):
        try:
            logger.info(f"Executing SQL query: {sql}")
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            logger.info(f" Query executed. Rows returned: {len(results)}")
            return results
        except mysql.connector.Error as err:
            logger.error(" Error running query", exc_info=True)
            raise

    def run_query_with_columns(self, sql):
        try:
            logger.info(f"Executing SQL query with columns: {sql}")
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            logger.info(f"Query executed. Columns: {columns}, Rows: {len(results)}")
            return results, columns
        except mysql.connector.Error as err:
            logger.error("Error running query with columns", exc_info=True)
            raise

    def insert_data(self, table_name, records):
        if not records:
            print("No records to insert.")
            logger.warning(f"No records to insert into `{table_name}`.")
            return

        columns = (
            ["report_date", "country_name", "total_cases", "new_cases", "total_deaths", "new_deaths", "etl_timestamp"]
            if table_name == "daily_cases"
            else ["report_date", "country_name", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "etl_timestamp"]
        )

        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"""
            INSERT IGNORE INTO {table_name} ({", ".join(columns)})
            VALUES ({placeholders})
        """

        try:
            logger.info(f"Inserting {len(records)} records into `{table_name}`...")
            self.cursor.executemany(insert_query, records)
            self.conn.commit()
            print(f"Inserted {self.cursor.rowcount} rows into `{table_name}`.")
            logger.info(f"Inserted {self.cursor.rowcount} rows into `{table_name}`.")
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            logger.error("Error inserting data into database.", exc_info=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.info("🔒 Database connection closed.")
