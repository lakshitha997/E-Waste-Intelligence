# E-Waste Generation and Recycling Intelligence

## Project Overview
This project analyzes global electronic waste (e-waste) generation and documented recycling data using an ETL (Extract, Transform, Load) pipeline.

It processes country-level data from the Global E-waste Monitor 2024 and generates cleaned datasets, a SQLite database, data quality reports, and visualizations.

## Objectives
- Analyze e-waste generation across countries and regions.
- Calculate documented e-waste recycling rates.
- Identify gaps in documented collection and recycling data.
- Perform data cleaning and validation.
- Store processed data in CSV and SQLite formats.
- Generate charts for data analysis.

## Dataset
- **Source:** Global E-waste Monitor 2024 (UNITAR/ITU)
- **Data year:** 2022
- **Records:** 189
- **Original columns:** 8

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- SQLite
- Jupyter Notebook

## ETL Pipeline

### 1. Extract
Reads the original country-level e-waste dataset from a CSV file.

### 2. Transform
- Standardizes column names.
- Converts numerical columns to appropriate data types.
- Removes duplicate country records.
- Handles missing values without incorrectly replacing them with zero.
- Calculates recycling rates.
- Calculates e-waste not documented as collected and recycled.
- Assigns data validation statuses.

### 3. Load
Saves the processed data into:
- Cleaned CSV file
- SQLite database
- Data quality report

## Data Quality
The pipeline checks missing values, duplicate records, and invalid numerical values.

Validation statuses:
- **Passed:** Available data passes the implemented checks.
- **Incomplete:** Documented recycling information is missing.
- **Review:** A numerical validation rule is triggered.

## Key Calculations

**Recycling Rate (%)**

Documented collected e-waste / Generated e-waste × 100

**E-waste not documented as collected and recycled**

Generated e-waste − Documented collected e-waste

This second metric is not proof of landfill disposal. It represents the amount not documented as formally collected and recycled.

## Project Structure

```text
E-Waste-Intelligence/
│
├── data/
│   ├── raw/
│   │   └── ewaste_raw.csv
│   └── processed/
│       ├── ewaste_cleaned.csv
│       └── ewaste_intelligence.db
│
├── src/
│   └── etl_pipeline.py
│
├── notebooks/
│
├── reports/
│   ├── etl_quality_report.csv
│   ├── ewaste_generation.png
│   └── recycling_rate.png
│
├── requirements.txt
└── README.md
```

## How to Run

1. Clone this repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the ETL pipeline:

```bash
python src/etl_pipeline.py
```

## Limitations
- The dataset represents 2022 statistics.
- Documented recycling information is missing for many countries.
- Some country names in the source dataset are incomplete.
- Missing documented collection data is not assumed to mean zero recycling.

## Future Enhancements
- Build an interactive dashboard using Streamlit.
- Add time-series analysis with data from multiple years.
- Integrate additional economic and environmental indicators.
- Improve country-name validation and standardization.

## Data Source
Global E-waste Monitor 2024 — UNITAR and ITU.