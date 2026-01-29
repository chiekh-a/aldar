"""FastMCP Server for SQL Query Execution.

MCP server that exposes a run_sql_query tool for executing SQL queries
against any SQLAlchemy-supported database.
"""

import logging
import os
from typing import Annotated, Any, Dict, Optional

from fastmcp import FastMCP
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from sql_mcp_server.sql_executor import execute_query

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("SQL Query Server")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for load balancers and monitoring."""
    return JSONResponse({"status": "healthy", "service": "sql-mcp-server"})


@mcp.tool
async def run_sql_query(
    database_url: Annotated[
        str,
        Field(
            description="SQLAlchemy database URL (e.g., postgresql://user:pass@host:port/dbname, mysql+pymysql://user:pass@host:3306/dbname, sqlite:///./test.db)"
        ),
    ],
    query: Annotated[
        str,
        Field(
            description="SQL query to execute. Supports SELECT, INSERT, UPDATE, DELETE statements."
        ),
    ],
    params: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description="Optional parameters for parameterized queries to prevent SQL injection."
        ),
    ] = None,
) -> dict:
    """Execute a SQL query against a database.

    Supports PostgreSQL, MySQL, SQLite, and other SQLAlchemy-compatible databases.
    Use parameterized queries for safety.

    Returns a dictionary with:
    - success: Whether the query executed successfully
    - rows: Query results as a list of dictionaries (for SELECT queries)
    - row_count: Number of rows returned (SELECT) or affected (INSERT/UPDATE/DELETE)
    - columns: Column names from the result set (for SELECT queries)
    - error: Error message if the query failed
    - error_type: Type of error that occurred
    - execution_time_ms: Query execution time in milliseconds
    """
    logger.info(f"Executing SQL query: {query[:100]}...")

    result = await execute_query(database_url, query, params)

    if result.success:
        logger.info(f"Query succeeded: {result.row_count} rows in {result.execution_time_ms}ms")
    else:
        logger.error(f"Query failed: {result.error_type} - {result.error}")

    return result.model_dump()


def main():
    """Entry point for the server."""
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    logger.info(f"Starting SQL MCP Server on {host}:{port}")

    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    main()
