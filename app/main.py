# ABOUTME: Main FastHTML application entry point for BlogBot
# ABOUTME: Sets up the web server, routes, and database connections
# mypy: disable-error-code="name-defined,no-any-return"

from fasthtml.common import *  # type: ignore

# Create the FastHTML app
app = FastHTML()


@app.get("/")
def home():  # type: ignore
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
    return {"status": "ok", "phase": "1"}


if __name__ == "__main__":
    serve()
