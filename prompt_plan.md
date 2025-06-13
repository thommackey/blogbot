Below is a single markdown file containing (a) a carefully‑layered blueprint that has been refined twice into right‑sized, safety‑first steps and (b) a sequenced set of LLM prompts—each in its own text code fence—that implement those steps test‑first and without leaving stray code. Save the file locally (e.g., blog‑engine‑roadmap.md) for the agent to consume.

⸻

📜 Blog Engine Build Blueprint & LLM Prompt Suite

0  | Guiding Principles

#	Principle	Why it matters
1	Incrementalism	Each slice deploys & tests in <1 hour to de‑risk early.
2	API‑first	Every UI action calls the same documented endpoint.
3	Stateless Core	No hidden server state → easier scaling & idempotence.
4	Strong Contracts	Type hints + pytest + ruff + mypy gate every PR.
5	No Orphans	Every new artifact is wired into routing and CI before moving on.


⸻

1  | Phase & Sprint Breakdown (🔍 Round 1 granularity)

Phase	Sprint (≈3 days)	Deliverable
0 Bootstrap	0‑A Repo Skeleton	pyproject, Dockerfile, pre‑commit, empty FastHTML app
 	0‑B CI Wiring	GitHub Actions running lint+type+test
1 Auth + GitHub	1‑A OAuth Flow	/auth/github & session cookie
 	1‑B GitHub Client	Typed wrapper with retry + rate‑limit handling
2 Settings DB	2‑A Schema	Sqlite + migration script
 	2‑B Settings CRUD API	/api/settings endpoints & tests
3 Content API	3‑A Read List	/api/content list with mock GitHub
 	3‑B Read Single	/api/content/{path}
 	3‑C Write	create/update POST
 	3‑D Delete	DELETE endpoint
4 Site Gen	4‑A Markdown → HTML	Markdown+front‑matter parser
 	4‑B Static Builder	Generates dist/ ready for GitHub Pages
5 Editor UI	5‑A Layout	Dashboard + Editor skeleton (HTMX)
 	5‑B Pause‑Preview	2‑sec debounce preview
6 Publish	6‑A Pages Push	/api/publish + branch create/update
7 Images	7‑A Upload Route	/api/images streaming‑to‑GitHub
8 Security	8‑A API Keys	table, hash, middleware
9 Feeds	9‑A RSS Generator	/feed.xml in static output
10 Polish	10‑A Perf & Docs	gzip, caching headers, OAS docs
 	10‑B Render Deploy	render.yaml & green button


⸻

2  | Ticket‑Sized Steps (🔬 Round 2 micro‑breakdown)

Below is a single example sprint (3‑A Read List) decomposed further; every other sprint has an equivalent micro‑board in the full project tracker (omitted here for brevity).

Step	Δ	Safety Hook
3‑A‑1	Add ContentItem Pydantic model	Unit test for .dict() schema
3‑A‑2	Stub services/github.py -> list_markdown() returns empty list	pytest mock GitHub
3‑A‑3	Wire GET /api/content route returning hard‑coded empty list	super‑test client call
3‑A‑4	Implement real list_markdown() using GitHub search API	vcrpy cassette
3‑A‑5	Return hydrated ContentItem list	JSON schema assertion
3‑A‑6	Update OpenAPI docs with example payload	swagger‑generated diff test

(Repeat micro‑breakdown pattern for every sprint.)

⸻

3  | Sequenced LLM Prompts (💬 Copy ⇒ Paste into code‑gen agent)

How to use: After each prompt finishes and tests pass, commit; then feed the next prompt.
All prompts assume repo root, Python 3.12, FastAPI == “FastHTML”, pytest, ruff, mypy pre‑installed.

⸻

Prompt 01 – Project Skeleton

You are ChatGPT‑Dev acting as an autonomous coder.

TASK:
1. Scaffold repo `blog_engine/` per spec:
   • pyproject.toml using `poetry`
   • `app/__init__.py`, `app/main.py` with a minimal FastHTML instance that returns `{ "status": "ok" }` at `/health`.
