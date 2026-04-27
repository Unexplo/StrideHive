"""Trend comparison and recovery summary tools for StrideHive."""

from __future__ import annotations

import statistics

from stridehive.server import mcp
from stridehive.data.mock import (
    get_athlete,
    get_health_metrics_for_athlete,
    get_sessions_for_athlete,
    get_all_health_metrics_for_athlete,
)

VALID_METRICS = ["resting_heart_rate", "steps", "calories_total", "sleep_hours", "hrv_ms"]

# Metrics where higher = better (for trend interpretation)
HIGHER_IS_BETTER = {"steps", "sleep_hours", "hrv_ms", "calories_total"}


@mcp.tool()
def compare_trends(
    athlete_id: str, metric: str, period1_days: int = 7, period2_days: int = 30
) -> dict:
    """Compare an athlete's recent metrics against a longer historical period.

    Useful for spotting improvement, regression, or stagnation over time.

    Args:
        athlete_id: The athlete's unique ID (e.g., 'athlete_001')
        metric: The metric to compare (resting_heart_rate, steps, calories_total, sleep_hours, hrv_ms)
        period1_days: Recent period in days (default: 7)
        period2_days: Historical period in days (default: 30)
    """
    if metric not in VALID_METRICS:
        return {"error": f"Invalid metric '{metric}'. Valid metrics: {', '.join(VALID_METRICS)}"}

    athlete = get_athlete(athlete_id)
    if not athlete:
        return {"error": f"Athlete '{athlete_id}' not found. Valid IDs: athlete_001, athlete_002, athlete_003"}

    all_data = get_health_metrics_for_athlete(athlete_id, metric=metric, days=period2_days)
    if len(all_data) < 3:
        return {"error": "Not enough data for trend comparison."}

    all_data.sort(key=lambda m: m["date"])

    recent_values = [r[metric] for r in all_data[-period1_days:] if metric in r]
    historical_values = [r[metric] for r in all_data if metric in r]

    if not recent_values or not historical_values:
        return {"error": "Not enough data points for the requested periods."}

    recent_mean = statistics.mean(recent_values)
    historical_mean = statistics.mean(historical_values)

    change_pct = ((recent_mean - historical_mean) / historical_mean * 100) if historical_mean != 0 else 0

    # Determine trend direction
    if metric in HIGHER_IS_BETTER:
        trend = "improving" if change_pct > 3 else ("declining" if change_pct < -3 else "stable")
    else:
        trend = "improving" if change_pct < -3 else ("declining" if change_pct > 3 else "stable")

    interpretation = _trend_interpretation(metric, change_pct, recent_mean, historical_mean, trend)

    return {
        "athlete": athlete["name"],
        "athlete_id": athlete_id,
        "metric": metric,
        "recent_period": {
            "days": period1_days,
            "mean": round(recent_mean, 1),
            "min": min(recent_values),
            "max": max(recent_values),
        },
        "historical_period": {
            "days": period2_days,
            "mean": round(historical_mean, 1),
            "min": min(historical_values),
            "max": max(historical_values),
        },
        "change_pct": round(change_pct, 1),
        "trend": trend,
        "interpretation": interpretation,
    }


