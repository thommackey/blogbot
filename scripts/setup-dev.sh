#!/bin/bash
# ABOUTME: One-time development environment setup script
# ABOUTME: Installs dependencies and configures the container for development

set -e

echo "🐳 Setting up BlogBot development environment..."

# Update package list and install dependencies
apt-get update -qq
apt-get install -y git curl

# Install Poetry
pip install poetry

# Install project dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

echo "✅ Development environment ready!"
echo "📖 Usage:"
echo "  poetry run python -m app.main    # Start FastHTML server"
echo "  poetry run pytest               # Run tests"
echo "  poetry run ruff check           # Linting"