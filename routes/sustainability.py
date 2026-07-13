"""
StadiumIQ — Sustainability Routes
Eco-impact tracking and AI green tips
"""

import uuid

from flask import Blueprint, current_app, jsonify, render_template, request, session

sustainability_bp = Blueprint("sustainability", __name__)


@sustainability_bp.route("/sustainability")
def sustainability_page():
    """Sustainability tracker page."""
    return render_template("sustainability.html")


@sustainability_bp.route("/api/sustainability/tips")
def get_tips():
    """Get AI-generated sustainability tips."""
    context = request.args.get("context", "general")

    ai = current_app.config.get("AI_ENGINE")
    if ai:
        tip = ai.sustainability_tip(context)
    else:
        tip = "🌱 Bring a reusable water bottle! All FIFA World Cup 2026 stadiums have free refill stations."

    return jsonify({"tip": tip, "context": context})


@sustainability_bp.route("/api/sustainability/log", methods=["POST"])
def log_action():
    """Log a sustainability action."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request data required"}), 400

    if "sustainability_session" not in session:
        session["sustainability_session"] = str(uuid.uuid4())

    action_type = data.get("action_type", "general")

    # Predefined impact values
    impact_map = {
        "public_transit": {"score": 10, "carbon_kg": 4.5, "desc": "Used public transit to the stadium"},
        "reusable_bottle": {"score": 5, "carbon_kg": 0.5, "desc": "Brought a reusable water bottle"},
        "recycling": {"score": 3, "carbon_kg": 0.3, "desc": "Used recycling bins properly"},
        "digital_ticket": {"score": 4, "carbon_kg": 0.1, "desc": "Used a digital ticket"},
        "local_food": {"score": 6, "carbon_kg": 1.2, "desc": "Chose locally sourced food"},
        "carpooling": {"score": 8, "carbon_kg": 3.0, "desc": "Carpooled to the stadium"},
    }

    impact = impact_map.get(action_type, {"score": 2, "carbon_kg": 0.2, "desc": action_type})

    # Store in session for demo purposes
    if "eco_actions" not in session:
        session["eco_actions"] = []

    actions = session["eco_actions"]
    actions.append(
        {
            "action_type": action_type,
            "description": impact["desc"],
            "impact_score": impact["score"],
            "carbon_saved_kg": impact["carbon_kg"],
        }
    )
    session["eco_actions"] = actions

    total_score = sum(a["impact_score"] for a in actions)
    total_carbon = sum(a["carbon_saved_kg"] for a in actions)

    return jsonify(
        {
            "action": impact,
            "total_score": total_score,
            "total_carbon_saved": round(total_carbon, 2),
            "action_count": len(actions),
        }
    )


@sustainability_bp.route("/api/sustainability/stats")
def get_stats():
    """Get user's sustainability stats."""
    actions = session.get("eco_actions", [])
    total_score = sum(a["impact_score"] for a in actions)
    total_carbon = sum(a["carbon_saved_kg"] for a in actions)

    return jsonify(
        {
            "total_score": total_score,
            "total_carbon_saved": round(total_carbon, 2),
            "action_count": len(actions),
            "actions": actions,
            "level": "Eco Champion 🏆" if total_score > 30 else ("Green Fan 🌿" if total_score > 15 else "Getting Started 🌱"),
        }
    )
