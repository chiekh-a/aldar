---
created: 2026-01-29 10:00
last-updated: 2026-01-29 10:05
---

# Context: FastMCP SQL Query Server

## File Map
_Use markers: [CREATE] [MODIFY] [DELETE] [KEEP] [REFERENCE]_

```
[CREATE]    @sql_mcp_server/server.py        - Main FastMCP server with run_sql_query tool
[CREATE]    @sql_mcp_server/models.py        - Pydantic models (SQLQueryInput, SQLQueryOutput)
[CREATE]    @sql_mcp_server/__init__.py      - Package init
[CREATE]    @pyproject.toml                  - Python project config with dependencies (uv compatible)
[CREATE]    @uv.lock                         - uv lockfile (auto-generated)
[CREATE]    @Dockerfile                      - Container image for Railway deployment (using uv)
[CREATE]    @railway.toml                    - Railway deployment configuration
[CREATE]    @.env.example                    - Example environment variables
[CREATE]    @README.md                       - Usage and deployment documentation
```

## Quick Reference
_Fast lookup for implementation details_

**Key Values**:
- Default port: `8000`
- Transport: `http` (accessible at `/mcp`)
- Connection timeout: `10` seconds
- Tool name: `run_sql_query`

**Environment Variables**:
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `LOG_LEVEL` - Logging level (default: INFO)

**SQLAlchemy Database URL Examples**:
- PostgreSQL: `postgresql://user:pass@host:5432/dbname`
- MySQL: `mysql+pymysql://user:pass@host:3306/dbname`
- SQLite: `sqlite:///./test.db`

## Key Decisions
_Document choices and rationale for future reference_

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transport | HTTP (not SSE) | FastMCP recommends HTTP for new projects; better for deployment |
| Sync vs Async | Sync SQLAlchemy with thread pool | SQLAlchemy core is sync; wrapping with asyncer/asyncio.to_thread avoids blocking |
| Connection pooling | Disabled (poolclass=None) | Per reference code: one-off queries don't benefit from pooling |
| Input validation | strict_input_validation=True | Production safety; reject malformed requests |
| Database URL handling | Per-request parameter | Flexibility to query any database; matches reference code pattern |

## Dependencies

**Upstream** (must be complete first):
- None (greenfield project)

**Downstream** (depends on this work):
- Future tools can be added to the same server

**External** (third-party):
- `fastmcp` - ^2.0 - MCP server framework
- `sqlalchemy` - ^2.0 - Database abstraction
- `pydantic` - ^2.0 - Data validation (bundled with fastmcp)
- `uvicorn` - ^0.30 - ASGI server (for production)
- `psycopg2-binary` - ^2.9 - PostgreSQL driver (optional)
- `pymysql` - ^1.1 - MySQL driver (optional)

**Tooling**:
- `uv` - Fast Python package manager (replaces pip/pip-tools)

## Open Questions
_Unresolved items that may affect implementation_
- [x] Should database URL be per-request or server-wide config? → **Per-request** (matches reference code)
- [ ] Should we add a `list_tables` or `describe_table` helper tool? → **Deferred to future scope**

## FastMCP Patterns (from context7 research)

### Basic Tool Definition
```python
from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

mcp = FastMCP("SQL Query Server", strict_input_validation=True)

@mcp.tool
async def run_sql_query(
    database_url: Annotated[str, Field(description="SQLAlchemy database URL")],
    query: Annotated[str, Field(description="SQL query to execute")],
    params: Annotated[dict | None, Field(description="Query parameters")] = None,
) -> dict:
    """Execute a SQL query."""
    # Implementation
    pass
```

### Running the Server
```python
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

### uv Commands
```bash
# Install dependencies
uv sync

# Run server
uv run python -m sql_mcp_server.server

# Add a dependency
uv add sqlalchemy

# Add dev dependency
uv add --dev pytest
```

### Wrapping Sync Code for Async
```python
import asyncio
from functools import partial

async def run_sync_in_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))
```

## Reference Code Analysis

The provided SQLQueryTool has these key features to preserve:
1. **Engine creation per query** with poolclass=None and connect_timeout=10
2. **Parameterized query support** via SQLAlchemy text() binding
3. **Row detection** via result.returns_rows
4. **Value serialization** for bytes, datetime, and complex objects
5. **Granular error handling** for Operational, Programming, Integrity, Database errors
6. **Execution time tracking** via time.perf_counter()
