#!/usr/bin/env python3
"""
CLI script for cleaning credit card delinquency data
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from utils.data_cleaning import clean_delinquency_data


def main():
    """Main entry point for CLI"""
    input_file = "output/delinquency_data.csv"
    output_file = "output/delinquency_data_cleaned.csv"

    cleaned_df = clean_delinquency_data(input_file, output_file)

    print("\nData cleaning complete!")
    print(f"Final shape: {cleaned_df.shape}")
    print(f"\nSummary statistics:")
    print(cleaned_df.describe())


if __name__ == "__main__":
    main()
