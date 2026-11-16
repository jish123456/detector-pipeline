import os
from datetime import datetime

from fastapi import FastAPI, HTTPException

from app import db
from app.models import Reading
from app.validation import find_gaps, validate_rate


def create_app(db_path: str | None = None) -> FastAPI:
    path = db_path or os.environ.get("DB_PATH", "data/readings.db")
    db.init_db(path)
    app = FastAPI(title="Detector Data Pipeline")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/readings", status_code=201)
    def post_reading(reading: Reading):
        issues = validate_rate(reading.count_rate)
        if issues:
            raise HTTPException(status_code=422, detail=issues)
        db.insert_reading(
            path, reading.timestamp.isoformat(), reading.channel, reading.count_rate
        )
        return {"stored": True}

    @app.get("/readings")
    def get_readings(limit: int = 100, channel: int | None = None):
        return db.list_readings(path, limit=limit, channel=channel)

    @app.get("/gaps")
    def get_gaps(channel: int, max_gap_s: float = 5.0):
        stamps = [datetime.fromisoformat(t) for t in db.channel_timestamps(path, channel)]
        return find_gaps(stamps, max_gap_s)

    return app


app = create_app()
