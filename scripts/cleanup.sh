#!/bin/bash
# KaliDocker - Cleanup Script
# Removes stopped containers, unused volumes, and optionally rebuilds images

set -e

cd "$(dirname "$0")/.."

echo "🧹 KaliDocker Cleanup"
echo ""

# Stop all services
echo "Stopping services..."
docker compose down

# Remove orphan containers
echo "Removing orphan containers..."
docker container prune -f

# Optional: Remove volumes
if [[ "$1" == "--volumes" ]]; then
  echo "Removing volumes..."
  docker compose down -v
  docker volume prune -f
fi

# Optional: Rebuild images
if [[ "$1" == "--rebuild" ]]; then
  echo "Rebuilding images..."
  docker compose build --no-cache
fi

echo ""
echo "✅ Cleanup complete!"
