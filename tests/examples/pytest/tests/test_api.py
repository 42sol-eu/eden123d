"""Sample pytest tests for web API functionality."""
import pytest
import json
from typing import Dict, Any


class MockHTTPResponse:
    """Mock HTTP response for testing."""
    
    def __init__(self, status_code: int, data: Dict[str, Any]):
        self.status_code = status_code
        self._data = data
    
    def json(self) -> Dict[str, Any]:
        """Return JSON data."""
        return self._data


class APIClient:
    """Simple API client for testing."""
    
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.session_token = None
    
    def login(self, username: str, password: str) -> bool:
        """Mock login method."""
        if username == "admin" and password == "secret":
            self.session_token = "mock_token_123"
            return True
        return False
    
    def get_user(self, user_id: int) -> MockHTTPResponse:
        """Get user by ID."""
        if not self.session_token:
            return MockHTTPResponse(401, {"error": "Unauthorized"})
        
        if user_id == 1:
            return MockHTTPResponse(200, {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            })
        return MockHTTPResponse(404, {"error": "User not found"})
    
    def create_user(self, user_data: Dict[str, Any]) -> MockHTTPResponse:
        """Create a new user."""
        if not self.session_token:
            return MockHTTPResponse(401, {"error": "Unauthorized"})
        
        required_fields = ["name", "email"]
        if not all(field in user_data for field in required_fields):
            return MockHTTPResponse(400, {"error": "Missing required fields"})
        
        return MockHTTPResponse(201, {
            "id": 42,
            "name": user_data["name"],
            "email": user_data["email"]
        })


@pytest.fixture
def api_client():
    """Provide an API client instance."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    """Provide an authenticated API client."""
    api_client.login("admin", "secret")
    return api_client


class TestAuthentication:
    """Test API authentication."""
    
    def test_successful_login(self, api_client):
        """Test successful login."""
        result = api_client.login("admin", "secret")
        assert result is True
        assert api_client.session_token == "mock_token_123"
    
    def test_failed_login(self, api_client):
        """Test failed login."""
        result = api_client.login("wrong", "credentials")
        assert result is False
        assert api_client.session_token is None
    
    @pytest.mark.parametrize("username,password", [
        ("", "secret"),
        ("admin", ""),
        ("", ""),
        ("user", "wrong")
    ])
    def test_login_edge_cases(self, api_client, username, password):
        """Test login with various invalid credentials."""
        result = api_client.login(username, password)
        assert result is False


class TestUserOperations:
    """Test user-related API operations."""
    
    def test_get_existing_user(self, authenticated_client):
        """Test getting an existing user."""
        response = authenticated_client.get_user(1)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
    
    def test_get_nonexistent_user(self, authenticated_client):
        """Test getting a non-existent user."""
        response = authenticated_client.get_user(999)
        assert response.status_code == 404
        assert "error" in response.json()
    
    def test_get_user_unauthorized(self, api_client):
        """Test getting user without authentication."""
        response = api_client.get_user(1)
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"
    
    def test_create_user_success(self, authenticated_client):
        """Test successful user creation."""
        user_data = {
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
        response = authenticated_client.create_user(user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 42
        assert data["name"] == "Jane Smith"
        assert data["email"] == "jane@example.com"
    
    def test_create_user_missing_fields(self, authenticated_client):
        """Test user creation with missing fields."""
        user_data = {"name": "Jane Smith"}  # Missing email
        response = authenticated_client.create_user(user_data)
        assert response.status_code == 400
        assert "Missing required fields" in response.json()["error"]
    
    def test_create_user_unauthorized(self, api_client):
        """Test user creation without authentication."""
        user_data = {"name": "Jane", "email": "jane@example.com"}
        response = api_client.create_user(user_data)
        assert response.status_code == 401


@pytest.mark.integration
class TestIntegrationScenarios:
    """Integration test scenarios."""
    
    def test_full_user_workflow(self, api_client):
        """Test complete user workflow."""
        # Login
        assert api_client.login("admin", "secret") is True
        
        # Create user
        user_data = {"name": "Test User", "email": "test@example.com"}
        create_response = api_client.create_user(user_data)
        assert create_response.status_code == 201
        
        # Get existing user
        get_response = api_client.get_user(1)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "John Doe"
