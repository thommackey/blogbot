#!/bin/bash
# ABOUTME: Resume BlogBot development session from previous handoff
# ABOUTME: Shows current status, starts containers, and displays next steps

set -e

echo "🚀 BlogBot Development Session Resume"
echo "====================================="
echo

# Check current status
echo "📍 Current Status:"
echo "  Directory: $(pwd)"
echo "  Git Branch: $(git branch --show-current)"
echo "  Git Status: $(git status --porcelain | wc -l | xargs) uncommitted changes"
echo

# Start development environment
echo "🐳 Starting Development Environment..."
docker-compose --profile dev up -d

# Wait for setup to complete
echo "⏳ Waiting for container setup..."
sleep 10

# Show container status
echo "📊 Container Status:"
docker-compose ps

echo
echo "🧪 Running Quick Health Check..."
docker-compose exec dev poetry run python -c "
import sys
sys.path.append('/app')
from app.database import Database
from app.models import Settings

db = Database()
print('✅ Database connection: OK')

# Test importing FastHTML
try:
    from fasthtml.common import *
    print('✅ FastHTML import: OK')
except ImportError as e:
    print(f'❌ FastHTML import failed: {e}')

print('✅ Environment ready!')
"

echo
echo "📋 Next Steps (from SESSION.md):"
echo "  1. Implement GitHub API client (app/services/github.py)"
echo "  2. Write tests first (tests/test_github.py) - TDD approach"
echo "  3. Features: repo content, file operations, rate limiting"
echo "  4. Create PR when complete for review"
echo
echo "💻 Development Commands:"
echo "  docker-compose exec dev bash              # Enter container"
echo "  docker-compose exec dev poetry run pytest # Run tests"
echo "  ./scripts/commit.sh 'message'             # Commit with checks"
echo "  docker-compose down                       # Clean shutdown"
echo
echo "📖 Full context available in SESSION.md"
echo "🎯 Current branch: $(git branch --show-current)"
echo "✅ Ready to continue development!"