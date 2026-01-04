# KaliDocker 🐉

Modern security operations platform with Kali Linux tools, powered by Docker Compose.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Next.js   │───▶│   FastAPI   │───▶│    Kali     │     │
│  │  UI :3443   │    │  API :8000  │    │   Tools     │     │
│  └─────────────┘    └──────┬──────┘    └─────────────┘     │
│                            │                                 │
│                     ┌──────▼──────┐                         │
│                     │  PostgreSQL │                         │
│                     │    :5432    │                         │
│                     └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/sealmindset/KaliDocker.git
cd KaliDocker

# Copy environment template
cp .env.example .env

# Start all services
docker compose up -d

# Open the UI
open http://localhost:3443
```

## Services

| Service | Description | Port |
|---------|-------------|------|
| `ui` | Next.js web interface | 3443 |
| `api` | FastAPI backend | 8000 |
| `postgres` | PostgreSQL database | 5432 |
| `kali` | Base Kali tools | - |
| `kali-msf` | Metasploit Framework | - |

## Usage

### Start with Default Services
```bash
docker compose up -d
```

### Start with Kali Tools
```bash
docker compose --profile tools up -d
```

### Start with Metasploit
```bash
docker compose --profile msf up -d
```

### Interactive Kali Shell
```bash
docker compose run --rm kali
```

### Using Helper Scripts
```bash
# Start services
./scripts/start.sh          # Default (UI, API, DB)
./scripts/start.sh tools    # Include Kali tools
./scripts/start.sh msf      # Include Metasploit
./scripts/start.sh all      # Everything

# Development mode with hot-reload
./scripts/dev.sh

# Cleanup
./scripts/cleanup.sh            # Stop and clean containers
./scripts/cleanup.sh --volumes  # Also remove volumes
./scripts/cleanup.sh --rebuild  # Clean and rebuild images
```

## Environment Variables

Key settings in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `UI_PORT` | 3443 | Next.js UI port |
| `API_PORT` | 8000 | FastAPI backend port |
| `POSTGRES_PASSWORD` | postgres | Database password |
| `HTTP_PROXY` | (empty) | HTTP proxy URL for traffic interception |
| `HTTPS_PROXY` | (empty) | HTTPS proxy URL for traffic interception |
| `NO_PROXY` | localhost,... | Hosts to bypass proxy |

### Proxy Configuration (Burp Suite / ZAP)

To route all HTTP/HTTPS traffic from Kali tools through a proxy:

```bash
# Edit .env and set proxy URL
HTTP_PROXY=http://host.docker.internal:8080
HTTPS_PROXY=http://host.docker.internal:8080

# Restart containers
docker compose --profile msf up -d
```

**Note:** `host.docker.internal` points to your Mac's localhost from inside Docker.

## Security Tools

### Pre-installed Tools

The container includes a **minimal toolset** for fast builds:

| Tool | Purpose |
|------|---------|
| nmap | Network/port scanning |
| nuclei | Vulnerability scanning |
| ffuf | Web fuzzing |
| arjun | API parameter discovery |
| httpx | HTTP probing |
| nikto, dirb, sqlmap | Web scanning |
| metasploit | Exploitation framework |

### Installing Additional Tools

Need more tools? Install on-demand:

```bash
# Install a specific tool
docker compose exec kali-msf apt update && apt install -y <tool-name>

# Install a Kali metapackage (adds multiple tools)
docker compose exec kali-msf apt install -y kali-tools-web
```

**Available metapackages:** `kali-tools-top10`, `kali-tools-web`, `kali-tools-exploitation`, `kali-tools-forensics`

> **Note:** The base image is minimal. Kali has 600+ tools - install what you need.

## API Documentation

Once running, visit: http://localhost:8000/docs

## Development

```bash
# Run development servers with hot-reload
./scripts/dev.sh
```

## Volumes

Data persists in Docker volumes:
- `kalidocker-postgres-data` - Database
- `kalidocker-kali-data` - Kali home directory

## MCP Server (AI Integration)

KaliDocker includes an MCP server that exposes security tools to AI assistants like Claude.

### Available Tools
| Tool | Function | Description |
|------|----------|-------------|
| nmap | `scan_network` | Network/port scanning |
| nuclei | `scan_vulnerabilities` | Vulnerability detection |
| ffuf | `fuzz_endpoints` | Web endpoint fuzzing |
| arjun | `discover_parameters` | API parameter discovery |
| httpx | `probe_urls` | HTTP probing |

### Setup for Claude Desktop

1. Install dependencies:
```bash
cd mcp && pip install -r requirements.txt
```

2. Add to `~/.config/claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "kalidocker-security": {
      "command": "/path/to/KaliDocker/mcp/run_standalone.sh"
    }
  }
}
```

3. Restart Claude Desktop

### Alternative: Run in Docker
```bash
docker compose --profile mcp up -d
```

## License

GPL-3.0 - See [LICENSE](LICENSE)
