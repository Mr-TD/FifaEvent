"""
StadiumIQ — Stadium Routes
Interactive stadium navigator and POI endpoints
"""

from flask import Blueprint, current_app, jsonify, render_template, request

from utils import load_json

stadium_bp = Blueprint("stadium", __name__)


@stadium_bp.route("/stadium")
def stadium_page():
    """Stadium navigator page."""
    stadiums = load_json("stadiums.json")
    return render_template("stadium.html", stadiums=stadiums)


@stadium_bp.route("/api/stadiums")
def get_stadiums():
    """Get all FIFA World Cup 2026 stadiums.

    Returns:
        JSON with the complete list of stadiums.
    """
    stadiums = load_json("stadiums.json")
    return jsonify({"stadiums": stadiums})


@stadium_bp.route("/api/stadium/<int:stadium_id>/pois")
def get_pois(stadium_id):
    """Get points of interest for a specific stadium.

    If no POIs are defined for the requested stadium, default POIs are
    returned with coordinates offset to the stadium's location.

    Args:
        stadium_id: The ID of the stadium.

    Query Parameters:
        category (str): Optional filter by POI category.

    Returns:
        JSON with the list of POIs and the stadium ID.
    """
    pois = load_json("poi.json", default={})
    stadium_pois = pois.get(str(stadium_id), pois.get("default", []))

    # If using default, offset coordinates based on actual stadium location
    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)

    if stadium and str(stadium_id) not in pois:
        # Offset default POIs to stadium location
        for poi in stadium_pois:
            poi["latitude"] = stadium["latitude"] + poi["latitude"]
            poi["longitude"] = stadium["longitude"] + poi["longitude"]

    category = request.args.get("category")
    if category:
        stadium_pois = [p for p in stadium_pois if p["category"] == category]

    return jsonify({"pois": stadium_pois, "stadium_id": stadium_id})


@stadium_bp.route("/api/stadium/navigate", methods=["POST"])
def navigate():
    """AI-powered navigation recommendation.

    Request JSON:
        destination (str): Target location within the stadium.
        current_location (str): User's current position.
        accessibility_needs (str): Optional accessibility requirements.

    Returns:
        JSON with the AI-generated navigation recommendation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request data is required"}), 400

    destination = data.get("destination", "nearest exit")
    current_location = data.get("current_location", "main entrance")
    needs = data.get("accessibility_needs", "")

    ai = current_app.config.get("AI_ENGINE")
    if ai and needs:
        recommendation = ai.accessibility_guide(needs, destination)
    elif ai:
        recommendation = ai.chat(f"How do I get from {current_location} to {destination}?", context="Stadium navigation request")
    else:
        recommendation = f"Head towards {destination} from {current_location}. Follow the directional signs."

    return jsonify(
        {
            "recommendation": recommendation,
            "destination": destination,
        }
    )
