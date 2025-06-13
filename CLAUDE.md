# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based static site generator with a web interface - a "markdown file enhancer and publisher" that reads markdown files from GitHub repositories, provides a WYSIWYG editing interface, and publishes static sites to GitHub Pages.

**Key Philosophy**: API-first, single-user, agent-native, minimal complexity.

## Technology Stack

- **Framework**: FastHTML (leveraging HTMX for interactions)
- **Database**: SQLite with FastLite (for app configuration only)
- **Authentication**: GitHub OAuth
- **API Authentication**: API keys
- **Development**: Docker Compose with volume mounting for clean workflow
- **Deployment**: Docker → Render (app), GitHub Pages (static sites)

## Architecture

The system operates as a bridge between content repositories and published sites:
- Content Repo (Markdown) ↔ Blog Engine (FastHTML) → GitHub Pages (Static HTML)
- SQLite stores only app settings, not content
- All content operations go through GitHub API (stateless)

## Development Commands

This project uses **Docker Compose** for clean, simple containerized development:

```bash
# Start development container
docker-compose --profile dev up -d

# Enter development environment
docker-compose exec dev bash

# One-time setup (inside container)
./scripts/setup-dev.sh

# Development workflow:
# - Edit files on HOST (using normal tools)
# - Run commands in CONTAINER (for isolation)
poetry run python -m app.main  # Start FastHTML server
poetry run pytest             # Run tests
poetry run ruff check         # Linting
poetry run ruff format        # Code formatting
poetry run mypy app/          # Type checking

# Alternative: Run app directly with compose
docker-compose --profile app up

# Stop containers
docker-compose down

# Git operations with pre-commit checks
./scripts/commit.sh "commit message"  # Runs pre-commit in container, commits on host

# Or manual workflow:
docker-compose --profile dev up -d
docker-compose exec dev poetry run pre-commit run --all-files
git add . && git commit -m "message" && git push
docker-compose down

# Database operations (SQLite with FastLite)
# No migrations needed - direct SQLite operations

# Static site generation
poetry run python -m app.services.static_site build
```

## Project Structure (Planned)

```
blog-engine/
├── app/
│   ├── main.py          # FastHTML app entry point
│   ├── api/             # API endpoints (/api/content, /api/publish, etc.)
│   ├── auth/            # GitHub OAuth flow
│   ├── models/          # Python dataclasses for data structures
│   ├── services/        # Business logic
│   │   ├── github.py    # GitHub API client with retry/rate limiting
│   │   ├── markdown.py  # Markdown processing & frontmatter parsing
│   │   └── static_site.py # Static site generation
│   └── templates/       # FastHTML FT components (no Jinja2)
├── tests/              # Test files organized by module
├── .pre-commit-config.yaml # ruff, mypy, pytest hooks
├── pyproject.toml      # Poetry dependencies & project config
└── Dockerfile         # Container deployment
```

## Key Implementation Details

### Data Models
- **Settings**: Simple dataclass for blog configuration (single SQLite table)
- **API Keys**: Dataclass with hashed keys for agent access
- **Deployment Config**: Dataclass for GitHub Pages repository settings
- All models use Python dataclasses, no ORM required

### Content Structure
- Posts and pages distinguished by frontmatter `type` field
- All content stored as markdown files in GitHub repository
- Frontmatter includes: title, date, tags, type, slug

### API Design
- RESTful endpoints under `/api/`
- Consistent error responses with `error`, `detail`, and `action` fields
- Bearer token authentication for API access
- All operations are stateless and idempotent

### Security Requirements
- GitHub OAuth for user authentication
- API keys stored as hashes in database
- Never log sensitive data (tokens, keys)
- All secrets via environment variables

## Testing Strategy

The project requires comprehensive testing:
- **Unit tests**: Markdown processing, frontmatter parsing, URL generation
- **Integration tests**: GitHub API interactions (real API with test repos), database operations
- **API tests**: All endpoints with various inputs and error scenarios
- **E2E tests**: Complete publish flow using Playwright

## Error Handling

All errors should include helpful remediation steps:
- GitHub API failures → check repository access
- Publishing failures → check branch protection settings
- Authentication failures → re-authenticate with GitHub

## Development Phases

The project is designed to be built incrementally:
1. **Phase 1**: Core MVP (OAuth, basic editor, GitHub API, publishing)
2. **Phase 2**: Enhancement (images, full API, settings UI, RSS)
3. **Phase 3**: Polish (syntax highlighting, performance, documentation)

## Environment Variables

