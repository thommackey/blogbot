# Blog Engine Specification

## Overview

A Python-based static site generator with a web interface that acts as a "markdown file enhancer and publisher". The system reads markdown files from GitHub repositories, provides a WYSIWYG editing interface, and publishes static sites to GitHub Pages.

**Key Philosophy**: API-first, single-user, agent-native, minimal complexity.

## Core Requirements

### Functional Requirements
- Read/write markdown files from GitHub repos via API
- WYSIWYG markdown editor with pause-based preview (2-3 second delay)
- Generate static HTML sites with minimal/no CSS
- One-click publish to GitHub Pages
- Support posts and pages (distinguished by frontmatter)
- RSS feed generation
- Image upload and embedding

### Non-Functional Requirements
- Stateless and idempotent API operations
- Detailed error messages with remediation steps
- No local file storage (work entirely through GitHub API)
- Container-based deployment
- Full test coverage with type hints

## Architecture

### Technology Stack
- **Framework**: FastHTML (leveraging HTMX for interactions)
- **Database**: SQLite (for app configuration only)
- **Authentication**: GitHub OAuth
- **API Authentication**: API keys
- **Deployment**: Docker → Render (app), GitHub Pages (static sites)

### High-Level Architecture
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

## Data Model

### SQLite Schema
```sql
-- User settings (single row)
CREATE TABLE settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    blog_title TEXT,
    blog_description TEXT,
    author_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API keys for agent access
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);

-- Deployment configuration
CREATE TABLE deployment_config (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    github_pages_repo TEXT,
    github_pages_branch TEXT DEFAULT 'gh-pages'
);
```

### Markdown File Structure
```yaml
---
title: My Post Title
date: 2025-06-12
tags: [python, web]
type: post  # or 'page'
slug: custom-url-slug  # optional
---

Post content here...
```

### URL Structure
- Posts: `/2025-06-12-my-post-title`
- Pages: `/about/`
- Homepage: `/` (list of all posts)
- RSS: `/feed.xml`

## API Specification

### Authentication
All endpoints require `Authorization: Bearer <api_key>` header except auth endpoints.

### Endpoints

#### Posts/Pages

**List all content**
```
GET /api/content
Response: {
    "items": [{
        "path": "posts/my-post.md",
        "title": "My Post",
        "date": "2025-06-12",
        "type": "post",
        "tags": ["python"]
    }]
}
```

**Get single item**
```
GET /api/content/{path}
Response: {
    "path": "posts/my-post.md",
    "content": "---\ntitle: My Post\n---\nContent...",
    "frontmatter": {...}
}
```

**Create/Update content**
```
POST /api/content
Body: {
    "path": "posts/new-post.md",  # optional, auto-generated if missing
    "content": "Post content",
    "frontmatter": {
        "title": "New Post",
        "date": "2025-06-12",  # optional, defaults to now
        "type": "post"  # optional, defaults to "post"
    }
}
Response: {
    "path": "posts/new-post.md",
    "url": "/2025-06-12-new-post"
}
```

**Delete content**
```
DELETE /api/content/{path}
Response: {"status": "deleted"}
```

#### Publishing

**Publish site**
```
POST /api/publish
Response: {
    "status": "success",
    "published_at": "2025-06-12T10:30:00Z",
    "url": "https://username.github.io"
}

Error Response: {
    "error": "Authentication failed",
    "detail": "GitHub token expired",
    "action": "Re-authenticate with GitHub at /auth/github"
}
```

#### Configuration

**Get/Update settings**
```
GET/PUT /api/settings
Body: {
    "blog_title": "My Blog",
    "blog_description": "...",
    "content_repo": "user/blog-content",
    "github_pages_repo": "user/user.github.io"
}
```

#### Images

**Upload image**
```
POST /api/images
Body: multipart/form-data with image file
Response: {
    "path": "images/2025/image.png",
    "markdown": "![](../images/2025/image.png)"
}
```

### API Response Format
All responses follow consistent structure:
```json
{
    "data": {...},  // On success
    "error": "...",  // On error
    "detail": "...",  // Error details
    "action": "..."  // Suggested remediation
}
```

## UI/UX Requirements

### Pages
1. **Dashboard** (`/`)
   - List of all posts/pages
   - Quick stats
   - Publish button

