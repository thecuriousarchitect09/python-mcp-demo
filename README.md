# 🎥 YouTube Tutorial

Want to understand how this project works step by step?

[Video walkthrough](https://youtu.be/npZSxa5GWbw)

# 🚀 Simple Python MCP + Ollama Demo

A lightweight, beginner-friendly demonstration of the **Model Context Protocol (MCP)** using Python and **Ollama**.

This project shows how a local LLM can discover and invoke MCP tools exposed by an MCP server through a simple bridge application.

---

# 📂 Project Structure

| File | Description |
|--------|-------------|
| `server.py` | MCP server exposing tools such as `add` and `get_weather` |
| `ollama_mcp_client.py` | MCP client and Ollama bridge |
| `requirements.txt` | Python dependencies |

---

# 🎯 What You'll Learn

- How MCP servers expose tools
- How MCP clients discover tools dynamically
- How tool calling works with local LLMs
- How Ollama can use MCP tools
- The complete MCP request/response lifecycle

---

# 🏗 Architecture

```text
┌─────────────────────┐      stdio      ┌─────────────┐
│ ollama_mcp_client.py│ ◄─────────────► │  server.py  │
└─────────────────────┘                 └─────────────┘
              │
              ▼
       Ollama (gemma4:e2b)
              │
              ▼
        Tool Calls via MCP
```

---

# ⚙️ Prerequisites

## Install Ollama

Download and install Ollama:

https://ollama.com

Verify installation:

```bash
ollama --version
```

---

## Pull the Model

This demo uses:

```bash
ollama pull gemma4:e2b
```

Verify the model is available:

```bash
ollama list
```

---

# 📦 Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install mcp ollama
```

---

# ▶️ Running the Demo

Start the application:

```bash
python ollama_mcp_client.py
```

The client automatically:

1. Starts the MCP server
2. Discovers available MCP tools
3. Converts MCP tools into Ollama tool definitions
4. Sends prompts and tools to the model
5. Executes tool calls through MCP
6. Returns the final AI-generated response

---

# 🛠 Available Tools

The demo server exposes two example tools:

| Tool | Description |
|--------|-------------|
| `add(a, b)` | Adds two numbers |
| `get_weather(city)` | Returns mock weather information |

---

# 💬 Example Session

```text
[MCP] Tools available:
['add', 'get_weather']

Using model: gemma4:e2b

User:
What is 42 + 58? Also, what's the weather like in London?

[Ollama] Calling tool:
add({'a': 42, 'b': 58})

[MCP] Result:
100

[Ollama] Calling tool:
get_weather({'city': 'London'})

[MCP] Result:
Cloudy, 15°C

Assistant:
42 + 58 equals 100.
The weather in London is currently Cloudy, 15°C.
```

---

# 🔄 How It Works

## Step 1: Start MCP Server

The client launches `server.py` as a subprocess using the MCP stdio transport.

```text
ollama_mcp_client.py
        │
        ▼
    server.py
```

---

## Step 2: Discover Tools

The client requests the list of available MCP tools.

```text
list_tools()
      │
      ▼
server.py
      │
      ▼
[add, get_weather]
```

---

## Step 3: Convert Tools for Ollama

MCP tool schemas are transformed into Ollama-compatible tool definitions.

```text
MCP Tool Schema
       │
       ▼
Ollama Tool Definition
```

---

## Step 4: Send Prompt to Ollama

The user prompt and available tools are sent to the local model.

```text
User Prompt
      +
Available Tools
      │
      ▼
Gemma 4
```

---

## Step 5: Execute Tool Calls

When the model requests a tool:

```text
Gemma 4
    │
    ▼
add(a, b)
    │
    ▼
MCP Server
```

The client forwards the request to the MCP server and retrieves the result.

---

## Step 6: Generate Final Response

Tool results are fed back to the model.

```text
Tool Result
     │
     ▼
Gemma 4
     │
     ▼
Final Answer
```

---

# 🔁 End-to-End Flow

```text
User
 │
 ▼
ollama_mcp_client.py
 │
 ├─ Starts server.py
 ├─ Discovers MCP tools
 ├─ Converts tools for Ollama
 ├─ Sends prompt + tools
 │
 ▼
Gemma 4 (Ollama)
 │
 ├─ Requests tool execution
 ▼
server.py
 │
 └─ Returns result
 ▲
 │
Gemma 4
 │
 ▼
Final Response
```

---

# ➕ Adding a New Tool

## 1. Define the Tool

In `server.py`, add a tool description.

Example:

```python
Tool(
    name="multiply",
    description="Multiply two numbers",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        }
    }
)
```

---

## 2. Implement the Tool Logic

Add handling logic:

```python
elif name == "multiply":
    return args["a"] * args["b"]
```

---

## 3. Restart the Demo

```bash
python ollama_mcp_client.py
```

The tool will automatically appear in the discovered tool list.

No changes are required in the Ollama integration layer.

---

# 🔧 Technical Details

| Component | Value |
|------------|--------|
| Protocol | Model Context Protocol (MCP) |
| Transport | stdio |
| RPC Format | JSON-RPC 2.0 |
| MCP SDK | Python MCP SDK |
| LLM Runtime | Ollama |
| Model | gemma4:e2b |
| Tool Discovery | Dynamic |
| Tool Execution | Request / Response |

---

# 🚀 Why MCP?

MCP provides a standard way for AI applications to:

- Discover tools dynamically
- Invoke tools consistently
- Connect to external systems
- Share integrations across models and frameworks

Instead of building custom integrations for every LLM, you expose capabilities once through MCP and reuse them everywhere.

---

# 📚 References

- MCP Documentation: https://modelcontextprotocol.io
- Python MCP SDK: https://github.com/modelcontextprotocol/python-sdk
- Ollama Documentation: https://ollama.com/docs

---

# ⭐ Next Steps

After understanding this demo, try extending it with:

- Database tools
- REST API integrations
- File system access
- Vector databases
- RAG workflows
- Agent-to-agent communication
- Multi-tool orchestration

This project is intentionally simple so you can focus on understanding the core MCP concepts before moving to production-grade AI systems.
