"""
StadiumIQ — Accessibility Routes
AI-powered accessible navigation and features
"""

from flask import Blueprint, render_template, request, jsonify, current_app

accessibility_bp = Blueprint('accessibility', __name__)


@accessibility_bp.route('/accessibility')
def accessibility_page():
    """Accessibility hub page."""
    return render_template('accessibility.html')


@accessibility_bp.route('/api/accessibility/route', methods=['POST'])
def accessible_route():
    """Get AI-powered accessible route guidance."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request data required'}), 400

    user_needs = data.get('needs', 'wheelchair access')
    destination = data.get('destination', 'my seat')

    ai = current_app.config.get('AI_ENGINE')
    if ai:
        guidance = ai.accessibility_guide(user_needs, destination)
    else:
        guidance = f"Please proceed to the nearest accessible entrance. Staff in green vests can guide you to {destination}."

    return jsonify({
        'guidance': guidance,
        'needs': user_needs,
        'destination': destination,
    })
