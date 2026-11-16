"""Fake detector: posts one reading per channel per tick, with occasional dropouts and bad values."""
import os
import random
import time
from datetime import datetime, timezone

import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
INTERVAL_S = float(os.environ.get("INTERVAL_S", "1"))
CHANNELS = int(os.environ.get("CHANNELS", "4"))
DROPOUT_P = 0.05  # chance a reading is never sent
BAD_VALUE_P = 0.03  # chance a reading has an impossible value


def make_reading(channel: int, rng: random.Random) -> dict | None:
    """Return a reading dict, or None to simulate a dropout."""
    if rng.random() < DROPOUT_P:
        return None
    rate = max(0.0, rng.gauss(120.0, 10.0))
    if rng.random() < BAD_VALUE_P:
        rate = rng.choice([-5.0, 5000.0])
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "count_rate": rate,
    }


def main() -> None:
    rng = random.Random()
    with httpx.Client(base_url=API_URL, timeout=5) as client:
        while True:
            for channel in range(CHANNELS):
                reading = make_reading(channel, rng)
                if reading is None:
                    continue
                try:
                    resp = client.post("/readings", json=reading)
                    if resp.status_code != 201:
                        print("rejected", reading, resp.json())
                except httpx.HTTPError as exc:
                    print("API not reachable:", exc)
            time.sleep(INTERVAL_S)


if __name__ == "__main__":
    main()
