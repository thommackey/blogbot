#!/bin/bash
# ABOUTME: One-time development environment setup script
# ABOUTME: Installs dependencies and configures the container for development

set -e

# Logging function with timestamps - force stdout and flush
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [SETUP] $1" | tee /proc/1/fd/1
}

log "🐳 Setting up BlogBot development environment..."

# Update package list and install dependencies
log "📦 Installing system dependencies..."
apt-get update -qq
apt-get install -y git curl

# Install Poetry
log "📝 Installing Poetry..."
pip install poetry

# Install project dependencies
log "🔧 Installing Python dependencies..."
poetry install

# Note: Don't install pre-commit hooks here since we handle them manually
log "✅ Development environment ready!"
log "📖 Usage:"
log "  poetry run python -m app.main    # Start FastHTML server"
log "  poetry run pytest               # Run tests"
log "  poetry run ruff check           # Linting"