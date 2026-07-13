"""
StadiumIQ — Schedule Routes
Match schedule and AI-generated previews
"""

import json
import os

from flask import Blueprint, current_app, jsonify, render_template

schedule_bp = Blueprint("schedule", __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "data")


def load_json(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


@schedule_bp.route("/schedule")
def schedule_page():
    """Match schedule page."""
    matches = load_json("schedule.json")
    stadiums = load_json("stadiums.json")

    # Enrich matches with stadium names
    stadium_map = {s["id"]: s["name"] for s in stadiums}
    for match in matches:
        match["stadium_name"] = stadium_map.get(match["stadium_id"], "TBD")

    # Get unique groups and stages
    groups = sorted(set(m["group_name"] for m in matches if m["group_name"]))
    stages = sorted(set(m["stage"] for m in matches))

    return render_template("schedule.html", matches=matches, groups=groups, stages=stages)


@schedule_bp.route("/api/matches")
def get_matches():
    """Get all matches with optional filters."""
    matches = load_json("schedule.json")
    stadiums = load_json("stadiums.json")
    stadium_map = {s["id"]: s["name"] for s in stadiums}

    for match in matches:
        match["stadium_name"] = stadium_map.get(match["stadium_id"], "TBD")

    return jsonify({"matches": matches})


@schedule_bp.route("/api/match/<int:match_id>/preview")
def match_preview(match_id):
    """Get AI-generated match preview."""
    matches = load_json("schedule.json")
    match = next((m for m in matches if m["id"] == match_id), None)

    if not match:
        return jsonify({"error": "Match not found"}), 404

    stadiums = load_json("stadiums.json")
    stadium = next((s for s in stadiums if s["id"] == match["stadium_id"]), None)
    match["stadium_name"] = stadium["name"] if stadium else "TBD"

    ai = current_app.config.get("AI_ENGINE")
    if ai:
        preview = ai.generate_match_preview(match)
    else:
        preview = f"An exciting match between {match['team_a']} and {match['team_b']} awaits!"

    return jsonify(
        {
            "match": match,
            "preview": preview,
        }
    )
