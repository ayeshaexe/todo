"""
Basic tests to validate the Todo API implementation
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-api"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Todo API is running"

def test_api_routes_exist():
    """Test that API routes are registered (will return 401/404 due to auth, but not 404 for route not found)"""
    # This will fail with 401 since we don't have a valid JWT, but shouldn't fail with 404 for route not found
    response = client.get("/api/tasks")
    # Should return 401 (Unauthorized) rather than 404 (Not Found)
    assert response.status_code in [401, 422]  # 422 might occur if validation fails before auth

if __name__ == "__main__":
    pytest.main([__file__])