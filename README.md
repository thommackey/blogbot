# BlogBot

A Python-based static site generator with a web interface - a "markdown file enhancer and publisher" that reads markdown files from GitHub repositories, provides a WYSIWYG editing interface, and publishes static sites to GitHub Pages.

## Key Philosophy
- **API-first**: Every UI action calls documented endpoints
- **Single-user**: Designed for individual content creators
- **Agent-native**: Built to work seamlessly with AI development tools
- **Minimal complexity**: Simple, maintainable FastHTML architecture

## Technology Stack
- **Framework**: FastHTML (leveraging HTMX for interactions)
- **Database**: SQLite with FastLite (for app configuration only)
- **Authentication**: GitHub OAuth
- **Deployment**: Docker → Render (app), GitHub Pages (static sites)

## Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Content Repo   │────▶│   Blog Engine   │────▶│ GitHub Pages    │
│  (Markdown)     │◀────│   (FastHTML)    │     │  (Static HTML)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │     SQLite      │
                        │   (Settings)    │
                        └─────────────────┘
```

## Development

This project uses containerized development for complete isolation:

```bash
# Start development container
docker run -it --rm \
  -v $(pwd):/app \
  -p 8000:8000 \
  -w /app \
  python:3.12-slim bash

# Inside container
pip install poetry
poetry install
poetry run python -m app.main
```

For true isolation (AI agent development), work entirely inside containers:

```bash
# Clone and work in ephemeral container
docker run -it --rm -p 8000:8000 python:3.12-slim bash
git clone https://github.com/thommackey/blogbot.git
cd blogbot
# ... development work, commit & push frequently
```

## Status
- 📋 Project planning and architecture complete
- 🐳 Containerized development workflow established
- 🚧 Phase 1 implementation in progress

## Documentation
- `CLAUDE.md` - Development guidelines and containerized workflow
- `TODO.md` - Implementation phases and development tasks
- `spec.md` - Complete project specification