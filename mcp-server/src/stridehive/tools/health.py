"""Health metrics and anomaly detection tools for StrideHive."""

from __future__ import annotations

import statistics

from stridehive.server import mcp
from stridehive.data.mock import (
    get_athlete,
    get_health_metrics_for_athlete,
    get_sessions_for_athlete,
)

VALID_METRICS = ["resting_heart_rate", "steps", "calories_total", "sleep_hours", "hrv_ms"]


@mcp.tool()
def get_health_metrics(athlete_id: str, metric: str, days: int = 7) -> dict:
    """Get daily health metrics for an athlete over a time period.

    Supported metrics: resting_heart_rate, steps, calories_total, sleep_hours, hrv_ms

    Args:
        athlete_id: The athlete's unique ID (e.g., 'athlete_001')
        metric: The metric to retrieve (resting_heart_rate, steps, calories_total, sleep_hours, hrv_ms)
        days: Number of days of history to return (default: 7)
    """
    if metric not in VALID_METRICS:
        return {"error": f"Invalid metric '{metric}'. Valid metrics: {', '.join(VALID_METRICS)}"}

    athlete = get_athlete(athlete_id)
    if not athlete:
        return {"error": f"Athlete '{athlete_id}' not found. Valid IDs: athlete_001, athlete_002, athlete_003"}

    data = get_health_metrics_for_athlete(athlete_id, metric=metric, days=days)
    return {
        "athlete": athlete["name"],
        "athlete_id": athlete_id,
        "metric": metric,
        "days": days,
        "data_points": len(data),
        "values": data,
    }


@mcp.tool()
def get_anomalies(athlete_id: str, days: int = 7) -> dict:
    """Detect anomalies in an athlete's recent health data.

    Checks for unusual patterns: heart rate spikes, HRV drops,
    sleep disruption, and (for rehab athletes) gait asymmetry changes.
    Compares the recent period against a 14-day baseline.

    Args:
        athlete_id: The athlete's unique ID (e.g., 'athlete_001')
        days: Number of recent days to analyze (default: 7)
    """
    athlete = get_athlete(athlete_id)
    if not athlete:
        return {"error": f"Athlete '{athlete_id}' not found. Valid IDs: athlete_001, athlete_002, athlete_003"}

    # Get recent + baseline data
    all_data = get_health_metrics_for_athlete(athlete_id, days=days + 14)
    if len(all_data) < 3:
        return {"athlete": athlete["name"], "anomalies": [], "message": "Not enough data for analysis."}

    # Split into recent and baseline
    all_data.sort(key=lambda m: m["date"])
    recent = all_data[-days:] if len(all_data) >= days else all_data
    baseline = all_data[:-days] if len(all_data) > days else []

    anomalies = []

    if len(baseline) >= 3:
        for metric_key in ["resting_heart_rate", "hrv_ms", "sleep_hours"]:
            baseline_values = [r[metric_key] for r in baseline if metric_key in r]
            if len(baseline_values) < 3:
                continue

            bl_mean = statistics.mean(baseline_values)
            bl_stdev = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 0

            for day_record in recent:
                value = day_record.get(metric_key)
                if value is None:
                    continue

                deviation = abs(value - bl_mean)
                threshold = max(bl_stdev * 1.5, 1)
                is_anomaly = deviation > threshold

                # Also apply hard thresholds
                if metric_key == "resting_heart_rate" and value > bl_mean + 10:
                    is_anomaly = True
                elif metric_key == "hrv_ms" and value < bl_mean - 15:
                    is_anomaly = True
                elif metric_key == "sleep_hours" and value < 5.5:
                    is_anomaly = True

                if is_anomaly:
                    severity = "high" if deviation > threshold * 2 else "medium"
                    direction = "above" if value > bl_mean else "below"
                    anomalies.append({
                        "date": day_record["date"],
                        "metric": metric_key,
                        "value": value,
                        "baseline_avg": round(bl_mean, 1),
                        "severity": severity,
                        "message": _anomaly_message(metric_key, value, bl_mean, direction),
                    })

    # Check gait asymmetry for athlete_001
    if athlete_id == "athlete_001":
        sessions = get_sessions_for_athlete(athlete_id, limit=days + 5)
        sessions.sort(key=lambda s: s["date"])
        for i in range(1, len(sessions)):
            prev = sessions[i - 1].get("gait_asymmetry_pct")
            curr = sessions[i].get("gait_asymmetry_pct")
            if prev is not None and curr is not None and curr - prev > 3.0:
                anomalies.append({
                    "date": sessions[i]["date"],
                    "metric": "gait_asymmetry_pct",
                    "value": curr,
                    "previous_value": prev,
                    "severity": "high",
                    "message": f"Gait asymmetry jumped from {prev}% to {curr}% — possible compensation or setback.",
                })

    anomalies.sort(key=lambda a: a["date"], reverse=True)

    return {
        "athlete": athlete["name"],
        "athlete_id": athlete_id,
        "analysis_days": days,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }


def _anomaly_message(metric: str, value: float, baseline: float, direction: str) -> str:
    """Generate a human-readable anomaly message."""
    labels = {
        "resting_heart_rate": ("Resting HR", "bpm"),
        "hrv_ms": ("HRV", "ms"),
        "sleep_hours": ("Sleep", "hours"),
    }
    label, unit = labels.get(metric, (metric, ""))

    if metric == "resting_heart_rate" and direction == "above":
        return f"{label} elevated to {value} {unit} (baseline avg: {baseline:.0f} {unit}) — possible fatigue or illness."
    elif metric == "hrv_ms" and direction == "below":
        return f"{label} dropped to {value} {unit} (baseline avg: {baseline:.0f} {unit}) — possible overreaching or stress."
    elif metric == "sleep_hours" and direction == "below":
        return f"{label} at {value} {unit} (baseline avg: {baseline:.1f} {unit}) — insufficient recovery."
    else:
        return f"{label} at {value} {unit} is {direction} baseline avg of {baseline:.1f} {unit}."
