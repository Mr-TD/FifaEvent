"""
StadiumIQ — Transportation Routes
AI-powered transit recommendations and stadium transportation info.
"""

import logging
from datetime import UTC, datetime

from flask import Blueprint, current_app, jsonify, render_template, request

from utils import load_json

logger = logging.getLogger(__name__)

transportation_bp = Blueprint("transportation", __name__)


# Pre-defined transit options for each host city
TRANSIT_OPTIONS = {
    "New York": {
        "metro": "NJ Transit / PATH Train → MetLife Stadium shuttle",
        "bus": "FIFA Fan Shuttle from Times Square (every 10 min on match days)",
        "rideshare": "Drop-off at Lot K, Gate D — expect 15-min surge delays",
        "parking": "Lots A–K open 4 hours before kickoff ($50 pre-book / $75 walk-up)",
    },
    "Los Angeles": {
        "metro": "Metro E Line → SoFi Stadium/Hollywood Park station",
        "bus": "FIFA Fan Shuttle from LA Live (every 8 min on match days)",
        "rideshare": "Drop-off zone at Prairie Ave Gate — expect 20-min surge delays",
        "parking": "SoFi lots open 4 hours before kickoff ($60 pre-book / $80 walk-up)",
    },
    "Dallas": {
        "metro": "TRE commuter rail → AT&T Station + shuttle bus",
        "bus": "FIFA Fan Shuttle from downtown Dallas (every 12 min on match days)",
        "rideshare": "Drop-off at Lot 4, East Plaza — expect 10-min surge delays",
        "parking": "Lots 1–15 open 4 hours before kickoff ($40 pre-book / $60 walk-up)",
    },
    "Mexico City": {
        "metro": "Metro Línea 2 → Estadio Azteca station (direct access)",
        "bus": "FIFA Fan Shuttle from Zócalo (every 10 min on match days)",
        "rideshare": "Drop-off at Puerta 1 — expect 15-min surge delays",
        "parking": "Stadium lots open 3 hours before kickoff (MXN 500 pre-book)",
    },
}

# Default transit info used when a city-specific entry is not available
DEFAULT_TRANSIT = {
    "metro": "Check local transit authority for stadium shuttle services",
    "bus": "FIFA Fan Shuttle available from city center on match days",
    "rideshare": "Drop-off zones available at designated stadium gates",
    "parking": "Stadium parking opens 4 hours before kickoff — pre-book recommended",
}


@transportation_bp.route("/transportation")
def transportation_page():
    """Transportation hub page with transit options for all venues."""
    stadiums = load_json("stadiums.json")
    return render_template("transportation.html", stadiums=stadiums)


@transportation_bp.route("/api/transportation/options")
def get_transit_options():
    """Get transit options for a specific stadium.

    Query Parameters:
        stadium_id (int): ID of the stadium. Defaults to 1.

    Returns:
        JSON with transit modes, estimated times, and eco-impact data.
    """
    stadium_id = request.args.get("stadium_id", 1, type=int)

    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)

    if not stadium:
        return jsonify({"error": "Stadium not found"}), 404

    city = stadium.get("city", "")
    transit = TRANSIT_OPTIONS.get(city, DEFAULT_TRANSIT)

    return jsonify(
        {
            "stadium": stadium["name"],
            "city": city,
            "options": transit,
            "eco_recommendation": "🌱 Public transit saves ~4.5 kg CO₂ per trip compared to driving alone.",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )


@transportation_bp.route("/api/transportation/recommend", methods=["POST"])
def recommend_transport():
    """Get AI-powered transportation recommendation.

    Considers crowd density, time of day, and user preferences to suggest
    the optimal way to reach or leave the stadium.

    Request JSON:
        stadium_id (int): Target stadium.
        time_of_day (str): e.g. "morning", "afternoon", "evening".
        preference (str): e.g. "fastest", "cheapest", "eco-friendly".

    Returns:
        JSON with AI-generated recommendation.
    """
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    stadium_id = data.get("stadium_id", 1)
    time_of_day = data.get("time_of_day", "afternoon")
    preference = data.get("preference", "balanced")

    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)
    stadium_name = stadium["name"] if stadium else "the stadium"
    city = stadium.get("city", "Unknown") if stadium else "Unknown"

    ai = current_app.config.get("AI_ENGINE")
    if ai:
        recommendation = ai.transportation_recommendation(
            {
                "stadium_name": stadium_name,
                "city": city,
                "time_of_day": time_of_day,
                "preference": preference,
            }
        )
    else:
        recommendation = (
            f"For {stadium_name}, we recommend public transit during {time_of_day} hours. "
            "FIFA Fan Shuttles run every 10 minutes from city center on match days."
        )

    return jsonify(
        {
            "recommendation": recommendation,
            "stadium": stadium_name,
            "preference": preference,
        }
    )
