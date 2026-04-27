"""StrideHive MCP Server — entry point.

Exposes health and fitness data tools for Claude Code / Claude Desktop.
"""

import logging
import sys

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("stridehive")

mcp = FastMCP("StrideHive")

# Import tool modules — each registers tools on `mcp` via @mcp.tool() decorators
import stridehive.tools  # noqa: E402, F401


def main():
    """Entry point for the StrideHive MCP server."""
    logger.info("Starting StrideHive MCP server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
