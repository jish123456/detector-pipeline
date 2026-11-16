from datetime import datetime

MIN_RATE = 0.0
MAX_RATE = 1000.0


def validate_rate(count_rate: float) -> list[str]:
    """Return a list of problems with a count rate (empty list means valid)."""
    issues = []
    if count_rate < MIN_RATE:
        issues.append(f"count_rate {count_rate} is below {MIN_RATE}")
    if count_rate > MAX_RATE:
        issues.append(f"count_rate {count_rate} is above {MAX_RATE}")
    return issues


def find_gaps(timestamps: list[datetime], max_gap_s: float) -> list[dict]:
    """Return the spans where consecutive readings are further apart than max_gap_s."""
    ordered = sorted(timestamps)
    gaps = []
    for earlier, later in zip(ordered, ordered[1:]):
        seconds = (later - earlier).total_seconds()
        if seconds > max_gap_s:
            gaps.append(
                {
                    "start": earlier.isoformat(),
                    "end": later.isoformat(),
                    "seconds": seconds,
                }
            )
    return gaps