Required for deployment:
- `GITHUB_CLIENT_ID` - GitHub OAuth app client ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth app secret
- `SECRET_KEY` - Session encryption key
- `PORT` (optional, default: 8000)
- `LOG_LEVEL` (optional, default: INFO)

## Containerized Development

**Philosophy**: Docker Compose provides the cleanest containerized development experience:
- **Simple commands**: `docker-compose up` and `docker-compose exec dev bash`
- **No complex command chains**: Everything is in docker-compose.yml
- **Persistent containers**: Named containers that survive restarts
- **Clean teardown**: `docker-compose down` removes everything

**Docker Compose Workflow**:
1. `docker-compose --profile dev up -d` - Start development container
2. `docker-compose exec dev bash` - Enter container shell
3. `./scripts/setup-dev.sh` - One-time dependency installation
4. Edit files on host, run commands in container
5. `docker-compose down` - Clean shutdown

**Container Profiles**:
- `dev`: Development container with persistent shell
- `app`: Runs FastHTML app directly (for testing)

**Benefits for AI agents**:
- **Zero complex commands**: Simple, memorable docker-compose commands
- **Reproducible setup**: Same environment every time
- **Easy debugging**: Named containers visible in Docker Desktop
- **Fast iteration**: Volume mounting for immediate file changes
- **Clean isolation**: All dependencies contained, easy cleanup

**Setup Script**: `scripts/setup-dev.sh` handles all dependency installation automatically

## Writing code

- CRITICAL: NEVER USE --no-verify WHEN COMMITTING CODE
- We prefer simple, clean, maintainable solutions over clever or complex ones, even if the latter are more concise or performant. Readability and maintainability are primary concerns.
- Make the smallest reasonable changes to get to the desired outcome. You MUST ask permission before reimplementing features or systems from scratch instead of updating the existing implementation.
- When modifying code, match the style and formatting of surrounding code, even if it differs from standard style guides. Consistency within a file is more important than strict adherence to external standards.
- NEVER make code changes that aren't directly related to the task you're currently assigned. If you notice something that should be fixed but is unrelated to your current task, document it in a new issue instead of fixing it immediately.
- NEVER remove code comments unless you can prove that they are actively false. Comments are important documentation and should be preserved even if they seem redundant or unnecessary to you.
- All code files should start with a brief 2 line comment explaining what the file does. Each line of the comment should start with the string "ABOUTME: " to make it easy to grep for.
- When writing comments, avoid referring to temporal context about refactors or recent changes. Comments should be evergreen and describe the code as it is, not how it evolved or was recently changed.
- NEVER implement a mock mode for testing or for any purpose. We always use real data and real APIs, never mock implementations.
- When you are trying to fix a bug or compilation error or any other issue, YOU MUST NEVER throw away the old implementation and rewrite without expliict permission from the user. If you are going to do this, YOU MUST STOP and get explicit permission from the user.
- NEVER name things as 'improved' or 'new' or 'enhanced', etc. Code naming should be evergreen. What is new today will be "old" someday.

## Version Control

- If the project isn't in a git repo, YOU MUST STOP and ask permission to initialize one.
- YOU MUST STOP and ask how to handle uncommitted changes or untracked files when starting work.  Suggest committing existing work first.
- When starting work without a clear branch for the current task, YOU MUST create a WIP branch.
- YOU MUST TRACK All non-trivial changes in git.
- YOU MUST commit frequently throughout the development process, even if your high-level tasks are not yet done.

## Getting help

- ALWAYS ask for clarification rather than making assumptions.
- If you're having trouble with something, it's ok to stop and ask for help. Especially if it's something your human might be better at.

## Testing

- Tests MUST cover the functionality being implemented.
- NEVER ignore the output of the system or the tests - Logs and messages often contain CRITICAL information.
- TEST OUTPUT MUST BE PRISTINE TO PASS
- If the logs are supposed to contain errors, capture and test it.
- NO EXCEPTIONS POLICY: Under no circumstances should you mark any test type as "not applicable". Every project, regardless of size or complexity, MUST have unit tests, integration tests, AND end-to-end tests. If you believe a test type doesn't apply, you need the human to say exactly "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME"

### We practice TDD. That means:

- Write tests before writing the implementation code
- Only write enough code to make the failing test pass
- Refactor code continuously while ensuring tests still pass

#### TDD Implementation Process

- Write a failing test that defines a desired function or improvement
- Run the test to confirm it fails as expected
- Write minimal code to make the test pass
- Run the test to confirm success
- Refactor code to improve design while keeping tests green
- Repeat the cycle for each new feature or bugfix