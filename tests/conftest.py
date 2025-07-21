import pytest
import os
from unittest.mock import Mock, patch
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def mock_psycopg2():
    """Mock psycopg2 connection for testing."""
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = Mock()
        mock_conn.status = 1
        mock_conn.close = Mock()
        mock_connect.return_value = mock_conn
        yield mock_connect


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {"DB_PASSWORD": "test_password"}):
        yield


@pytest.fixture
def mock_cursor():
    """Mock cursor for testing database operations."""
    mock_cursor = Mock()
    mock_cursor.execute.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_cursor.fetchone.return_value = None

    # set up context manager behavior - better than reusing every test
    mock_cursor.__enter__ = Mock(return_value=mock_cursor)
    mock_cursor.__exit__ = Mock(return_value=None)

    return mock_cursor


@pytest.fixture
def mock_db_connection(mock_psycopg2, mock_cursor):
    """Complete mock database connection with cursor."""
    mock_conn = mock_psycopg2.return_value
    mock_conn.cursor = Mock(return_value=mock_cursor)
    mock_conn.commit = Mock()

    return mock_cursor


@pytest.fixture
def sample_connection_params():
    """Sample connection parameters for testing."""
    return {
        "host": "db",
        "database": "panda_db",
        "user": "postgres",
        "password": "test_password",
    }
