# KaliDocker Cheatsheet

Quick reference for running KaliDocker as an MCP security platform.

---

## 🚀 Quick Start

```bash
# One-time setup
./setup.sh

# Start services
docker compose --profile msf up -d

# Verify MCP
claude mcp list
```

---

## 📡 Using with Claude Code CLI

```bash
# Start Claude Code
claude

# Example prompts:
> Use scan_network to scan example.com for ports 80,443
> Use scan_vulnerabilities to check https://api.example.com for high severity issues
> Use fuzz_endpoints to find hidden paths on https://example.com/FUZZ
> Use discover_parameters on https://api.example.com/users
> Use probe_urls to check https://example.com, https://api.example.com
```

---

## 🛠️ MCP Tools Reference

| Tool | Command | Example |
|------|---------|---------|
| **nmap** | `scan_network` | Scan ports, detect services |
| **nuclei** | `scan_vulnerabilities` | CVE & vulnerability scanning |
| **ffuf** | `fuzz_endpoints` | Directory/endpoint fuzzing |
| **arjun** | `discover_parameters` | Find hidden API params |
| **httpx** | `probe_urls` | HTTP probing with status |

---

## 🐳 Docker Commands

```bash
# Start with Metasploit
docker compose --profile msf up -d

# Start all services
docker compose --profile msf --profile tools up -d

# Stop everything
docker compose down

# Rebuild containers
docker compose build --no-cache kali-msf

# Interactive shell
docker compose exec -it kali-msf zsh
```

---

## 🔍 Direct Tool Usage (without MCP)

```bash
# Nmap scan
docker compose exec kali-msf nmap -sV -p 22,80,443 target.com

# Nuclei scan
docker compose exec kali-msf nuclei -u https://target.com -severity high

# Ffuf fuzzing
docker compose exec kali-msf ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Arjun parameter discovery
docker compose exec kali-msf arjun -u https://api.target.com/endpoint

# Metasploit
docker compose exec -it kali-msf msfconsole
```

---

## 🔐 Proxy Configuration

Route traffic through Burp Suite or ZAP:

```bash
# Edit .env
HTTP_PROXY=http://host.docker.internal:8080
HTTPS_PROXY=http://host.docker.internal:8080

# Restart
docker compose --profile msf up -d
```

---

## 🩺 Troubleshooting

```bash
# Check container status
docker compose ps

# View logs
docker compose logs -f kali-msf

# Verify MCP connection
claude mcp list

# Rebuild if tools missing
docker compose build --no-cache kali-msf
docker compose --profile msf up -d
```

---

## 📦 Pre-installed Tools

The container includes a **minimal toolset**, not all 600+ Kali tools:

| Pre-installed | Category |
|--------------|----------|
| nmap, nikto, dirb, sqlmap | Scanning |
| nuclei, httpx, ffuf, subfinder | Discovery |
| arjun, shodan | API/Recon |
| metasploit, exploitdb | Exploitation |
| proxychains, tor | Anonymity |

---

## 📥 Installing Additional Tools

Need a tool not included? Install it on-demand:

```bash
# Install a specific tool
docker compose exec kali-msf apt update
docker compose exec kali-msf apt install -y <tool-name>

# Example: Install Burp Suite
docker compose exec kali-msf apt install -y burpsuite

# Install a Kali metapackage
docker compose exec kali-msf apt install -y kali-tools-web
```

### Kali Metapackages

| Package | Description | Size |
|---------|-------------|------|
| `kali-tools-top10` | Top 10 popular tools | ~1GB |
| `kali-tools-web` | Web app testing | ~2GB |
| `kali-tools-exploitation` | Exploitation tools | ~1.5GB |
| `kali-tools-forensics` | Forensics/recovery | ~2GB |

> **Note:** Installed tools persist in the `kali-data` volume but not across container rebuilds.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `setup.sh` | One-time setup script |
| `.env` | Environment configuration |
| `docker-compose.yml` | Service definitions |
| `mcp/server.py` | MCP server code |
| `mcp/run_standalone.sh` | MCP runner script |

