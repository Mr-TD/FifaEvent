"""
StadiumIQ — Chatbot Routes
AI-powered conversational assistant
"""

from flask import Blueprint, render_template, request, jsonify, current_app, session
import uuid

chatbot_bp = Blueprint('chatbot', __name__)

MAX_MESSAGE_LENGTH = 300
MAX_TRANSLATION_LENGTH = 1000


def _normalize_text_input(value, field_name, max_length, allow_empty=False):
    """Validate and normalize user-provided text input."""
    if not isinstance(value, str):
        raise ValueError(f'{field_name} must be provided as text')

    normalized = ' '.join(value.split())
    if not normalized and not allow_empty:
        raise ValueError(f'{field_name} is required')

    if len(normalized) > max_length:
        raise ValueError(f'{field_name} must be {max_length} characters or fewer')

    return normalized


@chatbot_bp.route('/chatbot')
def chatbot_page():
    """AI Chatbot page."""
    languages = current_app.config.get('SUPPORTED_LANGUAGES', {})
    return render_template('chatbot.html', languages=languages)


@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message and return AI response."""
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    try:
        message = _normalize_text_input(data.get('message', ''), 'message', MAX_MESSAGE_LENGTH)
        language = _normalize_text_input(data.get('language', 'en'), 'language', 20, allow_empty=True)
        context = _normalize_text_input(data.get('context', ''), 'context', 500, allow_empty=True)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    # Get or create session ID
    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())

    # Get AI engine from app
    ai = current_app.config.get('AI_ENGINE')
    if ai:
        response_text = ai.chat(message, language, context)
    else:
        response_text = "I'm StadiumIQ, your FIFA World Cup 2026 assistant! I'm currently in demo mode. Set up your Gemini API key for full AI capabilities."

    return jsonify({
        'response': response_text,
        'session_id': session['chat_session_id'],
        'language': language,
    })


@chatbot_bp.route('/api/chat/suggestions', methods=['GET'])
def suggestions():
    """Get context-aware quick suggestions."""
    suggestions_list = [
        {"text": "🗺️ Where is the nearest restroom?", "icon": "map-pin"},
        {"text": "🍔 What food options are available?", "icon": "utensils"},
        {"text": "📅 What matches are today?", "icon": "calendar"},
        {"text": "🚗 How do I get to the stadium?", "icon": "car"},
        {"text": "♿ Wheelchair accessible routes", "icon": "accessibility"},
        {"text": "🏥 Where is the medical station?", "icon": "heart-pulse"},
        {"text": "🛍️ Where can I buy merchandise?", "icon": "shopping-bag"},
        {"text": "🌱 Give me a sustainability tip", "icon": "leaf"},
    ]
    return jsonify({'suggestions': suggestions_list})


@chatbot_bp.route('/api/translate', methods=['POST'])
def translate():
    """Translate text between languages."""
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    try:
        text = _normalize_text_input(data.get('text', ''), 'text', MAX_TRANSLATION_LENGTH)
        source = _normalize_text_input(data.get('source_lang', 'en'), 'source_lang', 20, allow_empty=True)
        target = _normalize_text_input(data.get('target_lang', 'es'), 'target_lang', 20, allow_empty=True)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    ai = current_app.config.get('AI_ENGINE')
    if ai:
        translated = ai.translate(text, source, target)
    else:
        translated = f"[Translation to {target}] {text}"

    return jsonify({
        'original': text,
        'translated': translated,
        'source_lang': source,
        'target_lang': target,
    })