2. **Editor** (`/edit/{path}` or `/new`)
   - Split view: markdown editor (left), preview (right)
   - Frontmatter form (collapsible)
   - Save button (commits to GitHub)
   - Publish button

3. **Settings** (`/settings`)
   - Blog configuration
   - Repository settings
   - API key management

### Editor Features
- Syntax highlighting for markdown
- Pause-based preview (HTMX: `hx-trigger="keyup changed delay:2s"`)
- Drag-and-drop image upload
- Frontmatter editor with fields:
  - Title (text)
  - Date (date picker)
  - Tags (comma-separated)
  - Type (checkbox for page vs post)
  - Slug (optional)

## Deployment & Configuration

### Environment Variables
```bash
# Required (set in Render)
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
SECRET_KEY=...  # For session encryption

# Optional
PORT=8000
LOG_LEVEL=INFO
```

### Docker Configuration
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### First-Run Setup
1. User visits deployed app
2. Clicks "Login with GitHub"
3. Configures:
   - Blog title/description
   - Content repository
   - GitHub Pages repository
4. Generates first API key (optional)

## Development Standards

### Project Structure
```
blog-engine/
├── app/
│   ├── main.py          # FastHTML app
│   ├── api/             # API endpoints
│   ├── auth/            # GitHub OAuth
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   │   ├── github.py    # GitHub API client
│   │   ├── markdown.py  # Markdown processing
│   │   └── static_site.py # Site generation
│   └── templates/       # HTML templates
├── tests/
├── .pre-commit-config.yaml
├── pyproject.toml       # Project config
├── requirements.txt
└── Dockerfile
```

### Code Standards
- Type hints on all functions
- Docstrings for public APIs
- Tests for all endpoints and services
- Pre-commit hooks:
  - `ruff` (linting and formatting)
  - `mypy` (type checking)
  - `pytest` (test runner)

### Pre-commit Configuration
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.7
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Error Handling Strategy

### API Errors
- 400: Invalid request (missing required fields)
- 401: Invalid/missing API key
- 403: GitHub permissions issue
- 404: Resource not found
- 422: Validation error (invalid frontmatter)
- 500: Server error

### Error Response Examples
```python
# GitHub API failure
{
    "error": "GitHub API error",
    "detail": "Repository 'user/blog' not found",
    "action": "Check repository exists and you have access"
}

# Publishing failure
{
    "error": "Publishing failed",
    "detail": "GitHub Pages branch 'gh-pages' is protected",
    "action": "Remove branch protection or use different branch"
}
```

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Include request IDs for tracing
- Never log sensitive data (tokens, keys)

## Testing Strategy

### Test Categories
1. **Unit Tests**
   - Markdown processing
   - Frontmatter parsing
   - URL slug generation
   - Static site generation

2. **Integration Tests**
   - GitHub API interactions (mocked)
   - Database operations
   - File upload handling

3. **API Tests**
   - All endpoints with various inputs
   - Error scenarios
   - Authentication flows

4. **End-to-End Tests**
   - Complete publish flow
   - Editor preview functionality

### Example Test
```python
def test_create_post_without_date():
    """Posts without dates should use current date."""
    response = client.post("/api/content", json={
        "content": "Test content",
        "frontmatter": {"title": "Test Post"}
    })
    assert response.status_code == 200
    assert response.json()["path"].startswith(f"posts/{date.today()}")
```

## Implementation Phases

### Phase 1: Core (MVP)
- GitHub OAuth login
- Read/write markdown files via GitHub API
- Basic editor with preview
- Minimal static site generation
- Publish to GitHub Pages
- API for create/read posts

### Phase 2: Enhancement
- Image upload support
- API keys and full API
- Settings UI
- Delete/update posts
- RSS feed generation

### Phase 3: Polish
- Syntax highlighting in editor
- Better error handling
- Performance optimisation
- API documentation
- Deployment button/guide

## Success Criteria
- Can authenticate with GitHub
- Can create/edit markdown posts with frontmatter
- Can publish to GitHub Pages with one click
- APIs are idempotent and return helpful errors
- All code has type hints and tests
- Pre-commit hooks prevent bad commits
- Can be deployed to Render with minimal configuration