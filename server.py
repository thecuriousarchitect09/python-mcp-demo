"""
Simple MCP Server Demo
Exposes two tools: add and get_weather (mocked)
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import sys
import psutil
import json

app = Server("demo-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="get_weather",
            description="Get mock weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        ),
        types.Tool(
            name="systemInfo",
            description="Get system information",
            inputSchema={
                "type": "object"
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [types.TextContent(type="text", text=str(result))]

    elif name == "get_weather":
        city = arguments["city"]
        # Mock weather data
        weather_db = {
            "london": "Cloudy, 15°C",
            "tokyo": "Sunny, 28°C",
            "new york": "Rainy, 18°C",
        }
        weather = weather_db.get(city.lower(), f"No data for {city}")
        return [types.TextContent(type="text", text=weather)]
    
    elif name == "systemInfo":
        total_mem = psutil.virtual_memory().total
        systemInfo = {
                "platform": sys.platform,
                "memory":f"{total_mem / (1024**3):.2f} GB"
              }
        
        return [types.TextContent(type="text", text=json.dumps(systemInfo))]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
