"""
StadiumIQ — Main Routes
Home page and general navigation
"""

from flask import Blueprint, render_template

from utils import load_json

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page with hero stats and upcoming match ticker."""
    try:
        stadiums = load_json("stadiums.json")
        matches = load_json("schedule.json")
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
