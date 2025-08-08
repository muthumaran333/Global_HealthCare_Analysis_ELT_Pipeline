import configparser
from mysql_handler import MySQLHandler

def test_connection():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "mysql" not in config:
        print("Missing [mysql] section in config.ini")
        return

    try:
        db_handler = MySQLHandler({
            "host": config["mysql"]["host"],
            "user": config["mysql"]["user"],
            "password": config["mysql"]["password"],
            "database": config["mysql"]["database"]
        })
        print("Connected to the database successfully.")
    except Exception as e:
        print("Failed to connect to the database:", str(e))
    finally:
        db_handler.close()

if __name__ == "__main__":
    test_connection()
