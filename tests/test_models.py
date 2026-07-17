"""Tests for the StadiumIQ database models."""

from datetime import UTC, datetime

from models import Match


def test_stadium_model(app, sample_stadium):
    """Test stadium creation and to_dict."""
    with app.app_context():
        assert sample_stadium.name == "Test Stadium"

        stadium_dict = sample_stadium.to_dict()
        assert stadium_dict["name"] == "Test Stadium"
        assert stadium_dict["capacity"] == 50000


def test_match_model(app, sample_stadium):
    """Test match creation."""
    from models import db

    with app.app_context():
        match = Match(
            team_a="USA",
            team_b="Mexico",
            match_date=datetime.now(UTC),
            stadium_id=sample_stadium.id,
            stage="Group A",
        )
        db.session.add(match)
        db.session.commit()

        assert match.id is not None
        assert match.stadium.name == "Test Stadium"

        match_dict = match.to_dict()
        assert match_dict["team_a"] == "USA"
        assert match_dict["stage"] == "Group A"
