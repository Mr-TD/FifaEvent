"""
StadiumIQ — FIFA World Cup 2026
AI-Powered Stadium Experience Platform
Powered by Google Cloud Services

Run with: python app.py
"""

import logging

from flask import Flask, render_template
from flask_caching import Cache
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

from ai_engine import StadiumAI
from config import config_by_name
from models import db

# Initialize extensions
socketio = SocketIO()
csrf = CSRFProtect()
cache = Cache()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def create_app(config_name: str = "default") -> Flask:
    """Application factory — creates and configures the Flask app.

    Args:
        config_name: Configuration profile to use. One of
                     ``development``, ``production``, ``testing``, or ``default``.

    Returns:
        Fully configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Initialize AI engine (Google Gemini)
    api_key = app.config.get("GEMINI_API_KEY", "")
    ai_engine = StadiumAI(api_key)
    app.config["AI_ENGINE"] = ai_engine

    if ai_engine.use_gemini:
        logger.info("Google Gemini AI engine initialized successfully")
    else:
        logger.warning("Running in DEMO mode (no Gemini API key). Set GEMINI_API_KEY in .env for full AI.")

    # Report Google services status
    google_services = _detect_google_services(app)
    logger.info("Active Google services: %s", ", ".join(google_services))

    # Make Google config available to all templates
    @app.context_processor
    def inject_google_config() -> dict:
        return {
            "GOOGLE_MAPS_API_KEY": app.config.get("GOOGLE_MAPS_API_KEY", ""),
            "GOOGLE_ANALYTICS_ID": app.config.get("GOOGLE_ANALYTICS_ID", ""),
            "GOOGLE_OAUTH_CLIENT_ID": app.config.get("GOOGLE_OAUTH_CLIENT_ID", ""),
            "google_services_count": len(google_services),
        }

    # Register blueprints
    _register_blueprints(app)

    # Create database tables and seed data
    with app.app_context():
        db.create_all()
        from seed import seed_data

        seed_data(app)

    # Error handlers
    _register_error_handlers(app)

    return app


def _detect_google_services(app: Flask) -> list:
    """Detect which Google Cloud services are configured.

    Args:
        app: The Flask application instance.

    Returns:
        List of active Google service names.
    """
    services = []
    if app.config.get("GEMINI_API_KEY"):
        services.append("Gemini AI")
    if app.config.get("GOOGLE_MAPS_API_KEY"):
        services.append("Google Maps")
    if app.config.get("GOOGLE_ANALYTICS_ID"):
        services.append("Google Analytics")
    if app.config.get("GOOGLE_OAUTH_CLIENT_ID"):
        services.append("Google Sign-In")
    services.extend(["Google Fonts", "Google Translate", "Google Charts", "Google Calendar Links"])
    return services


def _register_blueprints(app: Flask) -> None:
    """Register all route blueprints with the application.

    Args:
        app: The Flask application instance.
    """
    from routes.accessibility import accessibility_bp
    from routes.auth import auth_bp
    from routes.chatbot import chatbot_bp
    from routes.crowd import crowd_bp
    from routes.main import main_bp
    from routes.ops_intelligence import ops_bp
    from routes.schedule import schedule_bp
    from routes.stadium import stadium_bp
    from routes.sustainability import sustainability_bp
    from routes.transportation import transportation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(stadium_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(crowd_bp)
    app.register_blueprint(accessibility_bp)
    app.register_blueprint(sustainability_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(transportation_bp)
    app.register_blueprint(ops_bp)

    # Exempt stateless API routes from CSRF
    csrf.exempt(chatbot_bp)
    csrf.exempt(stadium_bp)
    csrf.exempt(schedule_bp)
    csrf.exempt(crowd_bp)
    csrf.exempt(transportation_bp)
    csrf.exempt(ops_bp)


def _register_error_handlers(app: Flask) -> None:
    """Register custom error page handlers.

    Args:
        app: The Flask application instance.
    """

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500


if __name__ == "__main__":
    app = create_app("development")

    logger.info("=== StadiumIQ - FIFA World Cup 2026 ===")
    logger.info("    Powered by Google Cloud Services")
    logger.info("    http://localhost:5000")
    logger.info("==========================================")

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
