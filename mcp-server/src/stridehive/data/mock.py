"""Mock data for StrideHive MCP server.

Contains 3 athletes with 30 days of health metrics and training sessions.
All dates are computed relative to today so data always looks current.

Baked-in anomalies:
- athlete_001 (Alex): Gait asymmetry spike + resting HR spike on day 15
- athlete_002 (Jordan): HRV/sleep drop on days 20-23 (stress/overreaching)
- athlete_003 (Sam): Overtraining last 7 days — rising resting HR, dropping HRV
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

_TODAY = date.today()


def _d(days_ago: int) -> str:
    """Return ISO date string for N days ago."""
    return (_TODAY - timedelta(days=days_ago)).isoformat()


# ---------------------------------------------------------------------------
# Athletes
# ---------------------------------------------------------------------------

ATHLETES: dict[str, dict[str, Any]] = {
    "athlete_001": {
        "id": "athlete_001",
        "name": "Alex Rivera",
        "age": 28,
        "sport": "Running",
        "injury_history": "ACL reconstruction (left knee) - 4 months post-op",
        "coach": "Dr. Sarah Kim (Physio)",
    },
    "athlete_002": {
        "id": "athlete_002",
        "name": "Jordan Chen",
        "age": 34,
        "sport": "Strength Training",
        "injury_history": "None",
        "coach": "Marcus Webb (PT)",
    },
    "athlete_003": {
        "id": "athlete_003",
        "name": "Sam Okafor",
        "age": 19,
        "sport": "Soccer",
        "injury_history": "Mild hamstring strain (resolved)",
        "coach": "Academy Staff",
    },
}

# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

SESSIONS: list[dict[str, Any]] = [
    # ── Alex Rivera (athlete_001) — ACL rehab progression ──
    {
        "session_id": "sess_001_01",
        "athlete_id": "athlete_001",
        "date": _d(28),
        "type": "rehab",
        "duration_minutes": 40,
        "distance_km": 0.0,
        "calories_burned": 160,
        "avg_heart_rate": 105,
        "max_heart_rate": 128,
        "heart_rate_zones": {"zone1_recovery": 20, "zone2_fat_burn": 15, "zone3_cardio": 5, "zone4_threshold": 0, "zone5_max": 0},
        "notes": "Initial quad activation drills, single-leg balance work",
        "gait_asymmetry_pct": 12.1,
        "left_stride_length_cm": 62,
        "right_stride_length_cm": 71,
    },
    {
        "session_id": "sess_001_02",
        "athlete_id": "athlete_001",
        "date": _d(26),
        "type": "rehab",
        "duration_minutes": 45,
        "distance_km": 0.0,
        "calories_burned": 175,
        "avg_heart_rate": 108,
        "max_heart_rate": 132,
        "heart_rate_zones": {"zone1_recovery": 18, "zone2_fat_burn": 18, "zone3_cardio": 7, "zone4_threshold": 2, "zone5_max": 0},
        "notes": "Step-ups, leg press progression. Feeling more confident.",
        "gait_asymmetry_pct": 11.3,
        "left_stride_length_cm": 63,
        "right_stride_length_cm": 71,
    },
    {
        "session_id": "sess_001_03",
        "athlete_id": "athlete_001",
        "date": _d(23),
        "type": "rehab",
        "duration_minutes": 50,
        "distance_km": 0.5,
        "calories_burned": 210,
        "avg_heart_rate": 115,
        "max_heart_rate": 140,
        "heart_rate_zones": {"zone1_recovery": 15, "zone2_fat_burn": 20, "zone3_cardio": 10, "zone4_threshold": 5, "zone5_max": 0},
        "notes": "First treadmill walk. Slow pace, focus on symmetry.",
        "gait_asymmetry_pct": 10.2,
        "left_stride_length_cm": 65,
        "right_stride_length_cm": 72,
    },
    {
        "session_id": "sess_001_04",
        "athlete_id": "athlete_001",
        "date": _d(20),
        "type": "running",
        "duration_minutes": 25,
        "distance_km": 2.0,
        "calories_burned": 230,
        "avg_heart_rate": 132,
        "max_heart_rate": 155,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 8, "zone3_cardio": 8, "zone4_threshold": 4, "zone5_max": 0},
        "notes": "Light jog. Knee felt stable. Slight compensation noticed.",
        "gait_asymmetry_pct": 9.5,
        "left_stride_length_cm": 66,
        "right_stride_length_cm": 73,
    },
    {
        "session_id": "sess_001_05",
        "athlete_id": "athlete_001",
        "date": _d(17),
        "type": "rehab",
        "duration_minutes": 45,
        "distance_km": 0.0,
        "calories_burned": 185,
        "avg_heart_rate": 110,
        "max_heart_rate": 135,
        "heart_rate_zones": {"zone1_recovery": 15, "zone2_fat_burn": 20, "zone3_cardio": 8, "zone4_threshold": 2, "zone5_max": 0},
        "notes": "Good session. Single-leg squat depth improving.",
        "gait_asymmetry_pct": 8.8,
        "left_stride_length_cm": 67,
        "right_stride_length_cm": 73,
    },
    # Day 15 — BAD DAY: asymmetry spike + elevated HR
    {
        "session_id": "sess_001_06",
        "athlete_id": "athlete_001",
        "date": _d(15),
        "type": "running",
        "duration_minutes": 30,
        "distance_km": 2.5,
        "calories_burned": 280,
        "avg_heart_rate": 145,
        "max_heart_rate": 172,
        "heart_rate_zones": {"zone1_recovery": 2, "zone2_fat_burn": 5, "zone3_cardio": 10, "zone4_threshold": 10, "zone5_max": 3},
        "notes": "Pushed too hard. Knee swelling after. Physio flagged.",
        "gait_asymmetry_pct": 11.0,
        "left_stride_length_cm": 63,
        "right_stride_length_cm": 71,
    },
    {
        "session_id": "sess_001_07",
        "athlete_id": "athlete_001",
        "date": _d(12),
        "type": "rehab",
        "duration_minutes": 35,
        "distance_km": 0.0,
        "calories_burned": 140,
        "avg_heart_rate": 100,
        "max_heart_rate": 120,
        "heart_rate_zones": {"zone1_recovery": 25, "zone2_fat_burn": 10, "zone3_cardio": 0, "zone4_threshold": 0, "zone5_max": 0},
        "notes": "Recovery session. Light mobility and ice. Swelling down.",
        "gait_asymmetry_pct": 8.5,
        "left_stride_length_cm": 66,
        "right_stride_length_cm": 72,
    },
    {
        "session_id": "sess_001_08",
        "athlete_id": "athlete_001",
        "date": _d(9),
        "type": "running",
        "duration_minutes": 30,
        "distance_km": 2.8,
        "calories_burned": 250,
        "avg_heart_rate": 128,
        "max_heart_rate": 148,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 10, "zone4_threshold": 5, "zone5_max": 0},
        "notes": "Controlled pace. Gait looking better.",
        "gait_asymmetry_pct": 7.2,
        "left_stride_length_cm": 68,
        "right_stride_length_cm": 73,
    },
    {
        "session_id": "sess_001_09",
        "athlete_id": "athlete_001",
        "date": _d(6),
        "type": "rehab",
        "duration_minutes": 50,
        "distance_km": 0.0,
        "calories_burned": 200,
        "avg_heart_rate": 112,
        "max_heart_rate": 138,
        "heart_rate_zones": {"zone1_recovery": 15, "zone2_fat_burn": 22, "zone3_cardio": 10, "zone4_threshold": 3, "zone5_max": 0},
        "notes": "Plyometric intro. Box jumps (low). Feeling strong.",
        "gait_asymmetry_pct": 6.8,
        "left_stride_length_cm": 69,
        "right_stride_length_cm": 74,
    },
    {
        "session_id": "sess_001_10",
        "athlete_id": "athlete_001",
        "date": _d(4),
        "type": "running",
        "duration_minutes": 35,
        "distance_km": 3.5,
        "calories_burned": 300,
        "avg_heart_rate": 130,
        "max_heart_rate": 150,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 12, "zone4_threshold": 6, "zone5_max": 2},
        "notes": "Longest run since surgery. Great symmetry.",
        "gait_asymmetry_pct": 6.2,
        "left_stride_length_cm": 70,
        "right_stride_length_cm": 74,
    },
    {
        "session_id": "sess_001_11",
        "athlete_id": "athlete_001",
        "date": _d(2),
        "type": "rehab",
        "duration_minutes": 45,
        "distance_km": 0.0,
        "calories_burned": 190,
        "avg_heart_rate": 110,
        "max_heart_rate": 135,
        "heart_rate_zones": {"zone1_recovery": 15, "zone2_fat_burn": 20, "zone3_cardio": 8, "zone4_threshold": 2, "zone5_max": 0},
        "notes": "Strength circuit. Leg press at 80% of pre-op max.",
        "gait_asymmetry_pct": 5.8,
        "left_stride_length_cm": 71,
        "right_stride_length_cm": 75,
    },
    {
        "session_id": "sess_001_12",
        "athlete_id": "athlete_001",
        "date": _d(0),
        "type": "running",
        "duration_minutes": 30,
        "distance_km": 3.2,
        "calories_burned": 275,
        "avg_heart_rate": 126,
        "max_heart_rate": 146,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 10, "zone4_threshold": 5, "zone5_max": 0},
        "notes": "Easy run. Feeling confident. Target: sub-6% asymmetry.",
        "gait_asymmetry_pct": 5.5,
        "left_stride_length_cm": 71,
        "right_stride_length_cm": 75,
    },

    # ── Jordan Chen (athlete_002) — Consistent strength training ──
    {
        "session_id": "sess_002_01",
        "athlete_id": "athlete_002",
        "date": _d(28),
        "type": "strength",
        "duration_minutes": 60,
        "distance_km": 0.0,
        "calories_burned": 420,
        "avg_heart_rate": 125,
        "max_heart_rate": 158,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 20, "zone4_threshold": 12, "zone5_max": 3},
        "notes": "Push day — bench, OHP, dips. Hit PR on bench: 105kg.",
    },
    {
        "session_id": "sess_002_02",
        "athlete_id": "athlete_002",
        "date": _d(26),
        "type": "strength",
        "duration_minutes": 55,
        "distance_km": 0.0,
        "calories_burned": 390,
        "avg_heart_rate": 120,
        "max_heart_rate": 152,
        "heart_rate_zones": {"zone1_recovery": 12, "zone2_fat_burn": 18, "zone3_cardio": 15, "zone4_threshold": 8, "zone5_max": 2},
        "notes": "Pull day — deadlifts, rows, pull-ups. Solid volume.",
    },
    {
        "session_id": "sess_002_03",
        "athlete_id": "athlete_002",
        "date": _d(24),
        "type": "strength",
        "duration_minutes": 50,
        "distance_km": 0.0,
        "calories_burned": 360,
        "avg_heart_rate": 118,
        "max_heart_rate": 148,
        "heart_rate_zones": {"zone1_recovery": 12, "zone2_fat_burn": 18, "zone3_cardio": 12, "zone4_threshold": 6, "zone5_max": 2},
        "notes": "Leg day — squats, lunges, leg curl. Volume on track.",
    },
    # Days 22-20: stress period — missed sessions, elevated HR
    {
        "session_id": "sess_002_04",
        "athlete_id": "athlete_002",
        "date": _d(20),
        "type": "strength",
        "duration_minutes": 35,
        "distance_km": 0.0,
        "calories_burned": 240,
        "avg_heart_rate": 138,
        "max_heart_rate": 170,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 8, "zone3_cardio": 10, "zone4_threshold": 8, "zone5_max": 4},
        "notes": "Cut short. Felt off. Heart rate unusually high for the load.",
    },
    {
        "session_id": "sess_002_05",
        "athlete_id": "athlete_002",
        "date": _d(17),
        "type": "strength",
        "duration_minutes": 60,
        "distance_km": 0.0,
        "calories_burned": 400,
        "avg_heart_rate": 122,
        "max_heart_rate": 155,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 18, "zone3_cardio": 18, "zone4_threshold": 10, "zone5_max": 4},
        "notes": "Back to normal. Push day. Feeling recovered.",
    },
    {
        "session_id": "sess_002_06",
        "athlete_id": "athlete_002",
        "date": _d(14),
        "type": "strength",
        "duration_minutes": 65,
        "distance_km": 0.0,
        "calories_burned": 440,
        "avg_heart_rate": 124,
        "max_heart_rate": 160,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 22, "zone4_threshold": 14, "zone5_max": 4},
        "notes": "Pull day. Deadlift felt great. 180kg x 3.",
    },
    {
        "session_id": "sess_002_07",
        "athlete_id": "athlete_002",
        "date": _d(11),
        "type": "strength",
        "duration_minutes": 55,
        "distance_km": 0.0,
        "calories_burned": 380,
        "avg_heart_rate": 120,
        "max_heart_rate": 150,
        "heart_rate_zones": {"zone1_recovery": 12, "zone2_fat_burn": 18, "zone3_cardio": 15, "zone4_threshold": 8, "zone5_max": 2},
        "notes": "Leg day. Squats at 140kg. Good depth.",
    },
    {
        "session_id": "sess_002_08",
        "athlete_id": "athlete_002",
        "date": _d(8),
        "type": "strength",
        "duration_minutes": 60,
        "distance_km": 0.0,
        "calories_burned": 410,
        "avg_heart_rate": 123,
        "max_heart_rate": 156,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 16, "zone3_cardio": 20, "zone4_threshold": 10, "zone5_max": 4},
        "notes": "Push day. OHP at 70kg. Bench 100kg x 8.",
    },
    {
        "session_id": "sess_002_09",
        "athlete_id": "athlete_002",
        "date": _d(5),
        "type": "strength",
        "duration_minutes": 55,
        "distance_km": 0.0,
        "calories_burned": 385,
        "avg_heart_rate": 121,
        "max_heart_rate": 153,
        "heart_rate_zones": {"zone1_recovery": 12, "zone2_fat_burn": 17, "zone3_cardio": 16, "zone4_threshold": 8, "zone5_max": 2},
        "notes": "Pull day. Good consistency this week.",
    },
    {
        "session_id": "sess_002_10",
        "athlete_id": "athlete_002",
        "date": _d(2),
        "type": "strength",
        "duration_minutes": 60,
        "distance_km": 0.0,
        "calories_burned": 420,
        "avg_heart_rate": 124,
        "max_heart_rate": 158,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 20, "zone4_threshold": 12, "zone5_max": 3},
        "notes": "Leg day. New PR on squat: 145kg.",
    },

    # ── Sam Okafor (athlete_003) — Overtraining buildup ──
    {
        "session_id": "sess_003_01",
        "athlete_id": "athlete_003",
        "date": _d(29),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 9.5,
        "calories_burned": 680,
        "avg_heart_rate": 148,
        "max_heart_rate": 185,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 30, "zone4_threshold": 30, "zone5_max": 15},
        "notes": "Full team training. Good intensity.",
    },
    {
        "session_id": "sess_003_02",
        "athlete_id": "athlete_003",
        "date": _d(27),
        "type": "strength",
        "duration_minutes": 45,
        "distance_km": 0.0,
        "calories_burned": 320,
        "avg_heart_rate": 115,
        "max_heart_rate": 145,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 12, "zone4_threshold": 6, "zone5_max": 2},
        "notes": "Gym session. Lower body focus.",
    },
    {
        "session_id": "sess_003_03",
        "athlete_id": "athlete_003",
        "date": _d(25),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 10.2,
        "calories_burned": 710,
        "avg_heart_rate": 150,
        "max_heart_rate": 188,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 8, "zone3_cardio": 28, "zone4_threshold": 32, "zone5_max": 17},
        "notes": "Match simulation. High intensity.",
    },
    {
        "session_id": "sess_003_04",
        "athlete_id": "athlete_003",
        "date": _d(22),
        "type": "recovery",
        "duration_minutes": 30,
        "distance_km": 2.0,
        "calories_burned": 150,
        "avg_heart_rate": 105,
        "max_heart_rate": 120,
        "heart_rate_zones": {"zone1_recovery": 20, "zone2_fat_burn": 10, "zone3_cardio": 0, "zone4_threshold": 0, "zone5_max": 0},
        "notes": "Light jog and stretching. Rest day.",
    },
    {
        "session_id": "sess_003_05",
        "athlete_id": "athlete_003",
        "date": _d(20),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 9.8,
        "calories_burned": 690,
        "avg_heart_rate": 146,
        "max_heart_rate": 183,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 30, "zone4_threshold": 30, "zone5_max": 15},
        "notes": "Tactical session. Position drills.",
    },
    {
        "session_id": "sess_003_06",
        "athlete_id": "athlete_003",
        "date": _d(18),
        "type": "strength",
        "duration_minutes": 50,
        "distance_km": 0.0,
        "calories_burned": 340,
        "avg_heart_rate": 118,
        "max_heart_rate": 148,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 15, "zone4_threshold": 8, "zone5_max": 2},
        "notes": "Upper body and core. Good session.",
    },
    {
        "session_id": "sess_003_07",
        "athlete_id": "athlete_003",
        "date": _d(15),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 10.0,
        "calories_burned": 700,
        "avg_heart_rate": 149,
        "max_heart_rate": 186,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 8, "zone3_cardio": 28, "zone4_threshold": 32, "zone5_max": 17},
        "notes": "Inter-squad match. Played full 90.",
    },
    {
        "session_id": "sess_003_08",
        "athlete_id": "athlete_003",
        "date": _d(12),
        "type": "soccer",
        "duration_minutes": 75,
        "distance_km": 8.5,
        "calories_burned": 580,
        "avg_heart_rate": 142,
        "max_heart_rate": 178,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 12, "zone3_cardio": 25, "zone4_threshold": 22, "zone5_max": 11},
        "notes": "Technical session. Slightly shorter.",
    },
    {
        "session_id": "sess_003_09",
        "athlete_id": "athlete_003",
        "date": _d(10),
        "type": "strength",
        "duration_minutes": 45,
        "distance_km": 0.0,
        "calories_burned": 310,
        "avg_heart_rate": 116,
        "max_heart_rate": 142,
        "heart_rate_zones": {"zone1_recovery": 10, "zone2_fat_burn": 15, "zone3_cardio": 12, "zone4_threshold": 6, "zone5_max": 2},
        "notes": "Legs and core. Hamstring feeling good.",
    },
    # Last 7 days — overtraining begins (high frequency, double sessions)
    {
        "session_id": "sess_003_10",
        "athlete_id": "athlete_003",
        "date": _d(6),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 10.5,
        "calories_burned": 720,
        "avg_heart_rate": 152,
        "max_heart_rate": 190,
        "heart_rate_zones": {"zone1_recovery": 3, "zone2_fat_burn": 7, "zone3_cardio": 25, "zone4_threshold": 35, "zone5_max": 20},
        "notes": "Pre-match training. Very high intensity.",
    },
    {
        "session_id": "sess_003_11",
        "athlete_id": "athlete_003",
        "date": _d(6),
        "type": "strength",
        "duration_minutes": 40,
        "distance_km": 0.0,
        "calories_burned": 280,
        "avg_heart_rate": 122,
        "max_heart_rate": 150,
        "heart_rate_zones": {"zone1_recovery": 8, "zone2_fat_burn": 12, "zone3_cardio": 12, "zone4_threshold": 6, "zone5_max": 2},
        "notes": "PM gym session. Double day.",
    },
    {
        "session_id": "sess_003_12",
        "athlete_id": "athlete_003",
        "date": _d(5),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 10.8,
        "calories_burned": 740,
        "avg_heart_rate": 155,
        "max_heart_rate": 192,
        "heart_rate_zones": {"zone1_recovery": 2, "zone2_fat_burn": 5, "zone3_cardio": 22, "zone4_threshold": 38, "zone5_max": 23},
        "notes": "Match day. Full 90 minutes. Felt heavy legs at 70min.",
    },
    {
        "session_id": "sess_003_13",
        "athlete_id": "athlete_003",
        "date": _d(4),
        "type": "soccer",
        "duration_minutes": 75,
        "distance_km": 8.0,
        "calories_burned": 550,
        "avg_heart_rate": 148,
        "max_heart_rate": 182,
        "heart_rate_zones": {"zone1_recovery": 5, "zone2_fat_burn": 10, "zone3_cardio": 25, "zone4_threshold": 25, "zone5_max": 10},
        "notes": "Recovery match. Coach said take it easy but still ran hard.",
    },
    {
        "session_id": "sess_003_14",
        "athlete_id": "athlete_003",
        "date": _d(3),
        "type": "strength",
        "duration_minutes": 50,
        "distance_km": 0.0,
        "calories_burned": 350,
        "avg_heart_rate": 125,
        "max_heart_rate": 155,
        "heart_rate_zones": {"zone1_recovery": 8, "zone2_fat_burn": 12, "zone3_cardio": 15, "zone4_threshold": 10, "zone5_max": 5},
        "notes": "Full body session. Felt sluggish.",
    },
    {
        "session_id": "sess_003_15",
        "athlete_id": "athlete_003",
        "date": _d(1),
        "type": "soccer",
        "duration_minutes": 90,
        "distance_km": 9.2,
        "calories_burned": 650,
        "avg_heart_rate": 153,
        "max_heart_rate": 189,
        "heart_rate_zones": {"zone1_recovery": 3, "zone2_fat_burn": 7, "zone3_cardio": 25, "zone4_threshold": 35, "zone5_max": 20},
        "notes": "Team training. Legs feeling heavy. Cramped at 80min.",
    },
    {
        "session_id": "sess_003_16",
        "athlete_id": "athlete_003",
        "date": _d(0),
        "type": "soccer",
        "duration_minutes": 60,
        "distance_km": 6.5,
        "calories_burned": 450,
        "avg_heart_rate": 150,
        "max_heart_rate": 185,
        "heart_rate_zones": {"zone1_recovery": 3, "zone2_fat_burn": 7, "zone3_cardio": 20, "zone4_threshold": 20, "zone5_max": 10},
        "notes": "Asked to come off at 60min. Feeling fatigued.",
    },
]

# ---------------------------------------------------------------------------
# Health Metrics (30 days per athlete)
# ---------------------------------------------------------------------------


def _build_health_metrics() -> list[dict[str, Any]]:
    """Build 30 days of health metrics for all 3 athletes."""
    metrics: list[dict[str, Any]] = []

    for day in range(30):
        # ── Alex Rivera (athlete_001) ──
        # Baseline: resting HR ~62, HRV ~48, sleep ~7.5h
        # Day 15: spike — HR 82, HRV 33
        rhr_001 = 62
        hrv_001 = 48
        sleep_001 = 7.5
        sleep_q_001 = "good"
        steps_001 = 8500
        cals_001 = 2200

        if day == 15:
            rhr_001 = 82
            hrv_001 = 33
            sleep_001 = 5.5
            sleep_q_001 = "poor"
        elif day == 14:
            rhr_001 = 70
            hrv_001 = 40
            sleep_001 = 6.2
            sleep_q_001 = "fair"
        elif day == 16:
            rhr_001 = 68
            hrv_001 = 42
            sleep_001 = 6.8
            sleep_q_001 = "fair"
        elif day <= 5:
            # Recent improvement
            rhr_001 = 60 + (day % 3)
            hrv_001 = 50 + (day % 4)
            sleep_001 = 7.5 + (day % 2) * 0.3
            sleep_q_001 = "good"
            steps_001 = 9000 + day * 100
        elif day <= 12:
            rhr_001 = 63 + (day % 3)
            hrv_001 = 46 + (day % 5)
            sleep_001 = 7.2 + (day % 3) * 0.2
        else:
            rhr_001 = 64 + (day % 4)
            hrv_001 = 45 + (day % 5)
            sleep_001 = 7.0 + (day % 3) * 0.3

        metrics.append({
            "date": _d(day),
            "athlete_id": "athlete_001",
            "resting_heart_rate": rhr_001,
            "steps": steps_001,
            "calories_total": cals_001,
            "sleep_hours": round(sleep_001, 1),
            "sleep_quality": sleep_q_001,
            "hrv_ms": hrv_001,
        })

        # ── Jordan Chen (athlete_002) ──
        # Baseline: resting HR ~65, HRV ~55, sleep ~7.5h
        # Days 20-23: HRV drops to ~32, sleep drops to ~5h
        rhr_002 = 65
        hrv_002 = 55
        sleep_002 = 7.5
        sleep_q_002 = "good"
        steps_002 = 7000
        cals_002 = 2600

        if 20 <= day <= 23:
            rhr_002 = 72 + (day - 20) * 2
            hrv_002 = 42 - (day - 20) * 3
            sleep_002 = 5.8 - (day - 20) * 0.3
            sleep_q_002 = "poor" if day >= 22 else "fair"
            steps_002 = 5000
            cals_002 = 2200
        elif day <= 5:
            rhr_002 = 64 + (day % 3)
            hrv_002 = 56 + (day % 4)
            sleep_002 = 7.5 + (day % 2) * 0.3
            sleep_q_002 = "good"
        elif day <= 12:
            rhr_002 = 65 + (day % 3)
            hrv_002 = 54 + (day % 4)
            sleep_002 = 7.3 + (day % 3) * 0.2
        else:
            rhr_002 = 66 + (day % 3)
            hrv_002 = 53 + (day % 4)
            sleep_002 = 7.2 + (day % 3) * 0.2

        metrics.append({
            "date": _d(day),
            "athlete_id": "athlete_002",
            "resting_heart_rate": rhr_002,
            "steps": steps_002,
            "calories_total": cals_002,
            "sleep_hours": round(sleep_002, 1),
            "sleep_quality": sleep_q_002,
            "hrv_ms": hrv_002,
        })

        # ── Sam Okafor (athlete_003) ──
        # Baseline: resting HR ~55, HRV ~65, sleep ~8h
        # Last 7 days (day 0-6): overtraining — HR rising 55→68, HRV dropping 65→38
        rhr_003 = 55
        hrv_003 = 65
        sleep_003 = 8.0
        sleep_q_003 = "excellent"
        steps_003 = 12000
        cals_003 = 2800

        if day <= 6:
            # Overtraining progression (day 0 = worst, day 6 = start of decline)
            progress = 6 - day  # 0 at day 6, 6 at day 0
            rhr_003 = 58 + progress * 1.7
            hrv_003 = 58 - progress * 3.3
            sleep_003 = 7.2 - progress * 0.28
            sleep_q_003 = "poor" if day <= 2 else "fair"
            steps_003 = 14000 + progress * 200
            cals_003 = 3000 + progress * 50
        elif day <= 14:
            rhr_003 = 55 + (day % 3)
            hrv_003 = 63 + (day % 4)
            sleep_003 = 7.8 + (day % 3) * 0.2
            sleep_q_003 = "good"
        else:
            rhr_003 = 54 + (day % 3)
            hrv_003 = 65 + (day % 4)
            sleep_003 = 8.0 + (day % 2) * 0.2
            sleep_q_003 = "excellent" if day % 3 == 0 else "good"

        metrics.append({
            "date": _d(day),
            "athlete_id": "athlete_003",
            "resting_heart_rate": round(rhr_003),
            "steps": steps_003,
            "calories_total": cals_003,
            "sleep_hours": round(sleep_003, 1),
            "sleep_quality": sleep_q_003,
            "hrv_ms": round(hrv_003),
        })

    return metrics


HEALTH_METRICS: list[dict[str, Any]] = _build_health_metrics()


# ---------------------------------------------------------------------------
# Data Access Helpers
# ---------------------------------------------------------------------------


def get_athlete(athlete_id: str) -> dict[str, Any] | None:
    """Return athlete profile or None."""
    return ATHLETES.get(athlete_id)


def list_athletes() -> list[dict[str, Any]]:
    """Return all athlete profiles."""
    return list(ATHLETES.values())


def get_sessions_for_athlete(athlete_id: str, limit: int = 10) -> list[dict[str, Any]]:
    """Return most recent sessions for an athlete, sorted by date descending."""
    athlete_sessions = [s for s in SESSIONS if s["athlete_id"] == athlete_id]
    athlete_sessions.sort(key=lambda s: s["date"], reverse=True)
    return athlete_sessions[:limit]


def get_session_by_id(session_id: str) -> dict[str, Any] | None:
    """Return a specific session by its ID, or None."""
    for s in SESSIONS:
        if s["session_id"] == session_id:
            return s
    return None


def get_health_metrics_for_athlete(
    athlete_id: str, metric: str | None = None, days: int = 7
) -> list[dict[str, Any]]:
    """Return health metrics for an athlete over the last N days.

    If metric is specified, returns only date + that metric field.
    """
    cutoff = (_TODAY - timedelta(days=days)).isoformat()
    records = [
        m for m in HEALTH_METRICS
        if m["athlete_id"] == athlete_id and m["date"] >= cutoff
    ]
    records.sort(key=lambda m: m["date"], reverse=True)

    if metric:
        return [{"date": r["date"], metric: r.get(metric)} for r in records]
    return records


def get_all_health_metrics_for_athlete(
    athlete_id: str, days: int = 30
) -> list[dict[str, Any]]:
    """Return all health metric records for an athlete over the last N days."""
    return get_health_metrics_for_athlete(athlete_id, metric=None, days=days)
