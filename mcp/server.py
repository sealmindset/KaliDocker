#!/usr/bin/env python3
"""
KaliDocker MCP Server
Exposes security scanning tools via Model Context Protocol
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from tools import (
    scan_network,
    scan_vulnerabilities,
    fuzz_endpoints,
    discover_parameters,
    probe_urls
)

# Create the MCP server
server = Server("kalidocker-security")


# =============================================================================
# Tool Definitions
# =============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available security tools"""
    return [
        Tool(
            name="scan_network",
            description="Run nmap network scan for port discovery and service detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target IP, hostname, or CIDR range (e.g., '192.168.1.1', 'example.com', '10.0.0.0/24')"
                    },
                    "ports": {
                        "type": "string",
                        "description": "Port specification (e.g., '22,80,443' or '1-1000'). Optional."
                    },
                    "scan_type": {
                        "type": "string",
                        "description": "Nmap scan type flags (default: 'sV' for version detection)",
                        "default": "sV"
                    },
                    "extra_args": {
                        "type": "string",
                        "description": "Additional nmap arguments"
                    }
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="scan_vulnerabilities",
            description="Run nuclei vulnerability scanner with templates to detect security issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target URL (e.g., 'https://example.com')"
                    },
                    "templates": {
                        "type": "string",
                        "description": "Template category or path (e.g., 'cves', 'exposures', 'vulnerabilities')"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Filter by severity: critical, high, medium, low, info"
                    },
                    "extra_args": {
                        "type": "string",
                        "description": "Additional nuclei arguments"
                    }
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="fuzz_endpoints",
            description="Run ffuf to discover hidden endpoints, directories, and files via fuzzing",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL with FUZZ keyword (e.g., 'https://example.com/FUZZ')"
                    },
                    "wordlist": {
                        "type": "string",
                        "description": "Path to wordlist file",
                        "default": "/usr/share/wordlists/dirb/common.txt"
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, etc.)",
                        "default": "GET"
                    },
                    "extra_args": {
                        "type": "string",
                        "description": "Additional ffuf arguments"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="discover_parameters",
            description="Run arjun to discover hidden API parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target API URL"
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST)",
                        "default": "GET"
                    },
                    "extra_args": {
                        "type": "string",
                        "description": "Additional arjun arguments"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="probe_urls",
            description="Run httpx to probe URLs and get status codes, content types, and titles",
            inputSchema={
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "string",
                        "description": "Single URL or comma-separated list of URLs"
                    },
                    "extra_args": {
                        "type": "string",
                        "description": "Additional httpx arguments"
                    }
                },
                "required": ["urls"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute the requested security tool"""
    
    try:
        if name == "scan_network":
            result = await scan_network(
                target=arguments["target"],
                ports=arguments.get("ports"),
                scan_type=arguments.get("scan_type", "sV"),
                extra_args=arguments.get("extra_args")
            )
        elif name == "scan_vulnerabilities":
            result = await scan_vulnerabilities(
                target=arguments["target"],
                templates=arguments.get("templates"),
                severity=arguments.get("severity"),
                extra_args=arguments.get("extra_args")
            )
        elif name == "fuzz_endpoints":
            result = await fuzz_endpoints(
                url=arguments["url"],
                wordlist=arguments.get("wordlist", "/usr/share/wordlists/dirb/common.txt"),
                method=arguments.get("method", "GET"),
                extra_args=arguments.get("extra_args")
            )
        elif name == "discover_parameters":
            result = await discover_parameters(
                url=arguments["url"],
                method=arguments.get("method", "GET"),
                extra_args=arguments.get("extra_args")
            )
        elif name == "probe_urls":
            result = await probe_urls(
                urls=arguments["urls"],
                extra_args=arguments.get("extra_args")
            )
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
                "tool": name
            }, indent=2)
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
