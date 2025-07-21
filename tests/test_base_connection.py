import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.connections.base import BaseConnection
from unittest.mock import Mock


class TestBaseConnection:
    """Tests for BaseConnection class"""

    def test_init_creates_connection_with_correct_params(
        self, mock_psycopg2, mock_env_vars, sample_connection_params
    ):
        """BaseConnection initialises with correct connection parameters"""
        connection = BaseConnection()

        mock_psycopg2.assert_called_once_with(
            host=sample_connection_params["host"],
            database=sample_connection_params["database"],
            user=sample_connection_params["user"],
            password=sample_connection_params["password"],
        )
        assert connection.conn == mock_psycopg2.return_value

    def test_init_uses_environment_password(self, mock_psycopg2, mock_env_vars):
        """BaseConnection uses DB_PASSWORD from environment"""
        BaseConnection()

        call_args = mock_psycopg2.call_args
        assert call_args[1]["password"] == "test_password"

    def test_get_connection_returns_connection(self, mock_psycopg2):
        """get_connection returns the connection object"""
        connection = BaseConnection()

        result = connection.get_connection()

        assert result == connection.conn
        assert result == mock_psycopg2.return_value

    def test_close_connection_calls_close_on_connection(self, mock_psycopg2):
        """close_connection calls close() on the connection"""
        connection = BaseConnection()
        mock_conn = connection.conn

        connection.close_connection()

        mock_conn.close.assert_called_once()  # type: ignore # for some reason this wont notice its a mock

    def test_health_check_returns_connection_status(self, mock_psycopg2):
        """health_check returns the connection status"""
        connection = BaseConnection()
        expected_status = 1

        result = connection.health_check()

        assert result == expected_status

    def test_health_check_with_different_status(self, mock_psycopg2):
        """health_check with different connection status"""
        mock_conn = Mock()
        mock_conn.status = 0
        mock_psycopg2.return_value = mock_conn
        connection = BaseConnection()

        result = connection.health_check()

        assert result == 0
