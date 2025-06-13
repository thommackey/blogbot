#!/bin/bash
# ABOUTME: Smart commit script that runs pre-commit checks in container
# ABOUTME: but performs actual git operations on host for clean workflow

set -e

# Logging function that sends to Docker container logs
log() {
    local message="$(date '+%Y-%m-%d %H:%M:%S') [COMMIT] $1"
    echo "$message"
    # Also send to container logs if container is running
    docker-compose exec -T dev echo "$message" 2>/dev/null || true
}

if [ -z "$1" ]; then
    echo "❌ Usage: $0 'commit message'"
    exit 1
fi

log "🐳 Starting container for pre-commit checks..."
docker-compose --profile dev up -d

log "🔍 Running pre-commit checks in container..."
if docker-compose exec dev sh -c "echo '$(date '+%Y-%m-%d %H:%M:%S') [PRE-COMMIT] Starting pre-commit checks...' && poetry run pre-commit run --all-files"; then
    log "✅ Pre-commit checks passed!"
    log "📝 Committing changes on host..."
    git add .
    git commit -m "$1"
    git push
    log "🚀 Changes pushed successfully!"
else
    log "❌ Pre-commit checks failed. Fix issues and try again."
    docker-compose down
    exit 1
fi

log "🧹 Cleaning up container..."
docker-compose down
log "✨ Done!"