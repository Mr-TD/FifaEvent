"""
StadiumIQ — FIFA World Cup 2026
AI-Powered Stadium Experience Platform
Powered by Google Cloud Services

Run with: python app.py
"""

import os
import json
from flask import Flask, g
from flask_socketio import SocketIO
from config import config_by_name
from models import db, Stadium, Match, PointOfInterest
from ai_engine import StadiumAI

socketio = SocketIO()


def create_app(config_name='default'):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')

    # Initialize AI engine (Google Gemini)
    api_key = app.config.get('GEMINI_API_KEY', '')
    ai_engine = StadiumAI(api_key)
    app.config['AI_ENGINE'] = ai_engine

    if ai_engine.use_gemini:
        print('[OK] Google Gemini AI engine initialized successfully')
    else:
        print('[DEMO] Running in DEMO mode (no Gemini API key). Set GEMINI_API_KEY in .env for full AI.')

    # Report Google services status
    google_services = []
    if app.config.get('GEMINI_API_KEY'):
        google_services.append('Gemini AI')
    if app.config.get('GOOGLE_MAPS_API_KEY'):
        google_services.append('Google Maps')
    if app.config.get('GOOGLE_ANALYTICS_ID'):
        google_services.append('Google Analytics')
    if app.config.get('GOOGLE_OAUTH_CLIENT_ID'):
        google_services.append('Google Sign-In')

    # Always available (no key needed)
    google_services.extend(['Google Fonts', 'Google Translate', 'Google Charts', 'Google Calendar Links'])

    print(f'[GOOGLE] Active Google services: {", ".join(google_services)}')

    # Make Google config available to all templates
    @app.context_processor
    def inject_google_config():
        return {
            'GOOGLE_MAPS_API_KEY': app.config.get('GOOGLE_MAPS_API_KEY', ''),
            'GOOGLE_ANALYTICS_ID': app.config.get('GOOGLE_ANALYTICS_ID', ''),
            'GOOGLE_OAUTH_CLIENT_ID': app.config.get('GOOGLE_OAUTH_CLIENT_ID', ''),
            'google_services_count': len(google_services),
        }

    # Register blueprints
    from routes.main import main_bp
    from routes.chatbot import chatbot_bp
    from routes.stadium import stadium_bp
    from routes.schedule import schedule_bp
    from routes.crowd import crowd_bp
    from routes.accessibility import accessibility_bp
    from routes.sustainability import sustainability_bp
    from routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(stadium_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(crowd_bp)
    app.register_blueprint(accessibility_bp)
    app.register_blueprint(sustainability_bp)
    app.register_blueprint(auth_bp)

    # Create database tables and seed data
    with app.app_context():
        db.create_all()
        seed_data(app)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return '''
        <html>
        <head><title>404 - StadiumIQ</title>
        <link rel="stylesheet" href="/static/css/style.css"></head>
        <body style="display:flex;align-items:center;justify-content:center;min-height:100vh;text-align:center">
        <div class="bg-mesh"></div>
        <div style="position:relative;z-index:1">
            <h1 style="font-family:Outfit,sans-serif;font-size:6rem;background:linear-gradient(135deg,#7c3aed,#06d6a0);-webkit-background-clip:text;-webkit-text-fill-color:transparent">404</h1>
            <p style="color:#94a3b8;font-size:1.2rem">Looks like you wandered off the pitch!</p>
            <a href="/" style="margin-top:20px;display:inline-flex;padding:12px 28px;border-radius:12px;background:linear-gradient(135deg,#7c3aed,#06d6a0);color:white;text-decoration:none;font-weight:600">Back to Stadium</a>
        </div>
        </body></html>
        ''', 404

    @app.errorhandler(500)
    def server_error(e):
        return '''
        <html>
        <head><title>500 - StadiumIQ</title>
        <link rel="stylesheet" href="/static/css/style.css"></head>
        <body style="display:flex;align-items:center;justify-content:center;min-height:100vh;text-align:center">
        <div class="bg-mesh"></div>
        <div style="position:relative;z-index:1">
            <h1 style="font-family:Outfit,sans-serif;font-size:4rem;color:#f72585">VAR Review!</h1>
            <p style="color:#94a3b8;font-size:1.2rem">Something went wrong. Our team is reviewing the play.</p>
            <a href="/" style="margin-top:20px;display:inline-flex;padding:12px 28px;border-radius:12px;background:linear-gradient(135deg,#7c3aed,#06d6a0);color:white;text-decoration:none;font-weight:600">Back to Stadium</a>
        </div>
        </body></html>
        ''', 500

    return app


def seed_data(app):
    """Seed database with stadium and match data from JSON files."""
    if Stadium.query.first():
        return

    data_dir = os.path.join(app.root_path, 'static', 'data')

    # Seed stadiums
    try:
        with open(os.path.join(data_dir, 'stadiums.json'), 'r', encoding='utf-8') as f:
            stadiums = json.load(f)
        for s in stadiums:
            db.session.add(Stadium(
                id=s['id'], name=s['name'], city=s['city'], country=s['country'],
                capacity=s['capacity'], latitude=s['latitude'], longitude=s['longitude'],
                description=s.get('description', ''),
            ))
        db.session.commit()
        print(f'[OK] Seeded {len(stadiums)} stadiums')
    except Exception as e:
        db.session.rollback()
        print(f'[WARN] Stadium seed error: {e}')

    # Seed matches
    try:
        with open(os.path.join(data_dir, 'schedule.json'), 'r', encoding='utf-8') as f:
            matches = json.load(f)
        from datetime import datetime
        for m in matches:
            db.session.add(Match(
                id=m['id'], team_a=m['team_a'], team_b=m['team_b'],
                team_a_flag=m.get('team_a_flag', ''), team_b_flag=m.get('team_b_flag', ''),
                match_date=datetime.fromisoformat(m['match_date']),
                stadium_id=m['stadium_id'], stage=m['stage'],
                group_name=m.get('group_name', ''),
                score_a=m.get('score_a'), score_b=m.get('score_b'),
                status=m.get('status', 'scheduled'),
            ))
        db.session.commit()
        print(f'[OK] Seeded {len(matches)} matches')
    except Exception as e:
        db.session.rollback()
        print(f'[WARN] Match seed error: {e}')

    # Seed POIs
    try:
        with open(os.path.join(data_dir, 'poi.json'), 'r', encoding='utf-8') as f:
            all_pois = json.load(f)
        count = 0
        for stadium_id, pois in all_pois.items():
            if stadium_id == 'default':
                continue
            for p in pois:
                db.session.add(PointOfInterest(
                    stadium_id=int(stadium_id), name=p['name'],
                    category=p['category'], description=p.get('description', ''),
                    latitude=p['latitude'], longitude=p['longitude'],
                    floor=p.get('floor', 'Ground'),
                    is_accessible=p.get('is_accessible', True),
                    icon=p.get('icon', 'map-pin'),
                ))
                count += 1
        db.session.commit()
        print(f'[OK] Seeded {count} points of interest')
    except Exception as e:
        db.session.rollback()
        print(f'[WARN] POI seed error: {e}')


if __name__ == '__main__':
    app = create_app('development')

    print('\n=== StadiumIQ - FIFA World Cup 2026 ===')
    print('    Powered by Google Cloud Services')
    print('    http://localhost:5000')
    print('==========================================\n')

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
