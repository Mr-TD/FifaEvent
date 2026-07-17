"""
StadiumIQ — Database Seeder
Populates the database with FIFA World Cup 2026 stadiums, matches, and POI data.
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from models import Match, MatchStatus, PointOfInterest, Stadium, db
from utils import load_json

if TYPE_CHECKING:
    from flask import Flask

logger = logging.getLogger(__name__)


def seed_data(app: "Flask") -> None:
    """Seed the database with initial stadium, match, and POI data.

    This function is idempotent — it skips seeding if stadium data already
    exists.  Data is loaded from JSON files in ``static/data/``.

    Args:
        app: The Flask application instance (used for context only).
    """
    if Stadium.query.first():
        return

    _seed_stadiums()
    _seed_matches()
    _seed_pois()


def _seed_stadiums() -> None:
    """Load and insert stadium records from stadiums.json."""
    try:
        stadiums = load_json("stadiums.json")
        for s in stadiums:
            db.session.add(
                Stadium(
                    id=s["id"],
                    name=s["name"],
                    city=s["city"],
                    country=s["country"],
                    capacity=s["capacity"],
                    latitude=s["latitude"],
                    longitude=s["longitude"],
                    description=s.get("description", ""),
                )
            )
        db.session.commit()
        logger.info("Seeded %d stadiums", len(stadiums))
    except Exception as e:
        db.session.rollback()
        logger.warning("Stadium seed error: %s", e)


def _seed_matches() -> None:
    """Load and insert match records from schedule.json."""
    try:
        matches = load_json("schedule.json")
        for m in matches:
            db.session.add(
                Match(
                    id=m["id"],
                    team_a=m["team_a"],
                    team_b=m["team_b"],
                    team_a_flag=m.get("team_a_flag", ""),
                    team_b_flag=m.get("team_b_flag", ""),
                    match_date=datetime.fromisoformat(m["match_date"]),
                    stadium_id=m["stadium_id"],
                    stage=m["stage"],
                    group_name=m.get("group_name", ""),
                    score_a=m.get("score_a"),
                    score_b=m.get("score_b"),
                    status=m.get("status", MatchStatus.SCHEDULED),
                )
            )
        db.session.commit()
        logger.info("Seeded %d matches", len(matches))
    except Exception as e:
        db.session.rollback()
        logger.warning("Match seed error: %s", e)


def _seed_pois() -> None:
    """Load and insert point-of-interest records from poi.json."""
    try:
        all_pois = load_json("poi.json", default={})
        count = 0
        for stadium_id, pois in all_pois.items():
            if stadium_id == "default":
                continue
            for p in pois:
                db.session.add(
                    PointOfInterest(
                        stadium_id=int(stadium_id),
                        name=p["name"],
                        category=p["category"],
                        description=p.get("description", ""),
                        latitude=p["latitude"],
                        longitude=p["longitude"],
                        floor=p.get("floor", "Ground"),
                        is_accessible=p.get("is_accessible", True),
                        icon=p.get("icon", "map-pin"),
                    )
                )
                count += 1
        db.session.commit()
        logger.info("Seeded %d points of interest", count)
    except Exception as e:
        db.session.rollback()
        logger.warning("POI seed error: %s", e)