2. Add `.pre‑commit‑config.yaml` from spec.
3. Add `Dockerfile` from spec unchanged.
4. Write an initial `tests/test_health.py` that asserts 200 and JSON `status == "ok"`.

CONSTRAINTS:
- Use type hints everywhere.
- No business logic yet.
- All tests must pass `pytest -q`.

OUTPUT: Modified files only.


⸻

Prompt 02 – CI Pipeline

OBJECTIVE: Establish continuous quality gates.

STEPS:
1. Create `.github/workflows/ci.yml` that:
   a. Runs on push + PR.
   b. Caches Poetry.
   c. Executes `pre-commit run --all-files` and `pytest -q`.
2. Ensure exit code 1 if any hook or test fails.

VALIDATION: Add `tests/test_ci_stub.py` that always passes so pipeline stays green.

DELIVERABLE: New workflow file and passing tests.


⸻

Prompt 03 – Settings DB Schema

GOAL: Add Sqlite settings schema + migration.

INSTRUCTIONS:
1. Add dependency `alembic`.
2. Create `app/models/base.py` (SQLModel or SQLAlchemy 2.0) and `settings.py` per spec (single‑row table).
3. Provide Alembic `env.py` + first migration script auto‑generated.
4. Write `tests/test_settings_model.py` that:
   • Creates in‑memory DB
   • Inserts default row
   • Asserts id == 1 and unique constraint.

NOTE: Keep app bootstrapping untouched; migrations run via CLI later.


⸻

Prompt 04 – GitHub OAuth Flow

ADD: GitHub OAuth login with FastHTML.

