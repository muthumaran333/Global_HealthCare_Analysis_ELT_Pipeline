# 🌍 Global Healthcare Data ETL & Analysis CLI

A command-line Python application that extracts COVID-19 case and vaccination data from a public API, transforms it into a structured format, loads it into a MySQL database, and allows users to perform analytical queries directly from the terminal.

---

## 📦 Features

* 🔌 Extract COVID-19 case and vaccination data from a RESTful API
* 🧹 Transform and clean data using `pandas`
* 🗃️ Load structured data into a MySQL database
* 🧾 Run predefined analytical queries from the CLI
* 💻 Execute raw SQL queries
* 📂 Manage database tables (list/drop)
* 📋 View query results in formatted tables
* 🪵 Centralized logging for ETL and CLI operations

---

## 🗂️ Project Structure

```bash
.
├── cli_manager.py               # CLI command parsing and handling
├── config.ini                   # MySQL DB configuration
├── create_table.py              # Script to execute SQL file
├── etl/
│   ├── __init__.py
│   ├── api_client.py            # Fetches data from public API
│   ├── data_transformer.py      # Cleans and transforms raw data
│   ├── load_data.py             # Loads data into MySQL
│   └── __pycache__/             # Compiled bytecode cache
├── logs/
│   └── etl_log_YYYY-MM-DD.log   # Log file with timestamp
├── main.py                      # Entry-point CLI runner
├── mysql_handler.py             # Database connection & query logic
├── requirements.txt             # Project dependencies
├── sql/
│   └── create_tables.sql        # SQL table schema
├── test_connection.py           # MySQL connection test script
├── utils/
│   ├── logger.py                # Logging setup and configuration
│   └── __pycache__/
│       └── logger.*.pyc
└── README.md                    # You are here
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Prerequisites

* Python 3.8+
* MySQL server running locally or remotely
* Pip installed (`python -m ensurepip --upgrade`)

### 2. 🧪 Clone the Repository

```bash
git clone https://github.com/yourusername/global-healthcare-etl-cli.git
cd global-healthcare-etl-cli
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔐 Configure Database

Edit the `config.ini` file:

```ini
[mysql]
host = localhost
user = root
password = yourpassword
database = healthcare_db
port = 3306
```

### 5. 🏗️ Create Database Tables

```bash
python create_table.py
```

---

## 🚀 Using the CLI

```bash
python main.py <command> [arguments]
```

### ✅ Example Commands

#### 📥 Fetch and Load Data

```bash
python main.py fetch_data "India" 2020-01-01 2023-12-31
```

#### 📊 Query Data

* **Total Cases**:

  ```bash
  python main.py query_data total_cases India
  ```

* **Daily Trends**:

  ```bash
  python main.py query_data daily_trends India new_cases
  ```

* **Top N Countries**:

  ```bash
  python main.py query_data top_n_countries_by_metric 5 total_cases
  ```

#### 📂 List All Tables

```bash
python main.py list_tables
```

#### ❌ Drop All Tables

```bash
python main.py drop_tables
```

#### 💻 Run Custom SQL

```bash
python main.py run_sql "SELECT * FROM daily_cases LIMIT 10;"
```

---

## 🪵 Logging

Logs are automatically written to the `logs/` directory and rotate daily. Each run logs API status, transformation notes, DB inserts, and CLI usage.

Example:

```bash
logs/etl_log_2025-08-01.log
```

---

## 📚 Dependencies

```
mysql-connector-python
requests
pandas
tabulate
```

Install via:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Author

**Muthumaran T**
*ETL & Data Engineering Enthusiast*

---
