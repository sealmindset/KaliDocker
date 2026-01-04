#!/bin/bash
# KaliDocker Setup Script
# Ensures all dependencies are installed and configured

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 KaliDocker Setup"
echo "==================="

# Check Docker
echo ""
echo "1️⃣  Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop."
    exit 1
fi
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✅ Docker is running"

# Check docker compose
echo ""
echo "2️⃣  Checking Docker Compose..."
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found."
    exit 1
fi
echo "✅ Docker Compose available"

# Create .env if missing
echo ""
echo "3️⃣  Checking environment..."
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "📝 Creating .env from .env.example..."
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
fi
echo "✅ Environment configured"

# Build containers
echo ""
echo "4️⃣  Building Docker images..."
docker compose -f "$SCRIPT_DIR/docker-compose.yml" build

# Setup MCP Python environment
echo ""
echo "5️⃣  Setting up MCP Python environment..."
if [ ! -d "$SCRIPT_DIR/mcp/.venv" ]; then
    python3 -m venv "$SCRIPT_DIR/mcp/.venv"
fi
source "$SCRIPT_DIR/mcp/.venv/bin/activate"
pip install -q -r "$SCRIPT_DIR/mcp/requirements.txt"
deactivate
echo "✅ MCP dependencies installed"

# Make scripts executable
echo ""
echo "6️⃣  Setting permissions..."
chmod +x "$SCRIPT_DIR/mcp/run_standalone.sh"
chmod +x "$SCRIPT_DIR/scripts/"*.sh 2>/dev/null || true
echo "✅ Scripts are executable"

# Start containers
echo ""
echo "7️⃣  Starting services..."
docker compose -f "$SCRIPT_DIR/docker-compose.yml" --profile msf up -d
echo "✅ Services started"

# Check Claude Code CLI
echo ""
echo "8️⃣  Configuring Claude Code CLI..."
if command -v claude &> /dev/null; then
    # Check if MCP already configured
    if claude mcp list 2>/dev/null | grep -q "kalidocker-security"; then
        echo "✅ MCP already configured in Claude Code"
    else
        echo "📝 Adding MCP server to Claude Code..."
        claude mcp add kalidocker-security "$SCRIPT_DIR/mcp/run_standalone.sh" 2>/dev/null || true
        echo "✅ MCP server added"
    fi
else
    echo "⚠️  Claude Code CLI not found. Install from: https://claude.ai/code"
fi

# Final status
echo ""
echo "=========================================="
echo "🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "Services running:"
docker compose -f "$SCRIPT_DIR/docker-compose.yml" ps --format "table {{.Name}}\t{{.Status}}"
echo ""
echo "To use with Claude Code CLI:"
echo "  claude"
echo "  > Use scan_network to scan example.com"
echo ""
echo "Quick commands:"
echo "  docker compose --profile msf up -d    # Start services"
echo "  docker compose down                    # Stop services"
echo "  claude mcp list                        # Verify MCP"
