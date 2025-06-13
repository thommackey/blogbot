# ABOUTME: Database operations layer using SQLite with FastLite integration
# ABOUTME: Handles CRUD operations for Settings, APIKey, and DeploymentConfig models
import sqlite3
import json
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from app.models import Settings, APIKey, DeploymentConfig


class Database:
    """SQLite database operations for BlogBot configuration data."""
    
    def __init__(self, db_path: str = "blog.db"):
        """Initialize database connection and create schema."""
        self.db_path = db_path
        self.init_schema()
    
    def init_schema(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    blog_title TEXT NOT NULL,
                    blog_description TEXT NOT NULL,
                    github_repo TEXT NOT NULL,
                    github_branch TEXT NOT NULL DEFAULT 'main',
                    github_pages_url TEXT,
                    theme TEXT DEFAULT 'default',
                    custom_css TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    key_hash TEXT NOT NULL UNIQUE,
                    permissions TEXT NOT NULL,  -- JSON array
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS deployment_config (
                    id INTEGER PRIMARY KEY,
                    target_repo TEXT NOT NULL,
                    target_branch TEXT NOT NULL DEFAULT 'gh-pages',
                    build_command TEXT NOT NULL DEFAULT 'npm run build',
                    custom_domain TEXT,
                    auto_deploy BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    # Settings operations
    def save_settings(self, settings: Settings) -> None:
        """Save or update blog settings (single row table)."""
        with sqlite3.connect(self.db_path) as conn:
            # Delete existing settings (single row table pattern)
            conn.execute("DELETE FROM settings")
            
            # Insert new settings
            conn.execute("""
                INSERT INTO settings (
                    blog_title, blog_description, github_repo, github_branch,
                    github_pages_url, theme, custom_css
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                settings.blog_title,
                settings.blog_description,
                settings.github_repo,
                settings.github_branch,
                settings.github_pages_url,
                settings.theme,
                settings.custom_css
            ))
    
    def get_settings(self) -> Optional[Settings]:
        """Retrieve blog settings."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM settings LIMIT 1")
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return Settings(
                blog_title=row['blog_title'],
                blog_description=row['blog_description'],
                github_repo=row['github_repo'],
                github_branch=row['github_branch'],
                github_pages_url=row['github_pages_url'],
                theme=row['theme'],
                custom_css=row['custom_css']
            )
    
    # API Key operations
    def create_api_key(self, api_key: APIKey) -> int:
        """Create a new API key and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO api_keys (name, key_hash, permissions, is_active, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                api_key.name,
                api_key.key_hash,
                json.dumps(api_key.permissions),
                api_key.is_active,
                api_key.created_at.isoformat()
            ))
            return cursor.lastrowid
    
    def get_api_key(self, key_id: int) -> Optional[APIKey]:
        """Retrieve an API key by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM api_keys WHERE id = ?", (key_id,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return APIKey(
                name=row['name'],
                key_hash=row['key_hash'],
                permissions=json.loads(row['permissions']),
                is_active=bool(row['is_active']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
    
    def list_api_keys(self) -> List[APIKey]:
        """List all API keys."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM api_keys ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            return [
                APIKey(
                    name=row['name'],
                    key_hash=row['key_hash'],
                    permissions=json.loads(row['permissions']),
                    is_active=bool(row['is_active']),
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                for row in rows
            ]
    
    def deactivate_api_key(self, key_id: int) -> None:
        """Deactivate an API key."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE api_keys SET is_active = 0 WHERE id = ?",
                (key_id,)
            )
    
    # Deployment Config operations
    def save_deployment_config(self, config: DeploymentConfig) -> None:
        """Save or update deployment configuration (single row table)."""
        with sqlite3.connect(self.db_path) as conn:
            # Delete existing config (single row table pattern)
            conn.execute("DELETE FROM deployment_config")
            
            # Insert new config
            conn.execute("""
                INSERT INTO deployment_config (
                    target_repo, target_branch, build_command, custom_domain, auto_deploy
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                config.target_repo,
                config.target_branch,
                config.build_command,
                config.custom_domain,
                config.auto_deploy
            ))
    
    def get_deployment_config(self) -> Optional[DeploymentConfig]:
        """Retrieve deployment configuration."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM deployment_config LIMIT 1")
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            return DeploymentConfig(
                target_repo=row['target_repo'],
                target_branch=row['target_branch'],
                build_command=row['build_command'],
                custom_domain=row['custom_domain'],
                auto_deploy=bool(row['auto_deploy'])
            )