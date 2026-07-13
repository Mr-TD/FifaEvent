"""
StadiumIQ — Crowd Intelligence Routes
Real-time crowd density and AI recommendations
"""

import json
import os
import random
from datetime import datetime

from flask import Blueprint, current_app, jsonify, render_template

crowd_bp = Blueprint("crowd", __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "data")


def load_json(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def generate_crowd_data(stadium_id=1):
    """Generate simulated crowd density data."""
    zones = [
        {"zone": "North Stand", "color": "#7c3aed"},
        {"zone": "South Stand", "color": "#06d6a0"},
        {"zone": "East Wing", "color": "#d4af37"},
        {"zone": "West Wing", "color": "#f72585"},
        {"zone": "VIP Lounge", "color": "#4cc9f0"},
        {"zone": "Main Concourse", "color": "#ff6b35"},
        {"zone": "Gate A Area", "color": "#8338ec"},
        {"zone": "Gate B Area", "color": "#3a86ff"},
        {"zone": "Food Court Level 1", "color": "#fb5607"},
        {"zone": "Upper Deck", "color": "#06d6a0"},
    ]

    for zone in zones:
        zone["density"] = random.randint(25, 95)
        zone["people_count"] = random.randint(500, 8000)
        zone["alert_level"] = "critical" if zone["density"] > 85 else ("warning" if zone["density"] > 70 else "normal")

    overall = sum(z["density"] for z in zones) // len(zones)

    return {
        "stadium_id": stadium_id,
        "zones": zones,
        "overall_density": overall,
        "total_people": sum(z["people_count"] for z in zones),
        "timestamp": datetime.utcnow().isoformat(),
    }


@crowd_bp.route("/crowd")
def crowd_page():
    """Crowd intelligence dashboard."""
    stadiums = load_json("stadiums.json")
    return render_template("crowd.html", stadiums=stadiums)


@crowd_bp.route("/api/crowd/data")
def crowd_data():
    """Get current crowd density data."""
    from flask import request

    stadium_id = request.args.get("stadium_id", 1, type=int)
    data = generate_crowd_data(stadium_id)

    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)
    data["stadium_name"] = stadium["name"] if stadium else "Unknown Stadium"

    return jsonify(data)


@crowd_bp.route("/api/crowd/recommendations")
def crowd_recommendations():
    """Get AI-generated crowd management recommendations."""
    from flask import request

    stadium_id = request.args.get("stadium_id", 1, type=int)
    data = generate_crowd_data(stadium_id)

    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == stadium_id), None)
    data["stadium_name"] = stadium["name"] if stadium else "Unknown Stadium"

    ai = current_app.config.get("AI_ENGINE")
    if ai:
        recommendation = ai.crowd_recommendation(data)
    else:
        recommendation = "Monitor crowd levels and ensure all exit routes remain clear."

    return jsonify(
        {
            "recommendation": recommendation,
            "crowd_data": data,
        }
    )


@crowd_bp.route("/api/crowd/history")
def crowd_history():
    """Get historical crowd data for charts (simulated)."""
    hours = []
    for h in range(24):
        # Simulate a realistic crowd pattern — builds before match, peaks, then drops
        if h < 10:
            base = random.randint(5, 15)
        elif h < 14:
            base = random.randint(20, 45)
        elif h < 16:
            base = random.randint(50, 75)
        elif h < 19:
            base = random.randint(70, 95)
        elif h < 21:
            base = random.randint(60, 85)
        else:
            base = random.randint(10, 30)

        hours.append(
            {
                "hour": f"{h:02d}:00",
                "density": base,
                "people": base * 800,
            }
        )

    return jsonify({"history": hours})
