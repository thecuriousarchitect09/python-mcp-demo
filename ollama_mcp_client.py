"""
ollama_mcp_client.py
Connects Ollama (local LLM) to the MCP demo server.

Flow:
  1. Start server.py via stdio
  2. Fetch its tools and convert to Ollama tool format
  3. Send user message to Ollama with tools attached
  4. If Ollama calls a tool, forward the call to the MCP server
  5. Feed the result back to Ollama for a final answer

Requirements:
    pip install mcp ollama
    ollama pull qwen2.5:7b   (or any tool-capable model)
"""

import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MODEL = "gemma4:e2b"          # swap to llama3.2:3b, mistral, etc.
SERVER_SCRIPT = "server.py"   # path to your MCP server


# ── helpers ──────────────────────────────────────────────────────────────────

def mcp_tool_to_ollama(tool) -> dict:
    """Convert an MCP Tool object to Ollama's tool schema."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema,
        },
    }


async def call_mcp_tool(session: ClientSession, name: str, args: dict) -> str:
    """Call a tool on the MCP server and return its text result."""
    result = await session.call_tool(name, args)
    return result.content[0].text


# ── main loop ────────────────────────────────────────────────────────────────

async def chat(user_message: str):
    server_params = StdioServerParameters(
        command="python",
        args=[SERVER_SCRIPT],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Discover tools from the MCP server
            tools_result = await session.list_tools()
            ollama_tools = [mcp_tool_to_ollama(t) for t in tools_result.tools]
            print(f"[MCP] Tools available: {[t.name for t in tools_result.tools]}\n")

            # 2. Send user message to Ollama
            messages = [{"role": "user", "content": user_message}]
            print(f"User: {user_message}")

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools,
            )
            msg = response.message

            # 3. Agentic loop: handle tool calls until model gives a final answer
            while msg.tool_calls:
                messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

                for tc in msg.tool_calls:
                    fn = tc.function
                    print(f"[Ollama] Calling tool: {fn.name}({fn.arguments})")
                    tool_result = await call_mcp_tool(session, fn.name, fn.arguments)
                    print(f"[MCP]    Result: {tool_result}")

                    messages.append({
                        "role": "tool",
                        "content": tool_result,
                    })

                # Feed results back to Ollama
                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )
                msg = response.message

            print(f"\nAssistant: {msg.content}")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(chat("What is 42 + 58? Also, what's the weather like in London? and Also return current system details"))
