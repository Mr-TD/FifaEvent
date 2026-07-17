"""Tests for the StadiumAI engine."""

from ai_engine import StadiumAI


def test_ai_engine_initialization():
    """Test AI engine initializes with empty key."""
    engine = StadiumAI(api_key="")
    assert not engine.use_gemini
    assert engine.cache == {}


def test_mock_chat():
    """Test the fallback chat."""
    engine = StadiumAI(api_key="")
    response = engine.chat("Where is the restroom?", "en")
    assert "Restrooms are located" in response or "🚻" in response


def test_mock_translate():
    """Test the fallback translation."""
    engine = StadiumAI(api_key="")
    response = engine.translate("Hello", "en", "es")
    assert "[Traducción al español]" in response


def test_mock_crowd_recommendation():
    """Test crowd recommendation fallback."""
    engine = StadiumAI(api_key="")
    response = engine.crowd_recommendation({"overall_density": 90, "stadium_name": "Test"})
    assert "HIGH DENSITY" in response or "🔴" in response


def test_ai_cache():
    """Test that the cache stores responses."""
    engine = StadiumAI(api_key="")

    # Pre-populate cache manually
    engine.cache["test_hash"] = "Cached response"

    # Mock the hash function to return test_hash
    engine._get_cache_key = lambda x: "test_hash"

    response = engine.translate("Test string", "en", "es")
    assert response == "Cached response"


def test_mock_transportation_recommendation_eco():
    """Test transportation recommendation fallback with eco-friendly preference."""
    engine = StadiumAI(api_key="")
    response = engine.transportation_recommendation(
        {
            "stadium_name": "MetLife Stadium",
            "city": "New York",
            "time_of_day": "afternoon",
            "preference": "eco-friendly",
        }
    )
    assert "MetLife Stadium" in response
    assert "eco" in response.lower() or "🌱" in response


def test_mock_transportation_recommendation_fastest():
    """Test transportation recommendation fallback with fastest preference."""
    engine = StadiumAI(api_key="")
    response = engine.transportation_recommendation(
        {
            "stadium_name": "SoFi Stadium",
            "city": "Los Angeles",
            "time_of_day": "evening",
            "preference": "fastest",
        }
    )
    assert "SoFi Stadium" in response


def test_mock_transportation_recommendation_cheapest():
    """Test transportation recommendation fallback with cheapest preference."""
    engine = StadiumAI(api_key="")
    response = engine.transportation_recommendation(
        {
            "stadium_name": "AT&T Stadium",
            "city": "Dallas",
            "time_of_day": "morning",
            "preference": "cheapest",
        }
    )
    assert "AT&T Stadium" in response


def test_mock_ops_briefing():
    """Test operational intelligence briefing fallback."""
    engine = StadiumAI(api_key="")
    response = engine.ops_briefing(
        {
            "stadium_name": "Test Stadium",
            "overall_density": 75,
            "zones": [{"zone": "North Stand", "density": 80}],
            "role": "manager",
            "active_staff": 200,
            "active_volunteers": 100,
            "weather": "Sunny, 25°C",
            "upcoming_matches": [{"team_a": "USA", "team_b": "Mexico", "stage": "Group A"}],
            "timestamp": "2026-07-01T15:00:00",
        }
    )
    assert "Test Stadium" in response
    assert "Situation Report" in response or "Priority Actions" in response


def test_mock_ops_briefing_high_density():
    """Test ops briefing with high density triggers high alert."""
    engine = StadiumAI(api_key="")
    response = engine.ops_briefing(
        {
            "stadium_name": "High Density Arena",
            "overall_density": 90,
            "zones": [],
            "role": "security",
            "active_staff": 300,
            "active_volunteers": 150,
            "weather": "Clear",
            "upcoming_matches": [],
            "timestamp": "2026-07-01T18:00:00",
        }
    )
    assert "HIGH DENSITY" in response or "🔴" in response


def test_mock_sustainability_tip():
    """Test sustainability tip fallback returns a tip."""
    engine = StadiumAI(api_key="")
    response = engine.sustainability_tip("arriving")
    assert len(response) > 20  # Should be a meaningful tip


def test_mock_accessibility_guide():
    """Test accessibility guide fallback returns route guidance."""
    engine = StadiumAI(api_key="")
    response = engine.accessibility_guide("wheelchair access", "Section 200")
    assert "Section 200" in response
    assert "accessible" in response.lower() or "♿" in response


def test_mock_match_preview():
    """Test match preview fallback returns engaging text."""
    engine = StadiumAI(api_key="")
    response = engine.generate_match_preview({"team_a": "Brazil", "team_b": "Germany", "stage": "Quarter-Final"})
    assert "Brazil" in response
    assert "Germany" in response
