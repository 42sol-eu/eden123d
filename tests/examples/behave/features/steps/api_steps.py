"""Step definitions for API feature tests."""
from behave import given, when, then


class MockAPIResponse:
    """Mock API response."""
    
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self._data = data
    
    def json(self):
        return self._data


class MockAPIClient:
    """Mock API client for testing."""
    
    def __init__(self):
        self.authenticated = False
        self.last_response = None
    
    def login(self, username: str, password: str) -> bool:
        """Mock login."""
        if username == "admin" and password == "secret":
            self.authenticated = True
            return True
        return False
    
    def create_user(self, name: str, email: str) -> MockAPIResponse:
        """Mock user creation."""
        if not self.authenticated:
            return MockAPIResponse(401, {"error": "Unauthorized"})
        
        if not name or not email:
            return MockAPIResponse(400, {"error": "Missing required fields"})
        
        return MockAPIResponse(201, {
            "id": 42,
            "name": name,
            "email": email
        })
    
    def get_user(self, user_id: int) -> MockAPIResponse:
        """Mock get user."""
        if not self.authenticated:
            return MockAPIResponse(401, {"error": "Unauthorized"})
        
        if user_id == 1:
            return MockAPIResponse(200, {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            })
        
        return MockAPIResponse(404, {"error": "User not found"})


@given('I have an API client')
def step_have_api_client(context):
    """Initialize API client."""
    context.api_client = MockAPIClient()


@given('I am authenticated as "{username}" with password "{password}"')
def step_authenticate(context, username, password):
    """Authenticate with API."""
    context.api_client.login(username, password)


@given('I am not authenticated')
def step_not_authenticated(context):
    """Ensure not authenticated."""
    context.api_client.authenticated = False


@when('I create a user with name "{name}" and email "{email}"')
def step_create_user(context, name, email):
    """Create a user."""
    context.response = context.api_client.create_user(name, email)


@when('I request user with ID {user_id:d}')
def step_get_user(context, user_id):
    """Get user by ID."""
    context.response = context.api_client.get_user(user_id)


@then('the user should be created successfully')
def step_user_created_successfully(context):
    """Verify user was created."""
    assert context.response.status_code == 201


@then('the response should contain user ID')
def step_response_contains_user_id(context):
    """Verify response contains user ID."""
    data = context.response.json()
    assert "id" in data
    assert data["id"] is not None


@then('I should get user information')
def step_get_user_info(context):
    """Verify user information received."""
    assert context.response.status_code == 200
    data = context.response.json()
    assert "id" in data
    assert "name" in data
    assert "email" in data


@then('the user name should be "{expected_name}"')
def step_verify_user_name(context, expected_name):
    """Verify user name."""
    data = context.response.json()
    assert data["name"] == expected_name


@then('I should get a "not found" error')
def step_get_not_found_error(context):
    """Verify not found error."""
    assert context.response.status_code == 404
    data = context.response.json()
    assert "error" in data


@then('I should get an "unauthorized" error')
def step_get_unauthorized_error(context):
    """Verify unauthorized error."""
    assert context.response.status_code == 401
    data = context.response.json()
    assert "error" in data


@then('the response status should be {status:d}')
def step_verify_response_status(context, status):
    """Verify response status code."""
    assert context.response.status_code == status
