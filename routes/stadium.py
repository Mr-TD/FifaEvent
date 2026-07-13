"""
StadiumIQ — Stadium Routes
Interactive stadium navigator and POI endpoints
"""

import json
import os

from flask import Blueprint, current_app, jsonify, render_template, request

stadium_bp = Blueprint("stadium", __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "data")


def load_json(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [] if filename != "poi.json" else {}


@stadium_bp.route("/stadium")
def stadium_page():
    """Stadium navigator page."""
    stadiums = load_json("stadiums.json")
    return render_template("stadium.html", stadiums=stadiums)


@stadium_bp.route("/api/stadiums")
def get_stadiums():
    """Get all stadiums."""
    stadiums = load_json("stadiums.json")
    return jsonify({"stadiums": stadiums})


@stadium_bp.route("/api/stadium/<int:stadium_id>/pois")
def get_pois(stadium_id):
    """Get points of interest for a specific stadium."""
    pois = load_json("poi.json")
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
    """AI-powered navigation recommendation."""
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
