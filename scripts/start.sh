#!/bin/bash
# KaliDocker - Start Script
# Usage: ./scripts/start.sh [profile]
#   Profiles: default, tools, msf, all

set -e

cd "$(dirname "$0")/.."

PROFILE=${1:-default}

echo "🐉 Starting KaliDocker..."

case $PROFILE in
  "all")
    echo "Starting all services including Kali tools..."
    docker compose --profile tools --profile msf up -d
    ;;
  "tools")
    echo "Starting with Kali base tools..."
    docker compose --profile tools up -d
    ;;
  "msf")
    echo "Starting with Metasploit..."
    docker compose --profile msf up -d
    ;;
  *)
    echo "Starting default services (UI, API, PostgreSQL)..."
    docker compose up -d
    ;;
esac

echo ""
echo "✅ KaliDocker is running!"
echo ""
echo "   UI:  http://localhost:${UI_PORT:-3443}"
echo "   API: http://localhost:${API_PORT:-8000}/docs"
echo ""
echo "To stop: docker compose down"
