#!/usr/bin/env bash

set -Eeuo pipefail

docker-compose up -d --build
TRIVAGO_CLI="$(docker ps -aqf name=trivago-cli)"
echo "Container started..."
echo "Attaching to container..."
docker exec -it $TRIVAGO_CLI bash