"""Session query tools for StrideHive."""

from stridehive.server import mcp
from stridehive.data.mock import get_athlete, get_sessions_for_athlete, get_session_by_id


@mcp.tool()
def get_sessions(athlete_id: str, limit: int = 10) -> dict:
    """Get recent training sessions for an athlete.

    Returns a list of sessions with date, type, duration, calories,
    heart rate data, and session-specific metrics like gait asymmetry.

    Args:
        athlete_id: The athlete's unique ID (e.g., 'athlete_001')
        limit: Maximum number of sessions to return (default: 10)
    """
    athlete = get_athlete(athlete_id)
    if not athlete:
        return {"error": f"Athlete '{athlete_id}' not found. Valid IDs: athlete_001, athlete_002, athlete_003"}

    sessions = get_sessions_for_athlete(athlete_id, limit=limit)
    return {
        "athlete": athlete["name"],
        "athlete_id": athlete_id,
        "session_count": len(sessions),
        "sessions": sessions,
    }


@mcp.tool()
def get_session_detail(session_id: str) -> dict:
    """Get full detail of a specific training session.

    Returns complete session data including heart rate zones,
    gait metrics (if applicable), and notes.

    Args:
        session_id: The session's unique ID (e.g., 'sess_001_01')
    """
    session = get_session_by_id(session_id)
    if not session:
        return {"error": f"Session '{session_id}' not found."}

    athlete = get_athlete(session["athlete_id"])
    return {
        "athlete": athlete["name"] if athlete else "Unknown",
        "session": session,
    }