@mcp.tool()
def get_recovery_summary(athlete_id: str) -> dict:
    """Get an overall recovery status summary for an athlete.

    Combines sleep quality, HRV trends, resting heart rate, and
    recent training load into a single recovery assessment with
    a 0-100 score and actionable recommendations.

    Args:
        athlete_id: The athlete's unique ID (e.g., 'athlete_001')
    """
    athlete = get_athlete(athlete_id)
    if not athlete:
        return {"error": f"Athlete '{athlete_id}' not found. Valid IDs: athlete_001, athlete_002, athlete_003"}

    recent_metrics = get_all_health_metrics_for_athlete(athlete_id, days=7)
    baseline_metrics = get_all_health_metrics_for_athlete(athlete_id, days=30)
    recent_sessions = get_sessions_for_athlete(athlete_id, limit=20)

    if not recent_metrics or not baseline_metrics:
        return {"error": "Not enough data for recovery summary."}

    recent_metrics.sort(key=lambda m: m["date"])
    baseline_metrics.sort(key=lambda m: m["date"])

    # --- HRV Trend (30% weight) ---
    recent_hrv = [m["hrv_ms"] for m in recent_metrics]
    baseline_hrv = [m["hrv_ms"] for m in baseline_metrics]
    hrv_recent_avg = statistics.mean(recent_hrv) if recent_hrv else 0
    hrv_baseline_avg = statistics.mean(baseline_hrv) if baseline_hrv else 0
    hrv_change_pct = ((hrv_recent_avg - hrv_baseline_avg) / hrv_baseline_avg * 100) if hrv_baseline_avg else 0

    # Score: 100 if same or better, drops as HRV declines
    hrv_score = max(0, min(100, 100 + hrv_change_pct * 3))
    hrv_detail = f"HRV {'up' if hrv_change_pct >= 0 else 'down'} {abs(hrv_change_pct):.0f}% from 30-day avg ({hrv_baseline_avg:.0f}ms -> {hrv_recent_avg:.0f}ms)"

    # --- Sleep Quality (25% weight) ---
    recent_sleep = [m["sleep_hours"] for m in recent_metrics]
    sleep_avg = statistics.mean(recent_sleep) if recent_sleep else 0
    sleep_quality_map = {"excellent": 100, "good": 75, "fair": 45, "poor": 20}
    quality_scores = [sleep_quality_map.get(m["sleep_quality"], 50) for m in recent_metrics]
    sleep_score = statistics.mean(quality_scores) if quality_scores else 50
    sleep_detail = f"Avg {sleep_avg:.1f}h sleep, mostly '{_most_common([m['sleep_quality'] for m in recent_metrics])}' quality"

    # --- Resting HR (20% weight) ---
    recent_rhr = [m["resting_heart_rate"] for m in recent_metrics]
    baseline_rhr = [m["resting_heart_rate"] for m in baseline_metrics]
    rhr_recent_avg = statistics.mean(recent_rhr) if recent_rhr else 0
    rhr_baseline_avg = statistics.mean(baseline_rhr) if baseline_rhr else 0
    rhr_change = rhr_recent_avg - rhr_baseline_avg

    # Score: 100 if same or lower, drops as HR rises
    rhr_score = max(0, min(100, 100 - rhr_change * 5))
    rhr_detail = f"Resting HR {'elevated' if rhr_change > 2 else 'normal'} at {rhr_recent_avg:.0f} bpm (baseline: {rhr_baseline_avg:.0f} bpm)"

    # --- Training Load (25% weight) ---
    last_7_sessions = [s for s in recent_sessions if s["date"] >= recent_metrics[0]["date"]]
    all_sessions_30d = [s for s in recent_sessions]
    recent_load_min = sum(s["duration_minutes"] for s in last_7_sessions)
    avg_weekly_load = sum(s["duration_minutes"] for s in all_sessions_30d) / 4.0 if all_sessions_30d else 0
    load_ratio = (recent_load_min / avg_weekly_load * 100) if avg_weekly_load else 100

    # Optimal is 80-120% of normal. Penalize over or under.
    if 80 <= load_ratio <= 120:
        load_score = 85
    elif load_ratio > 120:
        load_score = max(0, 85 - (load_ratio - 120) * 1.5)
    else:
        load_score = max(0, 85 - (80 - load_ratio) * 1.0)
    load_detail = f"{load_ratio:.0f}% of typical weekly training volume"

    # --- Composite Score ---
    recovery_score = round(
        hrv_score * 0.30
        + sleep_score * 0.25
        + rhr_score * 0.20
        + load_score * 0.25
    )
    recovery_score = max(0, min(100, recovery_score))

    if recovery_score > 70:
        status = "well_recovered"
    elif recovery_score > 40:
        status = "moderate"
    else:
        status = "fatigued"

    # Recommendations
    recommendations = _build_recommendations(
        status, hrv_change_pct, sleep_avg, rhr_change, load_ratio
    )

    result: dict = {
        "athlete": athlete["name"],
        "athlete_id": athlete_id,
        "recovery_score": recovery_score,
        "status": status,
        "factors": {
            "hrv_trend": {"score": round(hrv_score), "weight": "30%", "detail": hrv_detail},
            "sleep_quality": {"score": round(sleep_score), "weight": "25%", "detail": sleep_detail},
            "resting_hr": {"score": round(rhr_score), "weight": "20%", "detail": rhr_detail},
            "training_load": {"score": round(load_score), "weight": "25%", "detail": load_detail},
        },
        "recommendations": recommendations,
    }

    # Add gait status for athlete_001
    if athlete_id == "athlete_001":
        sessions = get_sessions_for_athlete(athlete_id, limit=20)
        gait_sessions = [s for s in sessions if "gait_asymmetry_pct" in s]
        if gait_sessions:
            gait_sessions.sort(key=lambda s: s["date"])
            current = gait_sessions[-1]["gait_asymmetry_pct"]
            oldest = gait_sessions[0]["gait_asymmetry_pct"]
            trend = "improving" if current < oldest else ("worsening" if current > oldest else "stable")
            result["gait_status"] = {
                "current_asymmetry_pct": current,
                "trend": trend,
                "period_start_pct": oldest,
                "note": f"Gait asymmetry {'improving' if trend == 'improving' else 'needs attention'} from {oldest}% to {current}%. Target: <5%.",
            }

    return result


