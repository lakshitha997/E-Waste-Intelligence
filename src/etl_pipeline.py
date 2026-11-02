import pandas as pd
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt

# PROJECT PATHS
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "ewaste_raw.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# 1. EXTRACT
print("STEP 1: EXTRACTING DATA")

df = pd.read_csv(RAW_FILE)

print("Original dataset shape:", df.shape)
print("Data extracted successfully!")


# 2. INSPECT
print("\nSTEP 2: INSPECTING DATA")

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# 3. TRANSFORM
print("\nSTEP 3: TRANSFORMING DATA")

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Remove unwanted spaces from country names
df["country"] = df["country"].astype("string").str.strip()

# Convert numerical columns
numeric_columns = [
    "ewaste_generated_million_kg_2022",
    "ewaste_generated_kg_per_capita_2022",
    "ewaste_documented_collected_million_kg_2022",
    "gdp_per_capita_usd",
    "gdp_per_capita_year"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows without essential information
df = df.dropna(
    subset=["country", "ewaste_generated_million_kg_2022"]
)

# Remove duplicate country records
df = df.drop_duplicates(subset=["country"])

# Calculate recycling rate
df["recycling_rate_percent"] = (
    df["ewaste_documented_collected_million_kg_2022"]
    / df["ewaste_generated_million_kg_2022"]
) * 100

# Calculate unrecycled or undocumented waste
df["unrecycled_or_not_documented_million_kg"] = (
    df["ewaste_generated_million_kg_2022"]
    - df["ewaste_documented_collected_million_kg_2022"]
)


# Flag data quality status

df["validation_status"] = "Passed"

# Missing recycling information
missing_recycling = df[
    "ewaste_documented_collected_million_kg_2022"
].isna()

df.loc[missing_recycling, "validation_status"] = "Incomplete"

# Invalid numerical values
invalid = (
    (df["ewaste_generated_million_kg_2022"] < 0)
    | (df["ewaste_documented_collected_million_kg_2022"] < 0)
    | (
        df["ewaste_documented_collected_million_kg_2022"]
        > df["ewaste_generated_million_kg_2022"]
    )
)

df.loc[invalid, "validation_status"] = "Review"


print("Data transformation completed!")


# 4. LOAD - CSV
print("\nSTEP 4: LOADING CLEANED DATA")

csv_output = OUTPUT_DIR / "ewaste_cleaned.csv"

df.to_csv(csv_output, index=False)

print("Cleaned CSV saved successfully!")


# 5. LOAD - SQLITE DATABASE

database = OUTPUT_DIR / "ewaste_intelligence.db"

with sqlite3.connect(database) as connection:
    df.to_sql(
        "ewaste_statistics",
        connection,
        if_exists="replace",
        index=False
    )

print("SQLite database created successfully!")


# 6. QUALITY REPORT

# Generate data quality report
quality_report = pd.DataFrame({
    "Metric": [
        "Total records",
        "Total columns",
        "Missing values",
        "Passed records",
        "Incomplete records",
        "Records requiring review"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df.isnull().sum().sum()),
        int((df["validation_status"] == "Passed").sum()),
        int((df["validation_status"] == "Incomplete").sum()),
        int((df["validation_status"] == "Review").sum())
    ]
})

quality_report.to_csv(
    REPORT_DIR / "etl_quality_report.csv",
    index=False
)

print("Quality report generated!")


# 7. VISUALIZATION

top_countries = df.nlargest(
    10, "ewaste_generated_million_kg_2022"
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_countries["country"],
    top_countries["ewaste_generated_million_kg_2022"]
)

plt.xticks(rotation=45, ha="right")
plt.xlabel("Country")
plt.ylabel("E-waste Generated (Million kg)")
plt.title("Top 10 E-Waste Generating Countries")

plt.tight_layout()

plt.savefig(REPORT_DIR / "ewaste_generation.png")
plt.close()


# Recycling rate chart (only known values)
recycling_data = df.dropna(
    subset=["recycling_rate_percent"]
)

top_recycling = recycling_data.nlargest(
    10, "recycling_rate_percent"
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_recycling["country"],
    top_recycling["recycling_rate_percent"]
)

plt.xticks(rotation=45, ha="right")
plt.xlabel("Country")
plt.ylabel("Documented Recycling Rate (%)")
plt.title("Top 10 Countries by Documented Recycling Rate")

plt.tight_layout()

plt.savefig(REPORT_DIR / "recycling_rate.png")
plt.close()


print("\n================================")
print("ETL PIPELINE COMPLETED!")
print("================================")
print("Processed records:", len(df))
print("Cleaned CSV:", csv_output)
print("Database:", database)
print("Quality report:", REPORT_DIR)
print("Charts generated successfully!")
