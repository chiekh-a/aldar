"""SQL Query Executor.

Executes SQL queries against any SQLAlchemy-supported database.
Supports SELECT, INSERT, UPDATE, DELETE statements with parameterized queries.
"""

import asyncio
import time
from functools import partial
from typing import Any, Dict, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)

from sql_mcp_server.models import SQLQueryOutput


def _serialize_value(value: Any) -> Any:
    """Serialize a database value to JSON-compatible format."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if hasattr(value, "isoformat"):
        # datetime, date, time objects
        return value.isoformat()
    if hasattr(value, "__dict__"):
        return str(value)
    return str(value)


def _execute_query_sync(
    database_url: str,
    query: str,
    params: Optional[Dict[str, Any]] = None,
) -> SQLQueryOutput:
    """Execute a SQL query synchronously and return results."""
    start_time = time.perf_counter()

    try:
        # Create engine with connection pooling disabled for one-off queries
        engine = create_engine(
            database_url,
            poolclass=None,  # Disable pooling for single queries
            connect_args={"connect_timeout": 10} if "sqlite" not in database_url else {},
        )

        with engine.connect() as connection:
            # Execute with optional parameters
            if params:
                result = connection.execute(text(query), params)
            else:
                result = connection.execute(text(query))

            # Check if this is a SELECT-like query that returns rows
            if result.returns_rows:
                rows = result.fetchall()
                columns = list(result.keys())

                # Convert rows to list of dicts
                rows_as_dicts = [
                    {col: _serialize_value(row[i]) for i, col in enumerate(columns)}
                    for row in rows
                ]

                execution_time = (time.perf_counter() - start_time) * 1000

                return SQLQueryOutput(
                    success=True,
                    rows=rows_as_dicts,
                    row_count=len(rows_as_dicts),
                    columns=columns,
                    execution_time_ms=round(execution_time, 2),
                )
            else:
                # For INSERT/UPDATE/DELETE, commit and return affected rows
                connection.commit()
                row_count = result.rowcount

                execution_time = (time.perf_counter() - start_time) * 1000

                return SQLQueryOutput(
                    success=True,
                    rows=None,
                    row_count=row_count if row_count >= 0 else 0,
                    columns=None,
                    execution_time_ms=round(execution_time, 2),
                )

    except OperationalError as e:
        # Connection errors, timeout, etc.
        error_msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
        return SQLQueryOutput(
            success=False,
            error=f"Connection error: {error_msg}",
            error_type="connection_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )

    except ProgrammingError as e:
        # SQL syntax errors, invalid table/column names
        error_msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
        return SQLQueryOutput(
            success=False,
            error=f"SQL error: {error_msg}",
            error_type="syntax_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )

    except IntegrityError as e:
        # Constraint violations (unique, foreign key, etc.)
        error_msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
        return SQLQueryOutput(
            success=False,
            error=f"Constraint violation: {error_msg}",
            error_type="integrity_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )

    except DatabaseError as e:
        # General database errors
        error_msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
        return SQLQueryOutput(
            success=False,
            error=f"Database error: {error_msg}",
            error_type="database_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )

    except SQLAlchemyError as e:
        # Catch-all for other SQLAlchemy errors
        error_msg = str(e)
        return SQLQueryOutput(
            success=False,
            error=f"Query error: {error_msg}",
            error_type="sqlalchemy_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )

    except Exception as e:
        # Unexpected errors
        error_msg = str(e)
        return SQLQueryOutput(
            success=False,
            error=f"Unexpected error: {error_msg}",
            error_type="unexpected_error",
            execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
        )


async def execute_query(
    database_url: str,
    query: str,
    params: Optional[Dict[str, Any]] = None,
) -> SQLQueryOutput:
    """Execute a SQL query asynchronously.

    Wraps the synchronous SQLAlchemy execution in asyncio.to_thread
    to avoid blocking the event loop.

    Args:
        database_url: SQLAlchemy database URL
        query: SQL query to execute
        params: Optional parameters for parameterized queries

    Returns:
        SQLQueryOutput with results or error information
    """
    return await asyncio.to_thread(
        partial(_execute_query_sync, database_url, query, params)
    )
