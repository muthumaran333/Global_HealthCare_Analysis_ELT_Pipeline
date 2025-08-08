import mysql.connector
import configparser
import os
import logging

# Configure logging
logging.basicConfig(
    filename='sql_execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def execute_sql_file(file_path):
    # Load database config from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    db_config = {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
        "database": config["mysql"]["database"],
        "port": int(config["mysql"].get("port", 3306))
    }

    logging.info(f"Starting execution of SQL file: {file_path}")

    # Read SQL file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        logging.info("SQL file read successfully.")
    except FileNotFoundError:
        logging.error(f"SQL file not found: {file_path}")
        return

    # Execute SQL statements
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
                logging.info(f"Executed statement: {statement.strip()[:100]}...")
        conn.commit()
        logging.info("All statements executed and committed successfully.")
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        print(f"MySQL Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(base_dir, "sql", "create_tables.sql")
    execute_sql_file(sql_file_path)
