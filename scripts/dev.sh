#!/bin/bash
# KaliDocker - Development Mode
# Starts services with hot-reload for UI and API development

set -e

cd "$(dirname "$0")/.."

echo "🐉 Starting KaliDocker in Development Mode..."

# Start database first
docker compose up -d postgres

# Wait for database
echo "Waiting for PostgreSQL..."
until docker compose exec -T postgres pg_isready -U kali > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL ready!"

# Start UI dev server
echo ""
echo "Starting UI development server..."
cd ui
npm install
npm run dev &
UI_PID=$!

# Start API dev server
echo "Starting API development server..."
cd ../api
pip install -r requirements.txt > /dev/null 2>&1
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

cd ..

echo ""
echo "✅ Development servers running!"
echo ""
echo "   UI:  http://localhost:3000"
echo "   API: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "kill $UI_PID $API_PID 2>/dev/null; docker compose down; exit" INT
wait
