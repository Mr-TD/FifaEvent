"""
StadiumIQ Configuration
FIFA World Cup 2026 — GenAI Stadium Experience Platform
Powered by Google Cloud Services
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'stadiumiq-fifa-2026-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///stadium_iq.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ─── Google Cloud Services ──────────────────────────────────
    # Google Gemini API (GenAI)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

    # Google Maps Platform (Maps JS, Places, Directions)
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

    # Google Analytics 4 (Measurement ID)
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')

    # Google OAuth 2.0 (Sign-In)
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '')

    # ─── App Settings ──────────────────────────────────────────
    APP_NAME = 'StadiumIQ'
    APP_VERSION = '2.0.0'
    APP_TAGLINE = 'AI-Powered FIFA World Cup 2026 Stadium Experience — Powered by Google'

    # Supported languages (Google Translate handles all, these are primary)
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Espanol',
        'fr': 'Francais',
        'pt': 'Portugues',
        'ar': 'Arabic',
        'zh': 'Chinese',
        'hi': 'Hindi',
        'de': 'Deutsch',
        'ja': 'Japanese',
        'ko': 'Korean',
        'it': 'Italiano',
        'nl': 'Nederlands',
    }

    # Debug mode
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')
    SECRET_KEY = 'test-secret-key'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
