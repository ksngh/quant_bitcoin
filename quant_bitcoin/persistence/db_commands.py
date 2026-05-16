"""Version-controlled PostgreSQL command-file loading and execution.

The SQL files under ``db/`` are the source of truth for schema DDL and any
managed first-start/reference DML. Application code may load and execute those
files, but it must not duplicate schema DDL in Python constants.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class DbCommandFile:
    """One managed SQL command file loaded from the repository ``db/`` tree."""

    path: Path
    sql: str


class SqlConnection(Protocol):
    """Minimal connection protocol needed for DB command execution."""

    def execute(self, query: str) -> object:
        """Execute a SQL command string."""


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DB_ROOT = REPOSITORY_ROOT / "db"
DB_INIT_DIR = DB_ROOT / "init"
DB_CHANGES_DIR = DB_ROOT / "changes"


def list_sql_command_files(directory: Path) -> tuple[Path, ...]:
    """Return SQL command files in deterministic lexicographic execution order."""

    if not directory.exists():
        return ()
    if not directory.is_dir():
        raise NotADirectoryError(f"DB command path is not a directory: {directory}")
    return tuple(sorted(path for path in directory.iterdir() if path.suffix == ".sql"))


def load_sql_command_files(directory: Path) -> tuple[DbCommandFile, ...]:
    """Load SQL command files from ``directory`` in deterministic order."""

    return tuple(
        DbCommandFile(path=path, sql=path.read_text(encoding="utf-8"))
        for path in list_sql_command_files(directory)
    )


def load_initial_db_commands() -> tuple[DbCommandFile, ...]:
    """Load first-start/init DB commands managed under ``db/init``."""

    return load_sql_command_files(DB_INIT_DIR)


def load_change_db_commands() -> tuple[DbCommandFile, ...]:
    """Load future existing-database change commands managed under ``db/changes``.

    An empty tuple is the expected current behavior when no change files have
    been added yet.
    """

    return load_sql_command_files(DB_CHANGES_DIR)


def execute_db_commands(
    connection: SqlConnection, commands: tuple[DbCommandFile, ...]
) -> None:
    """Execute loaded SQL command files in order on ``connection``."""

    for command in commands:
        connection.execute(command.sql)


def execute_initial_db_commands(connection: SqlConnection) -> None:
    """Execute all managed first-start/init DB commands on ``connection``."""

    execute_db_commands(connection, load_initial_db_commands())
