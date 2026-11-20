# CUSTOMER DATA ANALYSIS PROJECT
# Dataset: cleaned_customer.csv
# Libraries: pandas, matplotlib (optional for charts)

import pandas as pd
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False

# Keep this Python file and cleaned_customer.csv in the SAME folder.
FILE_PATH = Path(__file__).with_name("cleaned_customer.csv")

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print("ERROR: cleaned_customer.csv nahi mili.")
    print("CSV file ko is Python file ke same folder mein rakho.")
    raise SystemExit

# Prepare date column for monthly analysis
df["Signup_Date"] = pd.to_datetime(df["Signup_Date"], errors="coerce")

def line():
    print("-" * 58)

def show_overview():
    line()
    print("CUSTOMER DATASET OVERVIEW")
    line()
    print(f"Total records       : {len(df)}")
    print(f"Total columns       : {len(df.columns)}")
    print(f"Unique customers    : {df['CustomerID'].nunique()}")
    print(f"Average age         : {df['Age'].mean():.2f}")
    print(f"Average annual income: {df['Annual_Income'].mean():,.2f}")
    print("\nColumn names:", ", ".join(df.columns))
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())

def show_data():
    print("\n1. First 10 records\n")
    print(df.head(10).to_string(index=False))
    print("\n2. Last 10 records\n")
    print(df.tail(10).to_string(index=False))

def numerical_summary():
    print("\nNUMERICAL DATA SUMMARY")
    print(df[["Age", "Annual_Income"]].describe().round(2))

def gender_analysis():
    print("\nGENDER-WISE CUSTOMER COUNT")
    print(df["Gender"].value_counts(dropna=False).to_string())
    print("\nGENDER-WISE AVERAGE INCOME")
    print(df.groupby("Gender")["Annual_Income"].mean().round(2).to_string())
    if CHARTS_AVAILABLE:
        df["Gender"].value_counts().plot(kind="bar", title="Customers by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Number of customers")
        plt.tight_layout()
        plt.show()

def age_analysis():
    bins = [0, 18, 30, 45, 60, 100]
    labels = ["Below 18", "18-30", "31-45", "46-60", "Above 60"]
    age_groups = pd.cut(df["Age"], bins=bins, labels=labels, include_lowest=True)
    print("\nAGE GROUP-WISE CUSTOMER COUNT")
    print(age_groups.value_counts(sort=False).to_string())
    print("\nAverage age:", round(df["Age"].mean(), 2))
    if CHARTS_AVAILABLE:
        age_groups.value_counts(sort=False).plot(kind="bar", title="Customers by Age Group")
        plt.xlabel("Age group")
        plt.ylabel("Number of customers")
        plt.tight_layout()
        plt.show()

def income_analysis():
    print("\nANNUAL INCOME ANALYSIS")
    print("Minimum income:", f"{df['Annual_Income'].min():,.2f}")
    print("Maximum income:", f"{df['Annual_Income'].max():,.2f}")
    print("Average income:", f"{df['Annual_Income'].mean():,.2f}")
    print("Median income :", f"{df['Annual_Income'].median():,.2f}")
    bins = [0, 30000, 60000, 90000, 120000, float("inf")]
    labels = ["0-30k", "30k-60k", "60k-90k", "90k-120k", "120k+"]
    groups = pd.cut(df["Annual_Income"], bins=bins, labels=labels, include_lowest=True)
    print("\nCUSTOMERS BY INCOME RANGE")
    print(groups.value_counts(sort=False).to_string())

def state_analysis():
    print("\nSTATE-WISE CUSTOMER COUNT")
    counts = df["State"].value_counts()
    print(counts.to_string())
    if CHARTS_AVAILABLE:
        counts.plot(kind="bar", title="Customers by State")
        plt.xlabel("State")
        plt.ylabel("Number of customers")
        plt.tight_layout()
        plt.show()

