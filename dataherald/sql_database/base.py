"""SQL wrapper around SQLDatabase in langchain."""
import logging
import re
from typing import Any, List
from urllib.parse import unquote

import sqlparse
from langchain.sql_database import SQLDatabase as LangchainSQLDatabase
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Engine
from sshtunnel import SSHTunnelForwarder

from dataherald.sql_database.models.types import DatabaseConnection
from dataherald.utils.encrypt import FernetEncrypt
from dataherald.utils.s3 import S3

logger = logging.getLogger(__name__)


# Define a custom exception class
class SQLInjectionError(Exception):
    pass


class InvalidDBConnectionError(Exception):
    pass


class DBConnections:
    db_connections = {}

    @staticmethod
    def add(uri, engine):
        DBConnections.db_connections[uri] = engine


class SQLDatabase(LangchainSQLDatabase):
    """SQL Database.

    Wrapper around SQLDatabase object from langchain. Offers
    some helper utilities for insertion and querying.
    See `langchain documentation <https://tinyurl.com/4we5ku8j>`_ for more details:

    Args:
        *args: Arguments to pass to langchain SQLDatabase.
        **kwargs: Keyword arguments to pass to langchain SQLDatabase.

    """

    @property
    def engine(self) -> Engine:
        """Return SQL Alchemy engine."""
        return self._engine

    @property
    def metadata_obj(self) -> MetaData:
        """Return SQL Alchemy metadata."""
        return self._metadata

    @classmethod
    def from_uri(
        cls, database_uri: str, engine_args: dict | None = None, **kwargs: Any
    ) -> "SQLDatabase":
        """Construct a SQLAlchemy engine from URI."""
        _engine_args = engine_args or {}
        if database_uri.lower().startswith("duckdb"):
            config = {"autoload_known_extensions": False}
            _engine_args["connect_args"] = {"config": config}
        engine = create_engine(database_uri, **_engine_args)
        return cls(engine, **kwargs)

    @classmethod
    def get_sql_engine(
        cls, database_info: DatabaseConnection, refresh_connection=False
    ) -> "SQLDatabase":
        logger.info(f"Connecting db: {database_info.id}")
        if (
            database_info.id
            and database_info.id in DBConnections.db_connections
            and not refresh_connection
        ):
            return DBConnections.db_connections[database_info.id]

        fernet_encrypt = FernetEncrypt()
        try:
            if database_info.use_ssh:
                engine = cls.from_uri_ssh(database_info)
                DBConnections.add(database_info.id, engine)
                return engine
            db_uri = unquote(fernet_encrypt.decrypt(database_info.connection_uri))
            if db_uri.lower().startswith("bigquery"):
                file_path = database_info.path_to_credentials_file
                if file_path.lower().startswith("s3"):
                    s3 = S3()
                    file_path = s3.download(file_path)

                db_uri = db_uri + f"?credentials_path={file_path}"

            engine = cls.from_uri(db_uri)
            DBConnections.add(database_info.id, engine)
        except Exception as e:
            raise InvalidDBConnectionError(  # noqa: B904
                f"Unable to connect to db: {database_info.alias}, {e}"
            )
        return engine

    @classmethod
    def extract_parameters(cls, input_string):
        # Define a regex pattern to extract the required parameters
        pattern = r"([^:/]+)://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^/]+)"

        # Use the regex pattern to match and extract the parameters
        match = re.match(pattern, input_string)

        if match:
            driver = match.group(1)
            user = match.group(2)
            password = match.group(3)
            host = match.group(4)
            port = match.group(5)
            db = match.group(6) if match.group(6) else None

            # Create a dictionary with the extracted parameters
            return {
                "driver": driver,
                "user": user,
                "password": password,
                "host": host,
                "port": port if port else None,
                "db": db,
            }

        return None

    @classmethod
    def from_uri_ssh(cls, database_info: DatabaseConnection):
        file_path = database_info.path_to_credentials_file
        if file_path.lower().startswith("s3"):
            s3 = S3()
            file_path = s3.download(file_path)

        fernet_encrypt = FernetEncrypt()
        db_uri = unquote(fernet_encrypt.decrypt(database_info.connection_uri))
        db_uri_obj = cls.extract_parameters(db_uri)
        ssh = database_info.ssh_settings

        server = SSHTunnelForwarder(
            (ssh.host, 22 if not ssh.port else int(ssh.port)),
            ssh_username=ssh.username,
            ssh_password=fernet_encrypt.decrypt(ssh.password),
            ssh_pkey=file_path,
            ssh_private_key_password=fernet_encrypt.decrypt(ssh.private_key_password),
            remote_bind_address=(
                db_uri_obj["host"],
                5432 if not db_uri_obj["port"] else int(db_uri_obj["port"]),
            ),
        )
        server.start()
        local_port = str(server.local_bind_port)
        local_host = str(server.local_bind_host)

        return cls.from_uri(
            f"{db_uri_obj['driver']}://{db_uri_obj['user']}:{db_uri_obj['password']}@{local_host}:{local_port}/{db_uri_obj['db']}"
        )

    @classmethod
    def parser_to_filter_commands(cls, command: str) -> str:
        sensitive_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "GRANT",
            "REVOKE",
            "ALTER",
            "TRUNCATE",
            "MERGE",
            "EXECUTE",
        ]
        parsed_command = sqlparse.parse(command)

        for stmt in parsed_command:
            for token in stmt.tokens:
                if (
                    isinstance(token, sqlparse.sql.Token)
                    and token.normalized in sensitive_keywords
                ):
                    raise SQLInjectionError(
                        f"Sensitive SQL keyword '{token.normalized}' detected in the query."
                    )

        return command

    def run_sql(self, command: str, top_k: int = None) -> tuple[str, dict]:
        """Execute a SQL statement and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        with self._engine.connect() as connection:
            command = self.parser_to_filter_commands(command)
            cursor = connection.execute(text(command))
            if cursor.returns_rows and top_k:
                result = cursor.fetchmany(top_k)
                return str(result), {"result": result}
            if cursor.returns_rows:
                result = cursor.fetchall()
                return str(result), {"result": result}
        return "", {}

    # from llama-index's sql-wrapper
    def get_table_columns(self, table_name: str) -> List[Any]:
        """Get table columns."""
        return self._inspector.get_columns(table_name)

    # from llama-index's sql-wrapper
    def get_single_table_info(self, table_name: str) -> str:
        """Get table info for a single table."""
        # same logic as table_info, but with specific table names
        template = (
            "Table '{table_name}' has columns: {columns} "
            "and foreign keys: {foreign_keys}."
        )
        columns = []
        for column in self._inspector.get_columns(table_name):
            columns.append(f"{column['name']} ({str(column['type'])})")
        column_str = ", ".join(columns)
        foreign_keys = []
        for foreign_key in self._inspector.get_foreign_keys(table_name):
            foreign_keys.append(
                f"{foreign_key['constrained_columns']} -> "
                f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
            )
        foreign_key_str = ", ".join(foreign_keys)
        return template.format(
            table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
        )