DETAILS:
1. Use `authlib` to implement `/auth/github` (redirect) and `/auth/github/callback`.
2. On success, store GitHub `access_token` in signed cookie; no DB yet.
3. Provide config via env vars (`GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `SECRET_KEY`).
4. Provide stub HTML template explaining “Login successful”.

TESTS:
- Mock GitHub (responses library) to simulate token exchange.
- `tests/test_auth.py` ensures callback sets cookie and returns 200.

SECURITY: Use `state` param to prevent CSRF.


⸻

Prompt 05 – Typed GitHub Client

Create `app/services/github.py` wrapping `httpx.AsyncClient`.

FEATURES:
- `get_user()` -> login + email.
- Graceful retry (backoff) on 5xx and 429.
- Raises `GitHubAPIError` with `.action` hint on failure.

TESTS: Parametrized pytest for success (mock JSON) and failure (429) paths.

DOCS: Add docstring w/ example.


⸻

Prompt 06 – /GET api/content (empty)

TARGET: Implement read‑only `/api/content` returning empty list via github service stub.

STEPS:
1. Add `ContentItem` Pydantic model (path, title, date, type, tags).
2. Route returns `{"items": []}`.
3. Tests assert empty response & schema.

INTEGRATE: Register route in `app/main.py` router.


⸻

Prompt 07 – Content Listing GitHub Integration

UPGRADE `/api/content` to fetch real Markdown list.

LOGIC:
1. In `github.py`, add `list_markdown(repo:str)` that searches `*.md` blobs and returns minimal metadata.
2. Parse front‑matter **only filename stage** (title from slug).
3. Return hydrated ContentItem list, sorted by date desc.

TESTS:
- Use vcrpy cassette (`tests/cassettes/list_content.yaml`) with GitHub demo repo.


⸻

Prompt 08 – Get Single Content

Add `/api/content/{path}` route.

REQUIREMENTS:
1. Calls `github.get_file(repo, path)` to fetch raw text.
2. Splits front‑matter via `markdown.py::parse_frontmatter`.
3. Returns JSON `{path, content, frontmatter}`.

Write unit + integration tests (mock GitHub).


⸻

Prompt 09 – Create/Update Content

Implement POST `/api/content`.

WORK:
1. Accept JSON body from spec.
2. Validate via Pydantic model; default date ↦ `utcnow()`.
3. Compute slug if path not provided; ensure uniqueness (append ‑1).
4. Commit file via GitHub “create or update” API.

TESTS: 
- Mock GitHub to assert correct API call body.
- Ensure 201 status & returned URL follows pattern `/YYYY-MM-DD-slug`.


⸻

Prompt 10 – Delete Content

Implement DELETE `/api/content/{path}`.

DETAILS:
- Call GitHub delete file API with SHA (fetch first to get sha).
- Return `{"status":"deleted"}`.

Test happy + not‑found → 404.


⸻

Prompt 11 – Markdown Processor

Create `app/services/markdown.py`.

FUNCTIONS:
1. `parse_frontmatter(text:str)->(dict, str)`
2. `render_markdown(md:str)->str` using `markdown-it-py`.
3. `slugify(title:str)->str`.

Add unit tests w/ edge cases (emoji, non‑ascii).


⸻

Prompt 12 – Static Site Generator MVP

GOAL: CLI `python -m app.services.static_site build`.

STEPS:
1. Walk all markdown in repo via github client.
2. For each, render HTML (no CSS) and write into `dist/` tmp dir.
3. Generate `index.html` listing posts + `/feed.xml` (empty for now).
4. Return path of generated dir.

TESTS: Use tmp dir fixture; verify a post file ends with `</html>`.


⸻

Prompt 13 – Editor Dashboard & HTMX Preview

FRONT‑END: Add Jinja templates.

TASKS:
1. Dashboard (`/`) calls `/api/content` via fetch → renders table.
2. Editor (`/edit/{path}`) shows split view.
3. HTMX `hx-trigger="keyup changed delay:2s"` posts MD to `/api/preview` returning rendered HTML.

Server route `/api/preview` uses `render_markdown`.

Add Selenium (playwright) e2e test for preview debounce (1 post only).


⸻

Prompt 14 – Publish Endpoint

Implement POST `/api/publish`.

PROCESS:
1. Call `static_site.build()` -> dir.
2. Push dir (as commit) to `github_pages_repo`'s `gh-pages`.
3. Return success JSON with timestamp & URL.

Danger paths (branch protected) should raise 422 with action field.

Write integration test with mocked GitHub Pages repo.


⸻

Prompt 15 – Image Upload

Add `/api/images` accepting `multipart/form-data`.

WORK:
1. Stream bytes directly to `images/YYYY/filename` in content repo.
2. Return path + markdown embed snippet.

Add fastapi `UploadFile` chunked stream.
Unit test w/ 1 × PNG file.


⸻

Prompt 16 – API Keys & Middleware

SECURE API.

TASKS:
1. Table `api_keys` already exists; add creation CLI (`cli.py generate-key`).
2. Middleware reads `Authorization: Bearer`.
3. On miss, 401 JSON per spec.

Tests: auth success, missing, bad key.


⸻

Prompt 17 – RSS Feed Generator

Extend `static_site.build()`:

1. Collect latest 20 posts into RSS 2.0 XML (`/feed.xml`).
2. Add unit test comparing XML structure with fixture.

No change to editor.


⸻

Prompt 18 – Performance & Error Polishing

OBJECTIVES:
1. Add Uvicorn logging config (structured JSON).
2. Middleware adds `X-Request-ID`.
3. gzip static files during build.

Tests: assert gzip file exists & correct headers set.


⸻

Prompt 19 – Render Deploy Files

ADD:
- `render.yaml` specifying Docker build & env vars.
- Update README with one‑click deploy badge.

No tests needed, just static files.


⸻

Prompt 20 – End‑to‑End Publishing Flow

FINAL WIRING.

1. Write playwright script that:
   a. Logs in (mock GitHub).
   b. Creates post.
   c. Publishes site.
   d. Fetches generated HTML to assert new post present.

2. Hook script into CI (non‑cron skip decorator).

Ensure all TODOs resolved; project passes ruff, mypy, pytest, e2e.


⸻

4  | Next Steps for the Agent
	1.	Checkout empty repository.
	2.	Paste Prompt 01 into the code‑generation LLM; wait for tests to pass.
	3.	Commit and continue sequentially through Prompt 20.
	4.	Celebrate 🎉 — the Blog Engine is ready for first‑user onboarding!

⸻

End of file