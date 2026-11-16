import sqlite3
from contextlib import closing
from pathlib import Path


def init_db(path: str) -> None:
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                channel INTEGER NOT NULL,
                count_rate REAL NOT NULL
            )
            """
        )
        conn.commit()


def insert_reading(path: str, timestamp: str, channel: int, count_rate: float) -> None:
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            "INSERT INTO readings (timestamp, channel, count_rate) VALUES (?, ?, ?)",
            (timestamp, channel, count_rate),
        )
        conn.commit()


def list_readings(path: str, limit: int = 100, channel: int | None = None) -> list[dict]:
    query = "SELECT timestamp, channel, count_rate FROM readings"
    params: list = []
    if channel is not None:
        query += " WHERE channel = ?"
        params.append(channel)
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    with closing(sqlite3.connect(path)) as conn:
        rows = conn.execute(query, params).fetchall()
    return [{"timestamp": t, "channel": c, "count_rate": r} for t, c, r in rows]


def channel_timestamps(path: str, channel: int) -> list[str]:
    with closing(sqlite3.connect(path)) as conn:
        rows = conn.execute(
            "SELECT timestamp FROM readings WHERE channel = ? ORDER BY timestamp",
            (channel,),
        ).fetchall()
    return [r[0] for r in rows]
