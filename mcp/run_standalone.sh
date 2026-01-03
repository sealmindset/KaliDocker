#!/bin/bash
# KaliDocker MCP Server - Standalone Runner
# Run this directly on Mac to use MCP with Claude Desktop

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if docker compose stack is running
if ! docker compose -f "$PROJECT_DIR/docker-compose.yml" ps --services --filter "status=running" | grep -q "kali-msf"; then
    echo "⚠️  Kali container not running. Starting it..."
    docker compose -f "$PROJECT_DIR/docker-compose.yml" --profile msf up -d
    sleep 5
fi

# Set environment
export KALIDOCKER_COMPOSE_PATH="$PROJECT_DIR"
export USE_DOCKER=true

# Check for Python venv
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
    source "$SCRIPT_DIR/.venv/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Run MCP server
echo "🚀 Starting KaliDocker MCP Server..."
cd "$SCRIPT_DIR"
python server.py
