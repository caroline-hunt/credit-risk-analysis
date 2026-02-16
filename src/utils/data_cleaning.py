"""
Data cleaning utilities for credit card delinquency data
Cleans CSV data by removing duplicates, handling missing values,
standardizing dates and values, and outputting a cleaned dataframe
"""

import pandas as pd
from pathlib import Path


def clean_delinquency_data(input_file: str, output_file: str = None) -> pd.DataFrame:
    """
    Clean delinquency data from CSV file

    Args:
        input_file: Path to input CSV file
        output_file: Optional path to save cleaned CSV (if None, only returns dataframe)

    Returns:
        Cleaned pandas DataFrame
    """
    # Read the CSV file
    df = pd.read_csv(input_file)

    print(f"Original data shape: {df.shape}")
    print(f"Original data:\n{df.head()}\n")

    # 1. Remove duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    print(f"Duplicates removed: {duplicates_removed}")

    # 2. Handle missing values
    missing_before = df.isnull().sum().sum()
    print(f"Missing values before: {missing_before}")

    # Drop rows where date is missing
    df = df.dropna(subset=['date'])

    # Handle missing values in 'value' column
    if 'value' in df.columns:
        df['value'] = df['value'].replace('.', pd.NA)  # Replace '.' with NaN (FRED uses '.' for missing)
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])  # Drop rows with missing values

    missing_after = df.isnull().sum().sum()
    print(f"Missing values after: {missing_after}")

    # 3. Standardize date formats (convert to datetime and back to YYYY-MM-DD)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])  # Remove rows with invalid dates
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    print(f"Date format standardized to YYYY-MM-DD")

    # 4. Standardize values (ensure numeric and round to 2 decimal places)
    if 'value' in df.columns:
        df['value'] = df['value'].round(2)
        print(f"Values standardized (rounded to 2 decimal places)")

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    print(f"\nCleaned data shape: {df.shape}")
    print(f"Cleaned data:\n{df.head()}\n")

    # 5. Output cleaned dataframe
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to: {output_file}")

    return df
