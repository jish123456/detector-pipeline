from datetime import datetime, timedelta

from app.validation import find_gaps, validate_rate


def test_valid_rate_has_no_issues():
    assert validate_rate(120.0) == []


def test_negative_rate_is_rejected():
    assert len(validate_rate(-1.0)) == 1


def test_too_large_rate_is_rejected():
    assert len(validate_rate(5000.0)) == 1


def test_find_gaps_detects_missing_readings():
    t0 = datetime(2026, 1, 1, 12, 0, 0)
    stamps = [t0, t0 + timedelta(seconds=1), t0 + timedelta(seconds=20)]
    gaps = find_gaps(stamps, max_gap_s=5)
    assert len(gaps) == 1
    assert gaps[0]["seconds"] == 19


def test_find_gaps_empty_when_regular():
    t0 = datetime(2026, 1, 1, 12, 0, 0)
    stamps = [t0 + timedelta(seconds=i) for i in range(5)]
    assert find_gaps(stamps, max_gap_s=5) == []


def test_find_gaps_handles_unsorted_input():
    t0 = datetime(2026, 1, 1, 12, 0, 0)
    stamps = [t0 + timedelta(seconds=30), t0]
    assert len(find_gaps(stamps, max_gap_s=5)) == 1
