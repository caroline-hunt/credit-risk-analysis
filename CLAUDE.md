# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a credit risk analysis project that provides an MCP (Model Context Protocol) server for fetching and analyzing credit card delinquency data from the Federal Reserve Economic Data (FRED) API. The project focuses on analyzing FRED series DRCCLACBS (Delinquency Rate on Credit Card Loans, All Commercial Banks).

## Architecture

### Core Components

**MCP Server (`src/server.py`)**
- Exposes the `get_credit_card_delinquency_data` tool to Claude Code
- Runs as a stdio-based MCP server
- Delegates to `src/tools/delinquency_tool.py` for data fetching

**Data Fetching (`src/tools/delinquency_tool.py`)**
- Handles FRED API communication using httpx
- Fetches quarterly delinquency rate data
- Converts JSON responses to CSV format
- Saves data to `output/` directory
- Requires `FRED_API_KEY` environment variable from `.env` file

**Data Utilities (`src/utils/data_cleaning.py`)**
- Provides `clean_delinquency_data()` function for data preprocessing
- Handles: duplicate removal, missing value detection, date standardization, value rounding
- Used by analysis scripts and available for import

**Analysis Scripts (`scripts/`)**
- `clean_data.py`: CLI wrapper for data cleaning utilities
- `analyze_delinquency.py`: Generates time series plots with trend analysis, identifies sharp increases, produces summary statistics

### Data Flow

1. User requests delinquency data via Claude Code → MCP tool invoked
2. `delinquency_tool.py` fetches from FRED API → saves raw CSV to `output/delinquency_data.csv`
3. User can clean data → `clean_data.py` processes and saves to `output/delinquency_data_cleaned.csv`
4. User can analyze → `analyze_delinquency.py` generates visualizations and statistics in `output/`

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure FRED API key (required)
# Edit .env and add: FRED_API_KEY=your_key_here
```

### Running Scripts
```bash
# Clean delinquency data
python scripts/clean_data.py

# Analyze and visualize delinquency trends
python scripts/analyze_delinquency.py
```

### MCP Server
The server is typically invoked by Claude Code via the MCP configuration in `.mcp.json`. To test manually:
```bash
python src/server.py
```

## Key Configuration

**Environment Variables (`.env`)**
- `FRED_API_KEY`: Required for FRED API access. Get from https://fred.stlouisfed.org/

**MCP Configuration (`.mcp.json`)**
- Defines how Claude Code connects to the MCP server
- Points to `src/server.py` as the entry point

## Development Notes

### Adding New Analysis Scripts
- Import utilities from `src.utils.data_cleaning`
- Read cleaned data from `output/delinquency_data_cleaned.csv`
- Save outputs to `output/` directory (auto-created)

### Working with FRED Data
- Data is quarterly frequency (Jan, Apr, Jul, Oct)
- Values are in percentage points (e.g., 3.17 = 3.17%)
- FRED uses '.' for missing values (handled by cleaning utilities)
- Series ID: DRCCLACBS

### Path Resolution
- All scripts use pathlib for cross-platform compatibility
- Output paths are resolved relative to project root
- `SCRIPT_DIR` in delinquency_tool.py points to project root

### Data Cleaning Process
The cleaning pipeline follows this order:
1. Remove duplicate rows
2. Handle missing values (drops rows with missing dates/values)
3. Standardize dates to YYYY-MM-DD format
4. Round values to 2 decimal places
5. Sort by date ascending

### Analysis Conventions
- Sharp increases defined as: >1% period-over-period change OR >0.03 percentage point change
- Plots saved as PNG at 300 DPI
- Summary statistics exported to CSV for further use
