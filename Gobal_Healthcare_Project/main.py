import configparser
from mysql_handler import MySQLHandler
from etl.api_client import APIClient
from cli_manager import CLIManager
from utils.logger import get_logger

logger = get_logger("Main")

def main():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        logger.info("Loaded configuration from config.ini.")

        db_config = {
            "host": config["mysql"]["host"],
            "user": config["mysql"]["user"],
            "password": config["mysql"]["password"],
            "database": config["mysql"]["database"]
        }
        logger.info("Database configuration parsed successfully.")

        # Initialize core components
        db_handler = MySQLHandler(db_config)
        api_client = APIClient("http://localhost:3000/api")
        logger.info("ETL components initialized.")

        # Run CLIManager
        cli = CLIManager(api_client, db_handler)
        logger.info("Starting CLI manager.")
        cli.run()

    except Exception as e:
        logger.exception("Unhandled exception in main execution.")

if __name__ == "__main__":
    main()
