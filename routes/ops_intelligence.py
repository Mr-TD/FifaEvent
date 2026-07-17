"""
StadiumIQ — Operational Intelligence Routes
Real-time decision support for organizers, staff, and volunteers.
"""

import logging
import random
from datetime import UTC, datetime

from flask import Blueprint, current_app, jsonify, request

from utils import load_json

logger = logging.getLogger(__name__)

ops_bp = Blueprint("ops", __name__)


def _build_ops_context(stadium_id: int) -> dict:
    """Build an operational context snapshot for AI briefings.

    Aggregates stadium info, current crowd simulation, and upcoming match
    data into a single dictionary used by the AI engine.

    Args:
        stadium_id: The ID of the stadium to build context for.

    Returns:
        Dictionary with stadium, crowd, match, and environmental context.
    """
    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)
    stadium_name = stadium["name"] if stadium else "Unknown Stadium"

    # Simulated crowd snapshot
    overall_density = random.randint(30, 95)
    zones_summary = [
        {"zone": "North Stand", "density": random.randint(25, 95)},
        {"zone": "South Stand", "density": random.randint(25, 95)},
        {"zone": "East Wing", "density": random.randint(25, 95)},
        {"zone": "West Wing", "density": random.randint(25, 95)},
        {"zone": "Main Concourse", "density": random.randint(25, 95)},
    ]

    # Upcoming matches at this stadium
    matches = load_json("schedule.json")
    stadium_matches = [m for m in matches if m.get("stadium_id") == stadium_id]
    upcoming = [m for m in stadium_matches if m.get("status") == "scheduled"][:3]

    return {
        "stadium_name": stadium_name,
        "stadium_id": stadium_id,
        "overall_density": overall_density,
        "zones": zones_summary,
        "upcoming_matches": upcoming,
        "timestamp": datetime.now(UTC).isoformat(),
        "weather": "Clear, 28°C",  # Simulated
        "active_staff": random.randint(120, 350),
        "active_volunteers": random.randint(50, 200),
    }


@ops_bp.route("/api/ops/briefing")
def ops_briefing():
    """Generate an AI-powered operational briefing for venue staff.

    Provides a comprehensive situation report covering crowd status,
    staffing, upcoming events, and actionable recommendations.

    Query Parameters:
        stadium_id (int): ID of the stadium. Defaults to 1.
        role (str): Staff role — ``manager``, ``volunteer``, or ``security``.
                    Defaults to ``manager``.

    Returns:
        JSON with the AI-generated briefing and raw context data.
    """
    stadium_id = request.args.get("stadium_id", 1, type=int)
    role = request.args.get("role", "manager")

    context = _build_ops_context(stadium_id)
    context["role"] = role

    ai = current_app.config.get("AI_ENGINE")
    if ai:
        briefing = ai.ops_briefing(context)
    else:
        briefing = _mock_ops_briefing(context)

    return jsonify(
        {
            "briefing": briefing,
            "context": context,
            "role": role,
        }
    )


@ops_bp.route("/api/ops/volunteer-tasks")
def volunteer_tasks():
    """Get AI-suggested task assignments for volunteers.

    Provides prioritized tasks based on current crowd conditions and
    upcoming match schedule.

    Query Parameters:
        stadium_id (int): ID of the stadium. Defaults to 1.

    Returns:
        JSON with a list of prioritized volunteer tasks.
    """
    stadium_id = request.args.get("stadium_id", 1, type=int)
    context = _build_ops_context(stadium_id)

    density = context["overall_density"]

    if density > 80:
        tasks = [
            {"priority": "HIGH", "task": "Direct fans to alternative entrances — Gates C and E are less congested"},
            {"priority": "HIGH", "task": "Staff water distribution points in the North Stand concourse"},
            {"priority": "MEDIUM", "task": "Monitor queue lengths at food stalls and redirect fans to West Wing vendors"},
            {"priority": "MEDIUM", "task": "Ensure all emergency exit routes remain unobstructed"},
            {"priority": "LOW", "task": "Distribute fan engagement surveys at quieter entry points"},
        ]
    elif density > 50:
        tasks = [
            {"priority": "MEDIUM", "task": "Greet incoming fans at main gates and provide wayfinding assistance"},
            {"priority": "MEDIUM", "task": "Check accessibility stations — ensure wheelchair ramps and elevators are clear"},
            {"priority": "LOW", "task": "Replenish recycling station signage and eco-tip cards"},
            {"priority": "LOW", "task": "Assist at the merchandise stalls during pre-match rush"},
        ]
    else:
        tasks = [
            {"priority": "LOW", "task": "Set up fan zone activities and interactive displays"},
            {"priority": "LOW", "task": "Prepare information packs for incoming tour groups"},
            {"priority": "LOW", "task": "Conduct venue walk-through to check signage and accessibility markers"},
        ]

    return jsonify(
        {
            "tasks": tasks,
            "stadium": context["stadium_name"],
            "crowd_density": density,
            "timestamp": context["timestamp"],
        }
    )


def _mock_ops_briefing(context: dict) -> str:
    """Generate a mock operational briefing when AI is unavailable.

    Args:
        context: Operational context dictionary from ``_build_ops_context``.

    Returns:
        Formatted briefing string.
    """
    density = context["overall_density"]
    stadium = context["stadium_name"]
    staff = context["active_staff"]
    volunteers = context["active_volunteers"]

    if density > 80:
        alert = "🔴 HIGH DENSITY"
        action = "Activate overflow protocols. Deploy additional staff to high-density zones."
    elif density > 55:
        alert = "🟡 MODERATE DENSITY"
        action = "Pre-position staff at key transition points. Monitor gate throughput."
    else:
        alert = "🟢 NORMAL OPERATIONS"
        action = "Maintain standard staffing. Good window for maintenance rotations."

    return f"""**{alert} — {stadium}**

📊 **Situation Report** ({context['timestamp']})
- Overall crowd density: {density}%
- Active staff on site: {staff}
- Active volunteers: {volunteers}
- Weather: {context['weather']}

🎯 **Priority Actions:**
1. {action}
2. Ensure all accessibility routes remain clear and operational
3. Monitor sustainability stations — recycling compliance at standard levels
4. Coordinate with transport team for post-match fan dispersal planning

📋 **Upcoming at this venue:**
{chr(10).join(f"- {m.get('team_a', 'TBD')} vs {m.get('team_b', 'TBD')} ({m.get('stage', '')})" for m in context.get('upcoming_matches', [])[:3]) or '- No upcoming matches scheduled'}
"""
