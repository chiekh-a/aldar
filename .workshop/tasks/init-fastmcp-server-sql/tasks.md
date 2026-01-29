---
created: 2026-01-29 10:00
last-updated: 2026-01-29 10:05
current-phase: 5
---

# Tasks: FastMCP SQL Query Server

## Phase 1: Project Setup ✓
_Prerequisites: None_

- [x] Create project directory structure: `sql_mcp_server/`
- [x] Create `pyproject.toml` with dependencies: fastmcp, sqlalchemy, pydantic, uvicorn, psycopg2-binary (uv-compatible format)
- [x] Run `uv sync` to generate `uv.lock` and install dependencies
- [x] Create `sql_mcp_server/__init__.py`
- [x] Create `.env.example` with PORT, HOST, LOG_LEVEL
- [x] **VERIFY**: `uv sync` succeeds without errors and creates uv.lock

## Phase 2: Core Models ✓
_Prerequisites: Phase 1 complete_

- [x] Create `sql_mcp_server/models.py` with SQLQueryInput model (database_url, query, params)
- [x] Create SQLQueryOutput model (success, rows, row_count, columns, error, error_type, execution_time_ms)
- [x] Add Field descriptions matching the reference code exactly
- [x] **VERIFY**: Models can be imported: `uv run python -c "from sql_mcp_server.models import SQLQueryInput, SQLQueryOutput"`

## Phase 3: SQL Execution Logic ✓
_Prerequisites: Phase 2 complete_

- [x] Create `sql_mcp_server/sql_executor.py` with execute_query function
- [x] Implement engine creation with poolclass=None and connect_timeout=10
- [x] Implement parameterized query execution using text() binding
- [x] Implement row detection (returns_rows) and result conversion
- [x] Implement _serialize_value helper for bytes, datetime, complex objects
- [x] Implement granular error handling (OperationalError, ProgrammingError, IntegrityError, DatabaseError, SQLAlchemyError)
- [x] Add execution time tracking with time.perf_counter()
- [x] Wrap sync execution in async using asyncio.to_thread
- [x] **VERIFY**: Test with SQLite: `uv run python -c "import asyncio; from sql_mcp_server.sql_executor import execute_query; print(asyncio.run(execute_query('sqlite:///test.db', 'SELECT 1 as test', None)))"`

## Phase 4: FastMCP Server ✓
_Prerequisites: Phase 3 complete_

- [x] Create `sql_mcp_server/server.py` with FastMCP instance
- [x] Define `run_sql_query` tool with Annotated type hints and Field descriptions
- [x] Wire tool to call execute_query from sql_executor
- [x] Add environment variable handling for PORT, HOST, LOG_LEVEL
- [x] Add main block with mcp.run(transport="http")
- [x] **VERIFY**: Server starts: `uv run python -m sql_mcp_server.server` shows "Starting server on 0.0.0.0:8000"

## Phase 5: Deployment Configuration
_Prerequisites: Phase 4 complete_

- [x] Create `Dockerfile` with Python 3.11+, uv install, and CMD for server
- [x] Use multi-stage build: uv for deps, slim runtime image
- [x] Create `railway.toml` with build and deploy config
- [x] Add health check consideration (FastMCP HTTP transport has built-in /health or /mcp endpoint)
- [x] Update `pyproject.toml` with [project.scripts] entry point
- [ ] **VERIFY**: `docker build -t sql-mcp-server .` succeeds
- [ ] **VERIFY**: `docker run -p 8000:8000 sql-mcp-server` starts and responds

## Phase 6: Documentation & Testing
_Prerequisites: Phase 5 complete_

- [ ] Create README.md with: overview, installation, usage examples, deployment instructions
- [ ] Add example MCP client usage snippet
- [ ] Add example curl command to test the server
- [ ] Document supported database URLs
- [ ] **VERIFY**: README renders correctly on GitHub
- [ ] **VERIFY**: Run full Definition of Done checklist

---

## Blocked
_Tasks that cannot proceed and why_

(none)
