"""
Contract test for task endpoints to verify API compliance with expected contracts.
"""

import unittest
import requests
import os

class TestTaskContract(unittest.TestCase):
    """
    Contract tests for task endpoints to ensure API compliance.
    These tests verify that the task endpoints match the expected API contract
    without testing business logic.
    """

    def setUp(self):
        """Set up test environment."""
        self.base_url = os.getenv('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:3000')
        self.auth_token = None  # Will be set after successful auth

    def test_get_tasks_endpoint_contract(self):
        """
        Test that get tasks endpoint returns expected response structure.
        """
        # Without authentication, expect 401
        response = requests.get(f"{self.base_url}/api/tasks")

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # If 401 (unauthorized), verify error structure
        if response.status_code == 401:
            data = response.json()
            self.assertIn('error', data, "401 responses should include error field")
            self.assertIn('message', data, "401 responses should include message field")

    def test_create_task_endpoint_contract(self):
        """
        Test that create task endpoint accepts expected payload and returns expected response structure.
        """
        # Try creating a task without authentication (should fail)
        response = requests.post(f"{self.base_url}/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        })

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # If 401 (unauthorized), verify error structure
        if response.status_code == 401:
            data = response.json()
            self.assertIn('error', data, "401 responses should include error field")
            self.assertIn('message', data, "401 responses should include message field")

    def test_update_task_endpoint_contract(self):
        """
        Test that update task endpoint accepts expected payload and returns expected response structure.
        """
        # Try updating a task without authentication (should fail)
        response = requests.put(f"{self.base_url}/api/tasks/nonexistent-task-id", json={
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        })

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # If 401 (unauthorized) or 404 (not found), verify error structure
        if response.status_code in [401, 404]:
            data = response.json()
            self.assertIn('error', data, "Error responses should include error field")
            self.assertIn('message', data, "Error responses should include message field")

    def test_delete_task_endpoint_contract(self):
        """
        Test that delete task endpoint accepts expected requests and returns expected response structure.
        """
        # Try deleting a task without authentication (should fail)
        response = requests.delete(f"{self.base_url}/api/tasks/nonexistent-task-id")

        # Check response headers
        self.assertEqual(response.headers.get('Content-Type'), 'application/json',
                        "Response should be JSON")

        # If 401 (unauthorized) or 404 (not found), verify error structure
        if response.status_code in [401, 404]:
            data = response.json()
            self.assertIn('error', data, "Error responses should include error field")
            self.assertIn('message', data, "Error responses should include message field")

if __name__ == '__main__':
    unittest.main()