#!/bin/bash
# ABOUTME: Smart commit script that runs pre-commit checks in container
# ABOUTME: but performs actual git operations on host for clean workflow

set -e

if [ -z "$1" ]; then
    echo "❌ Usage: $0 'commit message'"
    exit 1
fi

echo "🐳 Starting container for pre-commit checks..."
docker-compose --profile dev up -d

echo "🔍 Running pre-commit checks in container..."
if docker-compose exec dev poetry run pre-commit run --all-files; then
    echo "✅ Pre-commit checks passed!"
    echo "📝 Committing changes on host..."
    git add .
    git commit -m "$1"
    git push
    echo "🚀 Changes pushed successfully!"
else
    echo "❌ Pre-commit checks failed. Fix issues and try again."
    docker-compose down
    exit 1
fi

echo "🧹 Cleaning up container..."
docker-compose down
echo "✨ Done!"