def _trend_interpretation(metric: str, change_pct: float, recent: float, historical: float, trend: str) -> str:
    """Generate human-readable trend interpretation."""
    labels = {
        "resting_heart_rate": "Resting heart rate",
        "steps": "Daily steps",
        "calories_total": "Daily calories",
        "sleep_hours": "Sleep duration",
        "hrv_ms": "Heart rate variability",
    }
    label = labels.get(metric, metric)
    direction = "increased" if change_pct > 0 else "decreased"

    if trend == "stable":
        return f"{label} is stable at {recent:.1f} (30-day avg: {historical:.1f})."
    elif trend == "improving":
        return f"{label} has {direction} {abs(change_pct):.1f}% — trending in the right direction."
    else:
        return f"{label} has {direction} {abs(change_pct):.1f}% in the last week compared to the 30-day average. This may warrant attention."


def _most_common(values: list[str]) -> str:
    """Return the most common value in a list."""
    if not values:
        return "unknown"
    return max(set(values), key=values.count)


def _build_recommendations(
    status: str, hrv_change: float, sleep_avg: float, rhr_change: float, load_ratio: float
) -> list[str]:
    """Build actionable recommendations based on recovery factors."""
    recs = []

    if status == "fatigued":
        recs.append("Consider reducing training intensity for 2-3 days.")
    elif status == "moderate":
        recs.append("Monitor closely — avoid increasing training load this week.")

    if hrv_change < -10:
        recs.append("HRV is trending down significantly. If this continues, consult coaching staff.")

    if sleep_avg < 7.0:
        recs.append(f"Sleep averaging {sleep_avg:.1f}h — aim for 8+ hours for optimal recovery.")

    if rhr_change > 5:
        recs.append("Resting heart rate is elevated. Rule out illness or external stress.")

    if load_ratio > 140:
        recs.append("Training volume is significantly above normal. Risk of overtraining.")
    elif load_ratio < 60:
        recs.append("Training volume is low. Gradual increase recommended if healthy.")

    if not recs:
        recs.append("All metrics look healthy. Maintain current routine.")

    return recs
