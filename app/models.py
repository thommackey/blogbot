# ABOUTME: Data models for BlogBot configuration and API key management
# ABOUTME: Python dataclasses for Settings, APIKey, and DeploymentConfig with SQLite integration
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Settings:
    """Blog configuration settings stored in SQLite."""
    blog_title: str
    blog_description: str
    github_repo: str  # Format: "user/repo"
    github_branch: str = "main"
    github_pages_url: Optional[str] = None
    theme: str = "default"
    custom_css: Optional[str] = None


@dataclass
class APIKey:
    """API key for programmatic access to BlogBot."""
    name: str
    key_hash: str  # Hashed version of the actual key
    permissions: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


@dataclass  
class DeploymentConfig:
    """GitHub Pages deployment configuration."""
    target_repo: str  # Where to deploy the static site
    target_branch: str = "gh-pages"
    build_command: str = "npm run build"
    custom_domain: Optional[str] = None
    auto_deploy: bool = True