"""
Contract test for auth endpoints to verify API compliance with expected contracts.
"""

import unittest
import requests
import os

class TestAuthContract(unittest.TestCase):
    """
    Contract tests for authentication endpoints to ensure API compliance.
    These tests verify that the auth endpoints match the expected API contract
    without testing business logic.
    """

    def setUp(self):
        """Set up test environment."""
        self.base_url = os.getenv('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:3000')

    def test_login_endpoint_contract(self):
        """
        Test that login endpoint accepts expected payload and returns expected response structure.
        """
        # Verify endpoint accepts POST requests
        response = requests.post(f"{self.base_url}/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        # Check that response has expected status codes
        self.assertIn(response.status_code, [200, 400, 401],
                     "Login endpoint should return 200 (success), 400 (validation error), or 401 (unauthorized)")

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # Check response structure if successful
        if response.status_code == 200:
            data = response.json()
            self.assertIn('user', data, "Successful login should return user object")
            self.assertIn('jwt_token', data, "Successful login should return jwt_token")
            self.assertIsInstance(data['user'], dict, "User should be an object")
            self.assertIsInstance(data['jwt_token'], str, "JWT token should be a string")

    def test_signup_endpoint_contract(self):
        """
        Test that signup endpoint accepts expected payload and returns expected response structure.
        """
        response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        })

        # Check that response has expected status codes
        self.assertIn(response.status_code, [200, 400],
                     "Signup endpoint should return 200 (success) or 400 (validation error)")

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # Check response structure if successful
        if response.status_code == 200:
            data = response.json()
            self.assertIn('user', data, "Successful signup should return user object")
            self.assertIn('jwt_token', data, "Successful signup should return jwt_token")
            self.assertIsInstance(data['user'], dict, "User should be an object")
            self.assertIsInstance(data['jwt_token'], str, "JWT token should be a string")

    def test_logout_endpoint_contract(self):
        """
        Test that logout endpoint accepts expected requests and returns expected response structure.
        """
        # Test that endpoint accepts POST requests (without proper auth token for contract testing)
        response = requests.post(f"{self.base_url}/api/auth/logout")

        # Check response structure
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # Status might be 401 (unauthorized) if no token provided, which is expected
        # The important thing is that it returns JSON in expected format
        try:
            data = response.json()
            # If it's a JSON response, check that it has standard error structure
            if response.status_code != 200:
                self.assertIn('error', data, "Error responses should include error field")
                self.assertIn('message', data, "Error responses should include message field")
        except ValueError:
            # Response wasn't JSON, which violates contract
            self.fail("Logout endpoint should return JSON response")

if __name__ == '__main__':
    unittest.main()