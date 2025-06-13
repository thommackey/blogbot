# ABOUTME: Integration tests for database operations with SQLite and FastLite
# ABOUTME: Tests database setup, CRUD operations, and data persistence
import pytest
import tempfile
import os
from datetime import datetime

from app.database import Database
from app.models import Settings, APIKey, DeploymentConfig


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    db = Database(path)
    yield db
    os.unlink(path)


class TestDatabaseSetup:
    """Test database initialization and schema creation."""
    
    def test_database_creation(self, temp_db):
        """Test that database and tables are created correctly."""
        # Database should be initialized
        assert temp_db.db_path.endswith('.db')
        
        # Tables should exist (this will be tested once we implement the schema)
        # For now, just verify the database object exists
        assert temp_db is not None


class TestSettingsOperations:
    """Test CRUD operations for Settings."""
    
    def test_create_settings(self, temp_db):
        """Test creating and retrieving settings."""
        settings = Settings(
            blog_title="Test Blog",
            blog_description="A test blog for testing",
            github_repo="user/test-repo",
            github_branch="main"
        )
        
        # Save settings
        temp_db.save_settings(settings)
        
        # Retrieve settings
        retrieved = temp_db.get_settings()
        
        assert retrieved.blog_title == "Test Blog"
        assert retrieved.blog_description == "A test blog for testing"
        assert retrieved.github_repo == "user/test-repo"
        assert retrieved.github_branch == "main"
    
    def test_update_settings(self, temp_db):
        """Test updating existing settings."""
        # Create initial settings
        settings = Settings(
            blog_title="Original Title",
            blog_description="Original description",
            github_repo="user/repo",
            github_branch="main"
        )
        temp_db.save_settings(settings)
        
        # Update settings
        updated_settings = Settings(
            blog_title="Updated Title",
            blog_description="Updated description",  
            github_repo="user/repo",
            github_branch="develop",
            theme="dark"
        )
        temp_db.save_settings(updated_settings)
        
        # Verify update
        retrieved = temp_db.get_settings()
        assert retrieved.blog_title == "Updated Title"
        assert retrieved.blog_description == "Updated description"
        assert retrieved.github_branch == "develop"
        assert retrieved.theme == "dark"
    
    def test_get_settings_when_none_exist(self, temp_db):
        """Test getting settings when none have been created."""
        settings = temp_db.get_settings()
        assert settings is None


class TestAPIKeyOperations:
    """Test CRUD operations for API keys."""
    
    def test_create_api_key(self, temp_db):
        """Test creating and retrieving an API key."""
        api_key = APIKey(
            name="Test API Key",
            key_hash="hashed_secret_key",
            permissions=["read", "write"]
        )
        
        # Save API key
        key_id = temp_db.create_api_key(api_key)
        assert key_id is not None
        
        # Retrieve API key
        retrieved = temp_db.get_api_key(key_id)
        
        assert retrieved.name == "Test API Key"
        assert retrieved.key_hash == "hashed_secret_key"
        assert retrieved.permissions == ["read", "write"]
        assert retrieved.is_active is True
    
    def test_list_api_keys(self, temp_db):
        """Test listing all API keys."""
        # Create multiple API keys
        key1 = APIKey(name="Key 1", key_hash="hash1", permissions=["read"])
        key2 = APIKey(name="Key 2", key_hash="hash2", permissions=["write"])
        
        id1 = temp_db.create_api_key(key1)
        id2 = temp_db.create_api_key(key2)
        
        # List all keys
        keys = temp_db.list_api_keys()
        
        assert len(keys) == 2
        key_names = [key.name for key in keys]
        assert "Key 1" in key_names
        assert "Key 2" in key_names
    
    def test_deactivate_api_key(self, temp_db):
        """Test deactivating an API key."""
        api_key = APIKey(
            name="Test Key",
            key_hash="hash",
            permissions=["read"]
        )
        
        key_id = temp_db.create_api_key(api_key)
        
        # Deactivate the key
        temp_db.deactivate_api_key(key_id)
        
        # Verify it's deactivated
        retrieved = temp_db.get_api_key(key_id)
        assert retrieved.is_active is False


class TestDeploymentConfigOperations:
    """Test CRUD operations for deployment configuration."""
    
    def test_create_deployment_config(self, temp_db):
        """Test creating and retrieving deployment config."""
        config = DeploymentConfig(
            target_repo="user/blog-site",
            target_branch="gh-pages",
            build_command="npm run build",
            custom_domain="myblog.com"
        )
        
        # Save config
        temp_db.save_deployment_config(config)
        
        # Retrieve config
        retrieved = temp_db.get_deployment_config()
        
        assert retrieved.target_repo == "user/blog-site"
        assert retrieved.target_branch == "gh-pages"
        assert retrieved.build_command == "npm run build"
        assert retrieved.custom_domain == "myblog.com"
    
    def test_update_deployment_config(self, temp_db):
        """Test updating deployment configuration."""
        # Create initial config
        config = DeploymentConfig(
            target_repo="user/old-repo",
            target_branch="master"
        )
        temp_db.save_deployment_config(config)
        
        # Update config
        updated_config = DeploymentConfig(
            target_repo="user/new-repo",
            target_branch="gh-pages",
            custom_domain="newdomain.com",
            auto_deploy=False
        )
        temp_db.save_deployment_config(updated_config)
        
        # Verify update
        retrieved = temp_db.get_deployment_config()
        assert retrieved.target_repo == "user/new-repo"
        assert retrieved.target_branch == "gh-pages"
        assert retrieved.custom_domain == "newdomain.com"
        assert retrieved.auto_deploy is False