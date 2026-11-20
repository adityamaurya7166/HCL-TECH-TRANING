import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CUSTOMER DATA CLEANING PROJECT
# Dataset: customer.csv
# --------------------------------------------------

# Use the folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "customer.csv"
output_file = BASE_DIR / "cleaned_customer.csv"

# Load the messy CSV dataset
df = pd.read_csv(input_file)
original_row_count = len(df)
original_duplicate_count = df["CustomerID"].duplicated().sum()

print("\n========== ORIGINAL DATASET ==========")
print(df.head(10))
print("\nOriginal shape:", df.shape)
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Check that the expected columns are available
required_columns = [
    "CustomerID", "Name", "Age", "Gender",
    "Annual_Income", "Signup_Date", "State"
]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# 1. Remove duplicate customer IDs (keep the first occurrence)
df = df.drop_duplicates(subset=["CustomerID"], keep="first").copy()

# 2. Clean Name column (remove extra spaces and use title case)
df["Name"] = df["Name"].astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.title()

# 3. Clean and standardize Gender
df["Gender"] = df["Gender"].astype("string").str.strip().str.upper()

gender_map = {
    "MALE": "Male",
    "M": "Male",
    "FEMALE": "Female",
    "F": "Female"
}
df["Gender"] = df["Gender"].map(gender_map).fillna("Unknown")

# 4. Clean Annual_Income (remove currency symbols/commas)
df["Annual_Income"] = (
    df["Annual_Income"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Annual_Income"] = pd.to_numeric(
    df["Annual_Income"], errors="coerce"
)

# Treat negative income as invalid/missing
df.loc[df["Annual_Income"] < 0, "Annual_Income"] = np.nan

# Fill missing/invalid income with the median
median_income = df["Annual_Income"].median()
df["Annual_Income"] = df["Annual_Income"].fillna(median_income)

# 5. Clean Age and handle unrealistic values (keep ages 18 to 100)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df.loc[(df["Age"] < 18) | (df["Age"] > 100), "Age"] = np.nan

# Fill missing/invalid age with the median
median_age = df["Age"].median()
df["Age"] = df["Age"].fillna(median_age).round().astype(int)

# 6. Parse mixed Signup_Date formats and standardize dates
# Invalid date text (for example, 'invalid_date') becomes NaT.
df["Signup_Date"] = pd.to_datetime(
    df["Signup_Date"],
    format="mixed",
    errors="coerce"
)

# Export dates in YYYY-MM-DD format
df["Signup_Date"] = df["Signup_Date"].dt.strftime("%Y-%m-%d")

# 7. Clean State column (remove extra spaces and use uppercase)
df["State"] = df["State"].astype("string").str.strip().str.upper()

# Export the cleaned dataset
df.to_csv(output_file, index=False)

print("\n========== CLEANING SUMMARY ==========")
print("Rows before cleaning:", original_row_count)
print("Rows after removing duplicate CustomerIDs:", len(df))
print("Duplicate CustomerIDs removed:",
      original_duplicate_count)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\n========== CLEANED DATASET ==========")
print(df.head(10))
print("\nFinal shape:", df.shape)
print(f"\nCleaned file saved successfully at: {output_file}")
