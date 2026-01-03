# KaliDocker MCP Server

Model Context Protocol (MCP) server that exposes security scanning tools to AI assistants like Claude, GPT, and other MCP-compatible systems.

## Overview

This MCP server allows AI assistants to execute security scans by invoking tools that run inside the KaliDocker containers. All tools execute in an isolated Docker environment with proper timeouts and error handling.

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  AI Assistant   │────▶│   MCP Server    │────▶│  Kali Container │
│  (Claude/GPT)   │     │   (Python)      │     │  (Docker)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Available Tools

| Tool | Function | Description |
|------|----------|-------------|
| nmap | `scan_network` | Network discovery, port scanning, service detection |
| nuclei | `scan_vulnerabilities` | Template-based vulnerability scanning |
| ffuf | `fuzz_endpoints` | Web endpoint fuzzing and discovery |
| arjun | `discover_parameters` | Hidden API parameter discovery |
| httpx | `probe_urls` | HTTP endpoint probing with status codes |

---

## Installation

### Prerequisites

- Python 3.10+
- Docker Desktop running
- KaliDocker containers built (`docker compose build`)

### Option 1: Standalone (Recommended for Claude Desktop)

```bash
# Navigate to MCP directory
cd /path/to/KaliDocker/mcp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Docker

```bash
# Build and run MCP service
docker compose --profile mcp up -d
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KALIDOCKER_COMPOSE_PATH` | Parent directory | Path to docker-compose.yml |
| `KALIDOCKER_CONTAINER` | `kalidocker-kali-msf-1` | Container name for tool execution |
| `USE_DOCKER` | `true` | Use Docker for tool execution |
| `NMAP_TIMEOUT` | `300` | Nmap scan timeout (seconds) |
| `NUCLEI_TIMEOUT` | `600` | Nuclei scan timeout (seconds) |
| `FFUF_TIMEOUT` | `300` | Ffuf fuzzing timeout (seconds) |
| `ARJUN_TIMEOUT` | `300` | Arjun discovery timeout (seconds) |
| `HTTPX_TIMEOUT` | `120` | Httpx probing timeout (seconds) |

---

## Claude Desktop Setup

### 1. Start KaliDocker Containers

```bash
cd /path/to/KaliDocker
docker compose --profile msf up -d
```

### 2. Configure Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json` (Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kalidocker-security": {
      "command": "/path/to/KaliDocker/mcp/run_standalone.sh",
      "args": [],
      "env": {
        "KALIDOCKER_COMPOSE_PATH": "/path/to/KaliDocker"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. You should see the security tools available.

---

## Tool Reference

### scan_network (nmap)

Network discovery and port scanning.

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `target` | ✅ | - | IP, hostname, or CIDR range |
| `ports` | ❌ | All | Port specification (e.g., "22,80,443") |
| `scan_type` | ❌ | `sV` | Nmap scan flags |
| `extra_args` | ❌ | - | Additional nmap arguments |

**Example:**
```
Scan ports 22, 80, 443 on example.com with version detection
```

---

### scan_vulnerabilities (nuclei)

Template-based vulnerability scanning.

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `target` | ✅ | - | Target URL |
| `templates` | ❌ | All | Template category (cves, exposures) |
| `severity` | ❌ | All | Filter: critical, high, medium, low |
| `extra_args` | ❌ | - | Additional nuclei arguments |

**Example:**
```
Scan https://api.example.com for high severity vulnerabilities
```

---

### fuzz_endpoints (ffuf)

Web endpoint and directory fuzzing.

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | ✅ | - | URL with FUZZ keyword |
| `wordlist` | ❌ | `/usr/share/wordlists/dirb/common.txt` | Wordlist path |
| `method` | ❌ | `GET` | HTTP method |
| `extra_args` | ❌ | - | Additional ffuf arguments |

**Example:**
```
Fuzz https://api.example.com/FUZZ to find hidden endpoints
```

---

### discover_parameters (arjun)

Hidden API parameter discovery.

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | ✅ | - | Target API URL |
| `method` | ❌ | `GET` | HTTP method |
| `extra_args` | ❌ | - | Additional arjun arguments |

**Example:**
```
Discover hidden parameters on https://api.example.com/v1/users
```

---

### probe_urls (httpx)

HTTP endpoint probing with metadata.

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `urls` | ✅ | - | URL or comma-separated list |
| `extra_args` | ❌ | - | Additional httpx arguments |

**Example:**
```
Probe https://example.com, https://api.example.com for status codes
```

---

## Security Considerations

⚠️ **Important:** Only scan systems you have permission to test.

- All scans execute inside Docker containers
- Network traffic originates from Docker network
- Use `HTTP_PROXY` environment variable to route through Burp/ZAP
- Scan results may contain sensitive information

---

## Troubleshooting

### "Container not running"

```bash
docker compose --profile msf up -d
```

### "Command timed out"

Increase timeout in environment:
```bash
export NMAP_TIMEOUT=600
```

### "Tool not found"

Rebuild Kali container:
```bash
docker compose build --no-cache kali-msf
```

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | Main MCP server implementation |
| `tools.py` | Security tool wrappers |
| `config.py` | Configuration management |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Docker deployment |
| `run_standalone.sh` | Mac standalone runner |
| `claude_desktop_config.json` | Example Claude config |

---

## License

GPL-3.0 - Part of the KaliDocker project.
