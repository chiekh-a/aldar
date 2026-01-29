"""Models for SQL Query Tool."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SQLQueryInput(BaseModel):
    """Input model for SQL query tool."""

    database_url: str = Field(
        ...,
        description="SQLAlchemy database URL (e.g., postgresql://user:pass@host:port/dbname)",
    )
    query: str = Field(
        ...,
        description="SQL query to execute. Supports SELECT, INSERT, UPDATE, DELETE statements.",
    )
    params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional parameters for parameterized queries to prevent SQL injection.",
    )


class SQLQueryOutput(BaseModel):
    """Output model for SQL query tool."""

    success: bool = Field(..., description="Whether the query executed successfully")
    rows: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Query results as a list of dictionaries (for SELECT queries)",
    )
    row_count: int = Field(
        default=0,
        description="Number of rows returned (SELECT) or affected (INSERT/UPDATE/DELETE)",
    )
    columns: Optional[List[str]] = Field(
        default=None,
        description="Column names from the result set (for SELECT queries)",
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if the query failed",
    )
    error_type: Optional[str] = Field(
        default=None,
        description="Type of error that occurred (e.g., 'connection_error', 'syntax_error')",
    )
    execution_time_ms: Optional[float] = Field(
        default=None,
        description="Query execution time in milliseconds",
    )
