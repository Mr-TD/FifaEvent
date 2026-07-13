import pytest
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
