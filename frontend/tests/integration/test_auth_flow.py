"""
Integration test for registration and login flow to verify end-to-end functionality.
"""

import unittest
import requests
import os
import uuid

class TestAuthFlowIntegration(unittest.TestCase):
    """
    Integration tests for the registration and login flow.
    These tests verify that the entire flow works as expected.
    """

    def setUp(self):
        """Set up test environment."""
        self.base_url = os.getenv('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:3000')

    def test_registration_then_login_flow(self):
        """
        Test that a user can register and then successfully log in with the same credentials.
        """
        # Generate unique test credentials
        test_email = f"integration_test_{uuid.uuid4()}@example.com"
        test_password = "SecurePassword123!"
        test_name = "Integration Test User"

        # Register the user
        signup_response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": test_email,
            "password": test_password,
            "name": test_name
        })

        # Verify registration succeeded
        self.assertEqual(signup_response.status_code, 200,
                         f"Registration should succeed. Got status: {signup_response.status_code}")

        signup_data = signup_response.json()
        self.assertIn('user', signup_data, "Registration response should include user data")
        self.assertIn('jwt_token', signup_data, "Registration response should include JWT token")
        self.assertEqual(signup_data['user']['email'], test_email, "User email should match")
        self.assertEqual(signup_data['user']['name'], test_name, "User name should match")

        # Attempt to log in with the registered credentials
        login_response = requests.post(f"{self.base_url}/api/auth/login", json={
            "email": test_email,
            "password": test_password
        })

        # Verify login succeeded
        self.assertEqual(login_response.status_code, 200,
                         f"Login should succeed with registered credentials. Got status: {login_response.status_code}")

        login_data = login_response.json()
        self.assertIn('user', login_data, "Login response should include user data")
        self.assertIn('jwt_token', login_data, "Login response should include JWT token")
        self.assertEqual(login_data['user']['email'], test_email, "Logged in user email should match")
        self.assertEqual(login_data['user']['name'], test_name, "Logged in user name should match")

        # Verify the tokens are valid JWT tokens (basic check - they have 3 parts separated by dots)
        signup_token_parts = signup_data['jwt_token'].split('.')
        login_token_parts = login_data['jwt_token'].split('.')

        self.assertEqual(len(signup_token_parts), 3, "JWT token should have 3 parts")
        self.assertEqual(len(login_token_parts), 3, "JWT token should have 3 parts")

    def test_login_with_invalid_credentials(self):
        """
        Test that login fails with invalid credentials.
        """
        # Attempt to log in with invalid credentials
        login_response = requests.post(f"{self.base_url}/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })

        # Verify login failed
        self.assertEqual(login_response.status_code, 401,
                         f"Login should fail with invalid credentials. Got status: {login_response.status_code}")

        login_data = login_response.json()
        self.assertIn('error', login_data, "Error response should include error field")
        self.assertIn('message', login_data, "Error response should include message field")

    def test_duplicate_registration_fails(self):
        """
        Test that registering with an existing email fails appropriately.
        """
        test_email = f"duplicate_test_{uuid.uuid4()}@example.com"
        test_password = "SecurePassword123!"
        test_name = "Duplicate Test User"

        # Register the user first time
        first_signup_response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": test_email,
            "password": test_password,
            "name": test_name
        })

        self.assertEqual(first_signup_response.status_code, 200,
                         f"First registration should succeed. Got status: {first_signup_response.status_code}")

        # Attempt to register with the same email
        second_signup_response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": test_email,
            "password": test_password,
            "name": test_name
        })

        # Verify second registration failed
        self.assertEqual(second_signup_response.status_code, 400,
                         f"Duplicate registration should fail. Got status: {second_signup_response.status_code}")

        # Verify error response structure
        error_data = second_signup_response.json()
        self.assertIn('error', error_data, "Error response should include error field")
        self.assertIn('message', error_data, "Error response should include message field")

if __name__ == '__main__':
    unittest.main()