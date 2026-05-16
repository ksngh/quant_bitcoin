# Database Command Management

Task 024 makes version-controlled SQL files under `db/` the source of truth for PostgreSQL DDL and managed first-start/reference DML.

## Audit of Existing DB Commands

| Location | Command type | Task 024 decision |
| --- | --- | --- |
| `db/init/001_schema.sql` | DDL: `CREATE TABLE` and `CREATE INDEX` statements for candles, ingestion checkpoints, strategy configs, backtest runs, backtest results, backtest trades, and backtest graph points. | Source of truth for the accepted PostgreSQL schema. Docker first-start initialization and repository `initialize_schema()` both execute this managed file. |
| `quant_bitcoin/persistence/postgres.py` | Runtime DML: candle upsert, checkpoint upsert/load, backtest result persistence inserts/deletes/upserts, and read-model `SELECT` queries. | Remains application-owned runtime persistence logic because it depends on runtime payloads, transactions, row mapping, idempotent upserts, and read-model filters. It is not first-start schema/reference data. |
| `quant_bitcoin/persistence/postgres.py` before Task 024 | Duplicated DDL in `SCHEMA_SQL`. | Removed. Python no longer owns a separate schema DDL string. |
| `tests/` | Contract assertions over schema and runtime SQL behavior. | Tests now load managed SQL files from `db/` for DDL assertions and use fake connections to verify initialization executes command files in deterministic order. |
| README/docs/task documents | Human guidance and historical task notes. | README now points to this document and the current managed SQL layout. Historical task files may still describe earlier decisions in their original context. |

No managed seed/reference DML is currently required. Therefore `db/init/` currently contains schema DDL only.

## Directory Layout

```text
db/
  init/
    001_schema.sql       # Fresh database first-start DDL, executed by Docker init and app initialization.
  changes/
    .gitkeep             # Placeholder. Add ordered SQL files here for future existing-DB state changes.
```

## Fresh Database Initialization

Docker Compose mounts `./db/init` into PostgreSQL's `/docker-entrypoint-initdb.d` directory. On a fresh PostgreSQL data volume, the PostgreSQL image executes the managed SQL files in filename order.

Application repository initialization uses `quant_bitcoin.persistence.db_commands` to load `db/init/*.sql` in deterministic lexicographic order and execute each file on the provided PostgreSQL connection. This keeps local application initialization aligned with Docker first-start initialization without copying DDL into Python.

## Future Existing-Database Changes

Use `db/changes/` for explicit SQL command files that move an already-existing database from an older accepted state to a newer accepted state.

Naming convention:

```text
db/changes/NNN_short_description.sql
```

Rules:

- Use a zero-padded numeric prefix (`001`, `002`, `003`, ...).
- Keep filenames stable after review/merge.
- Make each file an explicit state-change command for an existing database.
- Do not add runtime persistence DML here unless it is a one-time state change or managed reference/seed command.
- Ordinary application writes such as candle upserts, checkpoint upserts, and backtest result inserts remain in repository runtime logic.

Current behavior when `db/changes/` has no `.sql` files: the command loader returns an empty tuple and executes nothing.

## Runtime Persistence DML Boundary

Runtime DML remains application-owned in `quant_bitcoin/persistence/postgres.py` for now:

- candle upsert writes runtime market data payloads and updates duplicate candles by identity;
- ingestion checkpoint upsert writes mutable restart state;
- strategy config, backtest run, result, trade, and graph-point DML is part of one transaction for a completed simulated run;
- read-model `SELECT` queries are runtime application behavior for loading persisted data.

These statements are intentionally not placed under `db/init/` because they are not first-start DDL or static reference data. They are intentionally not placed under `db/changes/` because they are not one-time existing-database state changes.
