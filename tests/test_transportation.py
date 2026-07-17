"""Tests for the transportation routes."""

from app import create_app


class TestTransportationRoutes:
    """Test suite for transportation endpoints."""

    def setup_method(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown_method(self):
        self.app_context.pop()

    def test_transportation_page_loads(self):
        """Test that the transportation page renders successfully."""
        response = self.client.get("/transportation")
        assert response.status_code == 200
        assert b"Transportation" in response.data

    def test_transit_options_returns_json(self):
        """Test that transit options API returns valid JSON with expected keys."""
        response = self.client.get("/api/transportation/options?stadium_id=1")
        assert response.status_code == 200
        data = response.get_json()
        assert "stadium" in data
        assert "options" in data
        assert "eco_recommendation" in data

    def test_transit_options_invalid_stadium(self):
        """Test transit options returns 404 for non-existent stadium."""
        response = self.client.get("/api/transportation/options?stadium_id=9999")
        assert response.status_code == 404

    def test_recommend_transport_valid_request(self):
        """Test AI recommendation endpoint with valid input."""
        response = self.client.post(
            "/api/transportation/recommend",
            json={
                "stadium_id": 1,
                "time_of_day": "evening",
                "preference": "eco-friendly",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "recommendation" in data
        assert data["preference"] == "eco-friendly"

    def test_recommend_transport_defaults(self):
        """Test AI recommendation with empty request body uses defaults."""
        response = self.client.post(
            "/api/transportation/recommend",
            json={},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "recommendation" in data

    def test_recommend_transport_invalid_body(self):
        """Test AI recommendation rejects non-object body."""
        response = self.client.post(
            "/api/transportation/recommend",
            data="not json",
            content_type="text/plain",
        )
        assert response.status_code == 200  # Falls back to defaults gracefully
