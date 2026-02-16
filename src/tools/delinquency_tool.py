"""
Credit Card Delinquency Data Tool
Handles fetching and processing FRED delinquency data
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_SERIES_ID = "DRCCLACBS"
FRED_API_URL = "https://api.stlouisfed.org/fred/series/observations"

# Get the project root directory (two levels up from this file)
SCRIPT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = SCRIPT_DIR / "output"


def calculate_start_date(years: int) -> str:
    """Calculate start date based on years back from today"""
    start_date = datetime.now() - timedelta(days=years * 365)
    return start_date.strftime("%Y-%m-%d")


def fetch_fred_data(years: int) -> dict:
    """Fetch data from FRED API"""
    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY not found in environment variables")

    start_date = calculate_start_date(years)

    params = {
        "series_id": FRED_SERIES_ID,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date
    }

    response = httpx.get(FRED_API_URL, params=params, timeout=30.0)
    response.raise_for_status()

    return response.json()


def convert_to_csv(data: dict, output_file: str) -> str:
    """Convert FRED JSON data to CSV format and save to file"""
    observations = data.get("observations", [])

    if not observations:
        return "No data available"

    # Create CSV string
    csv_lines = ["date,value"]

    for obs in observations:
        date = obs.get("date", "")
        value = obs.get("value", "")
        csv_lines.append(f"{date},{value}")

    csv_content = "\n".join(csv_lines)

    # Save to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(csv_content)

    return csv_content


def get_delinquency_data(years: int = 7, output_file: str = "output/delinquency_data.csv") -> dict:
    """
    Main function to fetch and save delinquency data

    Args:
        years: Number of years of historical data to fetch
        output_file: Path to save the CSV file

    Returns:
        dict with 'success', 'message', 'csv_content', and 'num_observations'
    """
    try:
        # Resolve output path relative to script directory
        if not os.path.isabs(output_file):
            output_file = str(SCRIPT_DIR / output_file)

        # Fetch data from FRED
        fred_data = fetch_fred_data(years)

        # Convert to CSV and save
        csv_content = convert_to_csv(fred_data, output_file)

        # Count observations
        num_observations = len(fred_data.get("observations", []))

        # Format year(s) correctly
        year_text = "year" if years == 1 else "years"

        message = f"""Credit card delinquency data from the last {years} {year_text} has been saved to {output_file}.

{csv_content}

Total observations: {num_observations}"""

        return {
            "success": True,
            "message": message,
            "csv_content": csv_content,
            "num_observations": num_observations
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error fetching delinquency data: {str(e)}",
            "csv_content": None,
            "num_observations": 0
        }
