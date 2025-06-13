# TODO.md - FastHTML Simplified Approach

## Phase 1: Core MVP

### Setup & Configuration (Container-First)
- [ ] Create development Docker setup with volume mounting
- [ ] Initialize project structure with FastHTML patterns inside container
- [ ] Set up Poetry dependencies (FastHTML, FastLite, etc.) in container
- [ ] Configure pre-commit hooks (ruff, mypy, pytest) in container
- [ ] Create docker-compose.yml for persistent development
- [ ] Set up environment variable configuration

### Data & Models
- [ ] Create Python dataclasses for Settings, API Keys, Deployment Config
- [ ] Set up SQLite database with FastLite integration
- [ ] Implement simple CRUD operations for configuration data
- [ ] Add database initialization and setup

### Authentication & Security
- [ ] Implement GitHub OAuth flow with FastHTML
- [ ] Create API key management with hashing
- [ ] Set up session management using FastHTML sessions
- [ ] Implement security middleware

### Core Services
- [ ] Build GitHub API client with retry/rate limiting
- [ ] Implement markdown processing with frontmatter parsing
- [ ] Create static site generation service
- [ ] Build content management logic

### Web Interface (FastHTML/HTMX)
- [ ] Create FastHTML app entry point with database
- [ ] Build WYSIWYG editor interface using FT components
- [ ] Implement content listing/management UI
- [ ] Create settings configuration UI
- [ ] Add HTMX interactions for dynamic updates

### API Endpoints
- [ ] Implement `/api/content` endpoints (CRUD)
- [ ] Create `/api/publish` endpoint
- [ ] Build authentication endpoints
- [ ] Add consistent error handling

### Publishing System
- [ ] Implement GitHub Pages deployment
- [ ] Create static site build process
- [ ] Add branch protection handling
- [ ] Test complete publish workflow

## Phase 2: Enhancement

### Content Features
- [ ] Add image upload and management
- [ ] Implement comprehensive API coverage
- [ ] Create advanced settings UI
- [ ] Build RSS feed generation

### Performance & UX
- [ ] Add HTMX optimizations
- [ ] Implement caching strategies
- [ ] Add progress indicators
- [ ] Create keyboard shortcuts

## Phase 3: Polish

### Developer Experience
- [ ] Add syntax highlighting in editor
- [ ] Implement performance monitoring
- [ ] Create comprehensive documentation
- [ ] Add logging and debugging tools

### User Experience
- [ ] Improve editor interface
- [ ] Add draft/preview modes
- [ ] Implement backup/restore functionality
- [ ] Create mobile-responsive design

## Testing Strategy (TDD Approach)

### Unit Tests
- [ ] Test markdown processing functions
- [ ] Test frontmatter parsing
- [ ] Test URL generation logic
- [ ] Test dataclass operations
- [ ] Test utility functions

### Integration Tests
- [ ] Test GitHub API interactions (real API with test repos)
- [ ] Test FastLite database operations
- [ ] Test service layer integration
- [ ] Test authentication flows

### API Tests
- [ ] Test all API endpoints with various inputs
- [ ] Test error scenarios and edge cases
- [ ] Test authentication/authorization
- [ ] Test input validation and sanitization

### End-to-End Tests
- [ ] Set up Playwright testing framework
- [ ] Test complete publish workflow
- [ ] Test user authentication flow
- [ ] Test content management workflow
- [ ] Test HTMX interactions

## Container Development Workflow

### Docker Compose Setup
```bash
# Start development environment
docker-compose --profile dev up -d

# Enter container shell
docker-compose exec dev bash

# One-time setup (inside container)
./scripts/setup-dev.sh

# Development workflow:
# Edit files: Use normal tools on HOST
# Run commands: Execute in CONTAINER
poetry run python -m app.main    # Start FastHTML server
poetry run pytest               # Run tests
poetry run ruff check           # Linting

# Alternative: Run app with compose
docker-compose --profile app up

# Clean shutdown
docker-compose down
```

### Benefits for Agent Development
- **Simple commands**: No complex docker run chains
- **Persistent containers**: Named containers in Docker Desktop
- **Easy setup**: Automated dependency installation script
- **Clean workflow**: compose up → exec → work → compose down
- **Immediate changes**: Volume mounting for file editing

## FastHTML-Specific Implementation Notes

### Database Pattern
- Use FastHTML's database-first argument pattern
- SQLite with FastLite for simple operations
- No migrations needed - just schema creation

### Component Structure
- FT components instead of Jinja2 templates
- HTMX for dynamic interactions
- Server-side rendering with minimal JavaScript

### Development Workflow
```bash
# Start with database reference
app = FastHTML(db='blog.db')

# Use dataclasses for form parsing
@dataclass
class BlogPost:
    title: str
    content: str
    tags: list[str]
```

## Current Status
- Architecture simplified for FastHTML patterns
- Container-first development workflow established
- Ready to begin Phase 1 implementation in isolated environment