# ABOUTME: Main FastHTML application entry point for BlogBot
# ABOUTME: Sets up the web server, routes, and database connections
# mypy: disable-error-code="name-defined,no-any-return"

import logging
import sys

from fasthtml.common import *  # type: ignore
from app.database import Database
from app.models import Settings

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("blogbot")

# Initialize database
db = Database()
logger.info("📊 Database initialized")

# Create the FastHTML app
app = FastHTML()

logger.info("🚀 BlogBot FastHTML application starting up...")


@app.get("/")
def home():  # type: ignore
    logger.info("🏠 Home page accessed")
    
    # Get current settings to show database integration
    settings = db.get_settings()
    status_text = "Phase 1 Development in Progress"
    
    if settings:
        status_text += f" - Blog: {settings.blog_title}"
    
    return Titled(
        "BlogBot",
        Div(
            H1("BlogBot"),
            P("A Python-based static site generator with FastHTML web interface"),
            P(status_text),
            A("Settings", href="/settings", style="margin: 10px; padding: 10px; background: #007acc; color: white; text-decoration: none; border-radius: 4px;"),
            style="text-align: center; margin-top: 50px;",
        ),
    )


@app.get("/health")
def health():  # type: ignore
    logger.info("❤️ Health check endpoint accessed")
    return {"status": "ok", "phase": "1"}


if __name__ == "__main__":
    serve()
