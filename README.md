## Dashboard

Below are screenshots of the Streamlit dashboard used to visualize billing data validation and transformation.

### Data View

![Dashboard](docs/dashboard%201.png)

### Transformed API Data

![Dashboard](docs/dashboard%202.png)
# SaaS Billing Data Migration Pipeline

## Overview

This project simulates migrating billing data from CSV datasets into a SaaS billing platform using REST APIs.

Many companies store billing data in spreadsheets or legacy systems. When migrating to a new billing platform, this data often contains inconsistencies such as missing values, duplicates, or invalid usage records.

This pipeline automates the process of validating, transforming, and uploading billing data.

---

## Features

- CSV data ingestion using pandas
- Data validation for missing values and invalid usage
- Transformation of records into API-ready JSON format
- Automated API upload using Python requests
- Logging of pipeline activity
- Streamlit dashboard for visualizing data

---

## Tech Stack

Python  
Pandas  
Requests  
Streamlit  
YAML  

---

## Project Structure

```
billing_data_migration_pipeline
│
├── data
│   └── customers.csv
│
├── src
│   ├── loader.py
│   ├── validator.py
│   ├── transformer.py
│   ├── api_client.py
│   └── logger.py
│
├── docs
│   ├── dashboard 1.png
│   └── dashboard 2.png
│
├── app.py
├── main.py
├── config.yaml
├── requirements.txt
└── README.md
```

---

## Running the Pipeline

Install dependencies

```
pip install -r requirements.txt
```

Run the pipeline

```
python main.py
```

Run the dashboard

```
streamlit run app.py
```

---

## Dashboard

### Data View

![Dashboard](docs/dashboard%201.png)

### Transformed API Data

![Dashboard](docs/dashboard%202.png)