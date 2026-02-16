# FRED Credit Card Delinquency MCP Server

An MCP server that provides credit card delinquency rate data from the Federal Reserve Economic Data (FRED) API.

## Features

- Fetches FRED series DRCCLACBS (Delinquency Rate on Credit Card Loans, All Commercial Banks)
- Returns data in CSV format
- Automatically saves data to a CSV file
- Configurable time range (default: 7 years)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a FRED API Key

1. Go to https://fred.stlouisfed.org/
2. Create a free account
3. Request an API key at https://fred.stlouisfed.org/docs/api/api_key.html
4. Copy your API key

### 3. Configure Environment Variables

Edit the `.env` file in the project root and add your FRED API key:

```
FRED_API_KEY=your_actual_api_key_here
```

The `.env` file has already been created for you.

### 4. Configure Claude Code

Add this MCP server to your Claude Code configuration:

**On macOS/Linux:** Edit `~/.claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "delinquency": {
      "command": "python3",
      "args": ["/Users/carolinehunt/credit-risk/server.py"]
    }
  }
}
```

**Note:**
- Replace the path with the actual path to your `server.py` file
- The API key is read from the `.env` file, so no need to add it here

### 5. Restart Claude Code

After updating the configuration, restart Claude Code for the changes to take effect.

## Usage

Once configured, you can ask Claude Code to fetch delinquency data:

**Example prompts:**
- "Get credit card delinquency data for the last 7 years"
- "Fetch credit card delinquency rates for the past 10 years"
- "Get delinquency data and save it to my_data.csv"

## Tool Details

### get_credit_card_delinquency_data

**Parameters:**
- `years` (integer, optional): Number of years of historical data to fetch (default: 7)
- `output_file` (string, optional): Output CSV file path (default: output/delinquency_data.csv)

**Returns:**
- CSV formatted data with columns: date, value
- Saves data to the specified output file in the `output/` directory

## Data Source

This server fetches data from the Federal Reserve Bank of St. Louis FRED API:
- Series: DRCCLACBS (Delinquency Rate on Credit Card Loans, All Commercial Banks)
- Frequency: Quarterly
- Units: Percent
- Source: Board of Governors of the Federal Reserve System (US)

## License

MIT
