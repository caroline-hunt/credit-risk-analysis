---
name: clean-data
description: This skill should be used when the user asks to "clean data", "clean the data", "remove duplicates", "handle missing values", "standardize data", "clean delinquency data", or mentions data cleaning tasks for credit risk analysis.
version: 1.0.0
---

# Clean Data Skill

This skill provides guidance and tools for cleaning credit card delinquency data.

## Overview

This skill helps clean CSV data by:
- Removing duplicate rows
- Handling missing values
- Standardizing date formats (to YYYY-MM-DD)
- Standardizing numeric values (rounding to 2 decimal places)
- Outputting a cleaned dataframe

## When This Skill Applies

Use this skill when:
- The user requests data cleaning operations
- Working with credit card delinquency data that needs preprocessing
- Preparing data for analysis or modeling
- Dealing with data quality issues

## Implementation

Data cleaning utilities are available in the `src/utils` module:

```python
from src.utils.data_cleaning import clean_delinquency_data

# Clean data and save to new file
cleaned_df = clean_delinquency_data(
    input_file="output/delinquency_data.csv",
    output_file="output/delinquency_data_cleaned.csv"
)
```

A CLI script is also available at `scripts/clean_data.py` for quick cleaning.

## Data Cleaning Steps

### 1. Remove Duplicate Rows
- Uses pandas `drop_duplicates()` to eliminate exact duplicate rows
- Reports number of duplicates found and removed

### 2. Handle Missing Values
- Drops rows with missing dates
- Converts FRED's '.' placeholder to NaN
- Drops rows with missing numeric values
- Alternative strategies available: forward fill, interpolation

### 3. Standardize Date Formats
- Converts all dates to pandas datetime objects
- Standardizes output format to YYYY-MM-DD
- Removes rows with invalid dates

### 4. Standardize Values
- Ensures all values are numeric
- Rounds values to 2 decimal places for consistency
- Handles conversion errors gracefully

### 5. Sort and Output
- Sorts data by date in ascending order
- Resets index for clean sequential indexing
- Saves to CSV without index column
- Returns pandas DataFrame for further analysis

## Usage Examples

**Basic cleaning:**
```bash
python scripts/clean_data.py
```

**Custom file paths:**
```python
cleaned_df = clean_delinquency_data(
    input_file="path/to/raw_data.csv",
    output_file="path/to/cleaned_data.csv"
)
```

**Get dataframe without saving:**
```python
cleaned_df = clean_delinquency_data(
    input_file="output/delinquency_data.csv",
    output_file=None
)
```

## Output

The cleaning process provides:
- Console output showing cleaning statistics
- Cleaned CSV file saved to specified location
- Pandas DataFrame with cleaned data
- Summary statistics of the cleaned data

## Best Practices

- Always inspect the cleaning report to understand what was removed/modified
- Review the summary statistics to catch any anomalies
- Keep the original raw data file unchanged
- Use descriptive output filenames (e.g., `*_cleaned.csv`)
