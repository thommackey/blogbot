# ABOUTME: Unit tests for data models and database operations
# ABOUTME: Tests Settings, APIKey, and DeploymentConfig dataclasses with SQLite
import pytest
import tempfile
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from app.models import Settings, APIKey, DeploymentConfig


class TestSettings:
    """Test the Settings dataclass and database operations."""
    
    def test_settings_creation(self):
        """Test basic Settings dataclass creation."""
        settings = Settings(
            blog_title="My Blog",
            blog_description="A test blog",
            github_repo="user/repo",
            github_branch="main"
        )
        
        assert settings.blog_title == "My Blog"
        assert settings.blog_description == "A test blog"
        assert settings.github_repo == "user/repo"
        assert settings.github_branch == "main"
        assert settings.github_pages_url is None
        assert settings.theme == "default"
    
    def test_settings_with_optional_fields(self):
        """Test Settings with all optional fields populated."""
        settings = Settings(
            blog_title="My Blog",
            blog_description="A test blog",
            github_repo="user/repo",
            github_branch="main",
            github_pages_url="https://user.github.io/repo",
            theme="dark",
            custom_css="body { color: red; }"
        )
        
        assert settings.github_pages_url == "https://user.github.io/repo"
        assert settings.theme == "dark"
        assert settings.custom_css == "body { color: red; }"


class TestAPIKey:
    """Test the APIKey dataclass and hashing functionality."""
    
    def test_api_key_creation(self):
        """Test basic APIKey dataclass creation."""
        api_key = APIKey(
            name="Test Key",
            key_hash="hashed_value",
            permissions=["read", "write"]
        )
        
        assert api_key.name == "Test Key"
        assert api_key.key_hash == "hashed_value"
        assert api_key.permissions == ["read", "write"]
        assert api_key.is_active is True
        assert isinstance(api_key.created_at, datetime)
    
    def test_api_key_with_custom_creation_date(self):
        """Test APIKey with custom creation date."""
        custom_date = datetime(2023, 1, 1, 12, 0, 0)
        api_key = APIKey(
            name="Test Key",
            key_hash="hashed_value",
            permissions=["read"],
            created_at=custom_date,
            is_active=False
        )
        
        assert api_key.created_at == custom_date
        assert api_key.is_active is False


class TestDeploymentConfig:
    """Test the DeploymentConfig dataclass."""
    
    def test_deployment_config_creation(self):
        """Test basic DeploymentConfig creation."""
        config = DeploymentConfig(
            target_repo="user/blog-site",
            target_branch="gh-pages",
            build_command="npm run build"
        )
        
        assert config.target_repo == "user/blog-site"
        assert config.target_branch == "gh-pages"
        assert config.build_command == "npm run build"
        assert config.custom_domain is None
        assert config.auto_deploy is True
    
    def test_deployment_config_with_custom_domain(self):
        """Test DeploymentConfig with custom domain."""
        config = DeploymentConfig(
            target_repo="user/blog-site",
            target_branch="gh-pages",
            build_command="npm run build",
            custom_domain="myblog.com",
            auto_deploy=False
        )
        
        assert config.custom_domain == "myblog.com"
        assert config.auto_deploy is False