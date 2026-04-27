# StrideHive

StrideHive connects motion and health data from your existing watch and phone to the people who need it — your trainer, physio, or coach. No extra hardware. Just wear your watch and let StrideHive handle the rest.

## Use Cases

- **ACL Rehab** — Monitor compensation patterns daily, not just at weekly clinic visits
- **Remote Personal Training** — Give trainers visibility into client effort and consistency
- **Sports Academies** — Track athlete recovery and flag overtraining before injury
- **Post-Surgical Recovery** — Track gait asymmetry as a key recovery metric

## What We're Building Now

An MCP server (CLI) that exposes StrideHive's health and session data as tools for Claude Code / Claude Desktop.

Once set up, you can ask Claude things like:
- "Show me Alex's session data for this week"
- "Any anomalies in the last 7 days?"
- "Compare Alex's recovery trend to last month"

Claude calls the tools, gets the data, and responds.

### Setup

```json
{
  "mcpServers": {
    "StrideHive": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

## License

MIT
