---
created: 2026-01-29 10:00
last-updated: 2026-01-29 10:05
status: planning
---

# FastMCP SQL Query Server

## What
Build a production-ready MCP server using FastMCP that exposes a `run_sql_query` tool for executing SQL queries against any SQLAlchemy-supported database, deployable to Railway.

## Why
This enables AI agents (Claude, etc.) to execute database queries through the MCP protocol, providing a standardized interface for database interactions with proper error handling, parameterized queries, and execution metrics.

## Success Criteria
- [ ] MCP server starts and accepts connections via HTTP transport
- [ ] `run_sql_query` tool executes SELECT/INSERT/UPDATE/DELETE queries
- [ ] Parameterized queries work correctly to prevent SQL injection
- [ ] Proper error handling for connection, syntax, integrity, and timeout errors
- [ ] Execution time metrics returned with each query result
- [ ] Server deployable to Railway with environment variable configuration
- [ ] Health check endpoint available for Railway deployment

## Out of Scope
- Connection pooling optimization (single-query engine pattern from reference code)
- Multiple database connection management (one URL per request)
- Query result caching
- User authentication/authorization layer
- Rate limiting
- Query logging to external service

## Approach
Create a minimal FastMCP server with a single tool `run_sql_query` that adapts the provided SQLAlchemy-based SQL execution logic. The server will use HTTP transport for deployment, accept database URLs at runtime (per-query), and return structured results matching the `SQLQueryOutput` model. Railway deployment via Dockerfile with environment-based configuration.

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLAlchemy sync blocking async event loop | High | Use `asyncer.asyncify()` or run in thread pool executor |
| Database credentials in query params | Med | Document security best practices, recommend connection string from env vars |
| Large result sets causing memory issues | Med | Document row limit recommendations, add optional limit parameter |

## Definition of Done
- [ ] All success criteria met
- [ ] Server runs locally with `uv run python -m sql_mcp_server.server` or `uv run fastmcp run`
- [ ] Can successfully query a test SQLite database
- [ ] Dockerfile builds and runs without errors (using uv)
- [ ] railway.toml ready for deployment
- [ ] README with usage examples and deployment instructions
