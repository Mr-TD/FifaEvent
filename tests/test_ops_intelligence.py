"""Tests for the operational intelligence routes."""

from app import create_app


class TestOpsIntelligenceRoutes:
    """Test suite for operational intelligence endpoints."""

    def setup_method(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown_method(self):
        self.app_context.pop()

    def test_ops_briefing_returns_json(self):
        """Test that the ops briefing API returns valid JSON."""
        response = self.client.get("/api/ops/briefing?stadium_id=1")
        assert response.status_code == 200
        data = response.get_json()
        assert "briefing" in data
        assert "context" in data
        assert "role" in data

    def test_ops_briefing_with_role(self):
        """Test that different roles produce briefings."""
        for role in ["manager", "volunteer", "security"]:
            response = self.client.get(f"/api/ops/briefing?stadium_id=1&role={role}")
            assert response.status_code == 200
            data = response.get_json()
            assert data["role"] == role

    def test_ops_briefing_context_has_required_fields(self):
        """Test that the context snapshot contains all expected fields."""
        response = self.client.get("/api/ops/briefing?stadium_id=1")
        data = response.get_json()
        context = data["context"]
        assert "stadium_name" in context
        assert "overall_density" in context
        assert "zones" in context
        assert "active_staff" in context
        assert "active_volunteers" in context
        assert "timestamp" in context

    def test_volunteer_tasks_returns_tasks(self):
        """Test that volunteer task endpoint returns a task list."""
        response = self.client.get("/api/ops/volunteer-tasks?stadium_id=1")
        assert response.status_code == 200
        data = response.get_json()
        assert "tasks" in data
        assert isinstance(data["tasks"], list)
        assert len(data["tasks"]) > 0

    def test_volunteer_tasks_have_priority(self):
        """Test that each task has a priority field."""
        response = self.client.get("/api/ops/volunteer-tasks?stadium_id=1")
        data = response.get_json()
        for task in data["tasks"]:
            assert "priority" in task
            assert task["priority"] in ("HIGH", "MEDIUM", "LOW")
            assert "task" in task

    def test_volunteer_tasks_include_stadium_info(self):
        """Test that volunteer tasks response includes stadium metadata."""
        response = self.client.get("/api/ops/volunteer-tasks?stadium_id=1")
        data = response.get_json()
        assert "stadium" in data
        assert "crowd_density" in data
        assert "timestamp" in data
