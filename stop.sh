#!/bin/bash
echo "Stopping Real-Time Analytics System..."
if docker compose version > /dev/null 2>&1; then
    docker compose down
else
    docker-compose down
fi
echo "Services stopped."
