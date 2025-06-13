# ABOUTME: Main FastHTML application entry point for BlogBot
# ABOUTME: Sets up the web server, routes, and database connections
# mypy: disable-error-code="name-defined,no-any-return"

import logging
import sys

from fasthtml.common import *  # type: ignore

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("blogbot")

# Create the FastHTML app
app = FastHTML()

logger.info("🚀 BlogBot FastHTML application starting up...")


@app.get("/")
def home():  # type: ignore
    logger.info("🏠 Home page accessed")
    return Titled(
        "BlogBot",
        Div(
            H1("BlogBot"),
            P("A Python-based static site generator with FastHTML web interface"),
            P("Status: Phase 1 Development in Progress"),
            style="text-align: center; margin-top: 50px;",
        ),
    )


@app.get("/health")
def health():  # type: ignore
    logger.info("❤️ Health check endpoint accessed")
    return {"status": "ok", "phase": "1"}


if __name__ == "__main__":
    serve()
