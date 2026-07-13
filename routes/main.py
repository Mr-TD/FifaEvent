"""
StadiumIQ — Main Routes
Home page and general navigation
"""

import json
import os

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "data")


@main_bp.route("/")
def index():
    """Landing page."""
    # Load stats for the hero section
    try:
        with open(os.path.join(DATA_DIR, "stadiums.json"), "r", encoding="utf-8") as f:
            stadiums = json.load(f)
        with open(os.path.join(DATA_DIR, "schedule.json"), "r", encoding="utf-8") as f:
            matches = json.load(f)
    except Exception:
        stadiums = []
        matches = []

    stats = {
        "venues": len(stadiums),
        "teams": 48,
        "matches": 104,
        "cities": len(set(s.get("city", "") for s in stadiums)),
    }

    # Get upcoming matches for ticker
    upcoming = [m for m in matches if m.get("status") == "scheduled"][:5]

    return render_template("index.html", stats=stats, upcoming=upcoming, stadiums=stadiums)


@main_bp.route("/about")
def about():
    """About page."""
    return render_template("index.html")
