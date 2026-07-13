"""
StadiumIQ Database Models
FIFA World Cup 2026
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Stadium(db.Model):
    """FIFA World Cup 2026 venue."""
    __tablename__ = 'stadiums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), default='')
    description = db.Column(db.Text, default='')

    # Relationships
    matches = db.relationship('Match', backref='stadium', lazy=True)
    pois = db.relationship('PointOfInterest', backref='stadium', lazy=True)
    crowd_snapshots = db.relationship('CrowdSnapshot', backref='stadium', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'country': self.country,
            'capacity': self.capacity,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'description': self.description,
        }


class Match(db.Model):
    """FIFA World Cup 2026 match."""
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    team_a = db.Column(db.String(100), nullable=False)
    team_b = db.Column(db.String(100), nullable=False)
    team_a_flag = db.Column(db.String(10), default='🏳️')
    team_b_flag = db.Column(db.String(10), default='🏳️')
    match_date = db.Column(db.DateTime, nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.id'), nullable=False)
    stage = db.Column(db.String(50), nullable=False)  # Group A, Round of 16, etc.
    group_name = db.Column(db.String(20), default='')
    score_a = db.Column(db.Integer, default=None, nullable=True)
    score_b = db.Column(db.Integer, default=None, nullable=True)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, live, completed

    def to_dict(self):
        return {
            'id': self.id,
            'team_a': self.team_a,
            'team_b': self.team_b,
            'team_a_flag': self.team_a_flag,
            'team_b_flag': self.team_b_flag,
            'match_date': self.match_date.isoformat(),
            'stadium_id': self.stadium_id,
            'stadium_name': self.stadium.name if self.stadium else '',
            'stage': self.stage,
            'group_name': self.group_name,
            'score_a': self.score_a,
            'score_b': self.score_b,
            'status': self.status,
        }


class PointOfInterest(db.Model):
    """Point of interest within a stadium."""
    __tablename__ = 'points_of_interest'

    id = db.Column(db.Integer, primary_key=True)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # food, restroom, exit, medical, merch, accessibility
    description = db.Column(db.Text, default='')
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    floor = db.Column(db.String(20), default='Ground')
    is_accessible = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(50), default='map-pin')

    def to_dict(self):
        return {
            'id': self.id,
            'stadium_id': self.stadium_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'floor': self.floor,
            'is_accessible': self.is_accessible,
            'icon': self.icon,
        }


class CrowdSnapshot(db.Model):
    """Real-time crowd density snapshot."""
    __tablename__ = 'crowd_snapshots'

    id = db.Column(db.Integer, primary_key=True)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.id'), nullable=False)
    zone = db.Column(db.String(50), nullable=False)  # North Stand, South Stand, East Gate, etc.
    density_level = db.Column(db.Integer, nullable=False)  # 0-100 percentage
    people_count = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    alert_level = db.Column(db.String(20), default='normal')  # normal, warning, critical

    def to_dict(self):
        return {
            'id': self.id,
            'stadium_id': self.stadium_id,
            'zone': self.zone,
            'density_level': self.density_level,
            'people_count': self.people_count,
            'timestamp': self.timestamp.isoformat(),
            'alert_level': self.alert_level,
        }


class ChatHistory(db.Model):
    """AI chatbot conversation history."""
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_message': self.user_message,
            'ai_response': self.ai_response,
            'language': self.language,
            'timestamp': self.timestamp.isoformat(),
        }


class SustainabilityAction(db.Model):
    """User sustainability action log."""
    __tablename__ = 'sustainability_actions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    impact_score = db.Column(db.Float, default=0.0)
    carbon_saved_kg = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'action_type': self.action_type,
            'description': self.description,
            'impact_score': self.impact_score,
            'carbon_saved_kg': self.carbon_saved_kg,
            'timestamp': self.timestamp.isoformat(),
        }