def state_income_analysis():
    result = df.groupby("State").agg(
        Customer_Count=("CustomerID", "nunique"),
        Average_Income=("Annual_Income", "mean"),
        Total_Income=("Annual_Income", "sum")
    ).sort_values("Average_Income", ascending=False)
    print("\nSTATE-WISE INCOME ANALYSIS")
    print(result.round(2).to_string())

def signup_analysis():
    dates = df.dropna(subset=["Signup_Date"]).copy()
    if dates.empty:
        print("Signup_Date mein valid dates nahi hain.")
        return
    monthly = dates.groupby(dates["Signup_Date"].dt.to_period("M")).size()
    print("\nMONTH-WISE NEW SIGNUPS")
    print(monthly.to_string())
    if CHARTS_AVAILABLE:
        monthly.index = monthly.index.astype(str)
        monthly.plot(kind="line", marker="o", title="Monthly Customer Signups")
        plt.xlabel("Month")
        plt.ylabel("New signups")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def search_customer():
    value = input("Customer ka naam ya CustomerID enter karo: ").strip()
    if not value:
        print("Search value empty hai.")
        return
    result = df[
        df["Name"].astype(str).str.contains(value, case=False, na=False)
        | df["CustomerID"].astype(str).str.contains(value, na=False)
    ]
    if result.empty:
        print("Customer nahi mila.")
    else:
        print(result.to_string(index=False))

def top_customers():
    print("\nTOP 10 CUSTOMERS BY ANNUAL INCOME")
    result = df.nlargest(10, "Annual_Income")
    print(result[["CustomerID", "Name", "Age", "Gender", "Annual_Income", "State"]].to_string(index=False))

def age_income_relationship():
    correlation = df["Age"].corr(df["Annual_Income"])
    print("\nAGE AND ANNUAL INCOME RELATIONSHIP")
    print(f"Correlation: {correlation:.3f}")
    if pd.isna(correlation):
        print("Correlation calculate nahi ho paya.")
    elif correlation > 0:
        print("Is dataset mein age aur income ke beech positive correlation hai.")
    elif correlation < 0:
        print("Is dataset mein age aur income ke beech negative correlation hai.")
    else:
        print("Is dataset mein linear correlation lagbhag zero hai.")
    if CHARTS_AVAILABLE:
        df.plot(kind="scatter", x="Age", y="Annual_Income",
                title="Age vs Annual Income")
        plt.tight_layout()
        plt.show()

def export_report():
    output = Path(__file__).with_name("customer_analysis_report.csv")
    report = df.groupby("State").agg(
        Customer_Count=("CustomerID", "nunique"),
        Average_Age=("Age", "mean"),
        Average_Income=("Annual_Income", "mean"),
        Total_Income=("Annual_Income", "sum")
    ).round(2).reset_index()
    report.to_csv(output, index=False)
    print(f"\nReport save ho gayi: {output}")

MENU = {
    "1": ("Dataset overview", show_overview),
    "2": ("First and last 10 records", show_data),
    "3": ("Numerical summary (Age and Income)", numerical_summary),
    "4": ("Gender-wise analysis", gender_analysis),
    "5": ("Age group analysis", age_analysis),
    "6": ("Annual income analysis", income_analysis),
    "7": ("State-wise customer count", state_analysis),
    "8": ("State-wise income analysis", state_income_analysis),
    "9": ("Monthly signup analysis", signup_analysis),
    "10": ("Search customer by name or ID", search_customer),
    "11": ("Top 10 customers by income", top_customers),
    "12": ("Age and income relationship", age_income_relationship),
    "13": ("Export state-wise report to CSV", export_report),
}

def main():
    print("=" * 58)
    print("       CUSTOMER DATA ANALYSIS PROJECT")
    print("=" * 58)
    while True:
        print("\nChoose an analysis option:")
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("\nApni choice enter karo (0-13): ").strip()

        if choice == "0":
            print("Project close ho gaya. Thank you!")
            break
        if choice in MENU:
            line()
            MENU[choice][1]()
            line()
        else:
            print("Invalid choice! Please 0 se 13 ke beech option select karo.")

if __name__ == "__main__":
    main()
