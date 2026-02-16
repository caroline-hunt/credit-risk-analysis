#!/usr/bin/env python3
"""
MCP Server for FRED Credit Card Delinquency Data
Exposes a tool to fetch DRCCLACBS series data from FRED API
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from tools.delinquency_tool import get_delinquency_data

# Initialize MCP server
app = Server("delinquency")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_credit_card_delinquency_data",
            description="Fetch credit card delinquency rate data from FRED (series DRCCLACBS). Returns data in CSV format and saves it to a file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "years": {
                        "type": "integer",
                        "description": "Number of years of historical data to fetch (default: 7)",
                        "default": 7
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output CSV file path (default: output/delinquency_data.csv)",
                        "default": "output/delinquency_data.csv"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    if name != "get_credit_card_delinquency_data":
        raise ValueError(f"Unknown tool: {name}")

    # Get parameters with defaults
    years = arguments.get("years", 7)
    output_file = arguments.get("output_file", "output/delinquency_data.csv")

    # Call the tool implementation
    result = get_delinquency_data(years=years, output_file=output_file)

    return [TextContent(type="text", text=result["message"])]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
