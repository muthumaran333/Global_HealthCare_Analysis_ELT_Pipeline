# 🌍 Global Healthcare Data ETL & Analysis — CLI & Dashboard

This project is a **full-stack data engineering solution** designed to collect, process, and analyze global COVID-19 case and vaccination data.

It includes:

* **Command-Line Interface (CLI)** for ETL operations and analytical queries
* **Interactive Streamlit Dashboard** for rich, visual data exploration

The solution uses a **Python + Pandas ETL pipeline** to extract data from a public REST API, clean and transform it, store it in a **MySQL database**, and make it accessible for both terminal-based analysis and interactive dashboards.

---

## 📦 Features

### **CLI**

* 🔌 **Data Extraction** – Fetch global COVID-19 case and vaccination data from REST API
* 🧹 **Data Cleaning** – Transform and prepare data using `pandas`
* 🗃 **Data Loading** – Store structured datasets in MySQL
* 🧾 **Predefined Queries** – Retrieve total cases, deaths, and vaccination stats per country
* 💻 **Custom SQL Execution** – Run raw SQL queries directly from the CLI
* 📂 **Database Management** – List and inspect available tables
* 📋 **Formatted Output** – View results in clean, tabular formats
* 🪵 **Logging** – Maintain detailed logs of ETL and CLI operations

### **Dashboard**

* 🌐 Compare COVID-19 data across multiple countries
* 📊 Time-series visualizations (Line, Bar, Area charts)
* 🗺 Interactive global choropleth maps
* 📋 Summary statistics at a glance
* 📥 Export visualized data as CSV
* 🔍 Inspect raw datasets within the app

---

## 🖥 Screenshots

### **CLI in Action**

| Command Example                    | Output                        |
| ---------------------------------- | ----------------------------- |
| ![CLI Fetch](Gobal_Healthcare_Project\images/Cli1.png)      | ![CLI Query](Gobal_Healthcare_Project\images/Cli2.png) |
| ![CLI Custom SQL](Gobal_Healthcare_Project\images/cli3.png) |     ![CLI Custom SQL](Gobal_Healthcare_Project\images/Cli4.png)                          |

---

### **Dashboard Views**

#### **1️⃣ Line Chart – Cases Over Time**

![Dashboard1](Gobal_Healthcare_Project\images/Dashboard1.png)

#### **2️⃣ Bar Chart – Vaccinations**

![Dashboard2](Gobal_Healthcare_Project\images/Dashboard2.png)

#### **3️⃣ Area Chart – Death Trends**

![Dashboard3](Gobal_Healthcare_Project\images/Dashboard3.png)

#### **4️⃣ Global Cumulative Map**

![Dashboard4](Gobal_Healthcare_Project\images/Dashboard4.png)

#### **5️⃣ Summary Statistics**

![Dashboard5](Gobal_Healthcare_Project\images/Dashboard5.png)

#### **6️⃣ Raw Data Viewer**

![Dashboard6](Gobal_Healthcare_Project\images/Dashboard6.png)

---

## 🗂 Project Structure

```bash
.
├── cli_manager.py               # CLI command parsing & handling
├── config.ini                    # MySQL database configuration
├── create_table.py               # Create database tables from schema
├── etl/
│   ├── api_client.py             # Fetch data from API
│   ├── data_transformer.py       # Clean & transform datasets
│   ├── load_data.py              # Load processed data into MySQL
├── logs/
│   └── etl_log_YYYY-MM-DD.log    # ETL log files
├── main.py                       # CLI entry point
├── mysql_handler.py              # MySQL query execution
├── sql/
│   └── create_tables.sql         # Database table schema
├── dashboard.py                  # Streamlit dashboard
├── requirements.txt              # Python dependencies
├── images/                       # Project screenshots
└── README.md
```

---

## ⚙️ Setup Instructions

### **1. Prerequisites**

* Python 3.8+
* MySQL Server
* Pip

### **2. Clone the Repository**

```bash
git clone https://github.com/muthumaran333/Global_HealthCare_Analysis_ELT_Pipeline.git
cd Global_HealthCare_Analysis_ELT_Pipeline
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure Database**

Edit `config.ini` with your database credentials:

```ini
[mysql]
host = localhost
user = root
password = yourpassword
database = healthcare_db
port = 3306
```

### **5. Create Database Tables**

```bash
python create_table.py
```

---

## 🚀 Running the Project

### **CLI Usage**

```bash
# Fetch data for India from Jan 2020 to Dec 2023
python main.py fetch_data "India" 2020-01-01 2023-12-31

# Query total cases for India
python main.py query_data total_cases India

# List all available database tables
python main.py list_tables

# Run a custom SQL query
python main.py run_sql "SELECT * FROM daily_cases LIMIT 10;"
```

### **Dashboard Usage**

```bash
streamlit run dashboard.py
```

Then open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 📚 Dependencies

```
mysql-connector-python
requests
pandas
tabulate
streamlit
plotly
altair
```

