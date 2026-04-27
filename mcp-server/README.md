# StrideHive MCP Server

MCP server that exposes health and fitness data tools for Claude Code / Claude Desktop.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

## Quick Start

```bash
cd mcp-server
uv sync
```

## Configure for Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "StrideHive": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/StrideHive/mcp-server",
        "run",
        "stridehive"
      ]
    }
  }
}
```

## Configure for Claude Code

```bash
claude mcp add stridehive -- uv --directory /ABSOLUTE/PATH/TO/StrideHive/mcp-server run stridehive
```

## Test with MCP Inspector

```bash
cd mcp-server
uv run mcp dev src/stridehive/server.py
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_sessions` | List recent training sessions for an athlete |
| `get_session_detail` | Get full detail of a specific session |
| `get_health_metrics` | Get daily health metrics over a time period |
| `get_anomalies` | Detect anomalies in recent health data |
| `compare_trends` | Compare recent vs historical metric trends |
| `get_recovery_summary` | Overall recovery status assessment |

## Sample Athletes

| ID | Name | Use Case |
|----|------|----------|
| `athlete_001` | Alex Rivera | ACL rehab, gait tracking |
| `athlete_002` | Jordan Chen | Remote personal training |
| `athlete_003` | Sam Okafor | Academy overtraining detection |

## Example Queries

- "Show me Alex's sessions this week"
- "Get Sam's HRV for the last 14 days"
- "Are there any anomalies for Jordan in the last 7 days?"
- "Compare Alex's resting heart rate — last week vs last month"
- "Give me Sam's recovery summary"
