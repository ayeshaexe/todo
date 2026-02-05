"""
Integration test for session persistence to verify end-to-end functionality.
"""

import unittest
import requests
import os
import time
import uuid

class TestSessionFlowIntegration(unittest.TestCase):
    """
    Integration tests for the session persistence flow.
    These tests verify that authentication state persists across browser refreshes
    and that JWT tokens are properly managed.
    """

    def setUp(self):
        """Set up test environment."""
        self.base_url = os.getenv('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:3000')
        self.auth_token = None
        self.user_data = None
        self.test_user_email = f"session_test_{uuid.uuid4()}@example.com"
        self.test_user_password = "SecurePassword123!"
        self.test_user_name = "Session Test User"

        # Register and authenticate a test user for the tests
        self._setup_test_user()

    def _setup_test_user(self):
        """Register and authenticate a test user."""
        # Register the user
        signup_response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": self.test_user_email,
            "password": self.test_user_password,
            "name": self.test_user_name
        })

        self.assertEqual(signup_response.status_code, 200,
                         f"User registration should succeed. Got status: {signup_response.status_code}")

        signup_data = signup_response.json()
        self.auth_token = signup_data['jwt_token']
        self.user_data = signup_data['user']

        self.assertIsNotNone(self.auth_token, "Should have received JWT token after signup")
        self.assertIsNotNone(self.user_data, "Should have received user data after signup")

    def _get_auth_headers(self):
        """Get headers with authorization token."""
        return {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def test_session_persistence_across_requests(self):
        """
        Test that JWT token remains valid across multiple requests.
        """
        # Create a task using the initial token
        create_response = requests.post(
            f"{self.base_url}/api/tasks",
            json={
                "title": "Session Persistence Test Task",
                "description": "Testing session persistence across requests",
                "completed": False
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(create_response.status_code, 200,
                         f"Task creation should succeed with initial token. Got status: {create_response.status_code}")

        create_data = create_response.json()
        self.assertIn('data', create_data, "Create response should include data field")
        task_id = create_data['data']['id']
        self.assertIsNotNone(task_id, "Task should have been created with an ID")

        # Make another request with the same token (simulating browser refresh scenario)
        get_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_response.status_code, 200,
                         f"Get tasks should succeed with same token. Got status: {get_response.status_code}")

        get_data = get_response.json()
        self.assertIn('data', get_data, "Get response should include data field")

        # Verify our task is in the list
        tasks = get_data['data']
        created_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(created_task, "Created task should be retrieved with same token")

        # Update the task with the same token
        update_response = requests.put(
            f"{self.base_url}/api/tasks/{task_id}",
            json={
                "title": "Updated Session Persistence Test Task",
                "completed": True
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(update_response.status_code, 200,
                         f"Task update should succeed with same token. Got status: {update_response.status_code}")

        # Clean up
        delete_response = requests.delete(
            f"{self.base_url}/api/tasks/{task_id}",
            headers=self._get_auth_headers()
        )
        self.assertEqual(delete_response.status_code, 200,
                         f"Task deletion should succeed. Got status: {delete_response.status_code}")

    def test_token_expiration_behavior(self):
        """
        Test behavior when using an expired token.
        """
        # For this test, we'll simulate what happens with an invalid/expired token
        # In a real scenario, we'd need to wait for token expiration or use a test environment
        # that allows token manipulation

        # Use an obviously invalid token
        invalid_token = "invalid.token.here"
        invalid_headers = {
            'Authorization': f'Bearer {invalid_token}',
            'Content-Type': 'application/json'
        }

        # Try to make an authenticated request with invalid token
        response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=invalid_headers
        )

        # Should get 401 Unauthorized
        self.assertEqual(response.status_code, 401,
                         f"Invalid token should result in 401. Got status: {response.status_code}")

        response_data = response.json()
        self.assertIn('error', response_data, "401 response should include error field")
        self.assertIn('message', response_data, "401 response should include message field")

    def test_logout_clears_session_state(self):
        """
        Test that logout properly invalidates the session.
        """
        # First, create a task to verify we have a valid session
        create_response = requests.post(
            f"{self.base_url}/api/tasks",
            json={
                "title": "Test Task Before Logout",
                "description": "This task will be created before logout",
                "completed": False
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(create_response.status_code, 200,
                         f"Task creation before logout should succeed. Got status: {create_response.status_code}")

        create_data = create_response.json()
        task_id = create_data['data']['id']
        self.assertIsNotNone(task_id, "Task should have been created before logout")

        # Perform logout
        logout_response = requests.post(
            f"{self.base_url}/api/auth/logout",
            headers=self._get_auth_headers()
        )

        # Logout response might vary depending on implementation
        # Some systems return 200 on success, others might return 401 after invalidating token
        self.assertIn(logout_response.status_code, [200, 204, 401],
                      f"Logout should return success or token-invalidated status. Got: {logout_response.status_code}")

        # Try to make another request with the same token (should fail after logout)
        get_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        # After logout, the token should be invalidated
        self.assertEqual(get_response.status_code, 401,
                         f"Requests after logout should fail with 401. Got status: {get_response.status_code}")

        # Clean up the task we created (using a fresh login)
        # Re-authenticate to clean up
        login_response = requests.post(f"{self.base_url}/api/auth/login", json={
            "email": self.test_user_email,
            "password": self.test_user_password
        })

        if login_response.status_code == 200:
            login_data = login_response.json()
            fresh_token = login_data['jwt_token']

            fresh_headers = {
                'Authorization': f'Bearer {fresh_token}',
                'Content-Type': 'application/json'
            }

            # Delete the test task
            cleanup_response = requests.delete(
                f"{self.base_url}/api/tasks/{task_id}",
                headers=fresh_headers
            )
            # Ignore cleanup result as it's not part of the test

    def test_concurrent_session_access(self):
        """
        Test that session tokens can be used concurrently across different requests.
        """
        # Create multiple tasks concurrently using the same session token
        import concurrent.futures

        def create_task(task_num):
            response = requests.post(
                f"{self.base_url}/api/tasks",
                json={
                    "title": f"Concurrent Task {task_num}",
                    "description": f"Task {task_num} created concurrently",
                    "completed": False
                },
                headers=self._get_auth_headers()
            )
            return response.status_code, response.json() if response.status_code == 200 else None

        # Create 3 tasks concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_task, i) for i in range(1, 4)]
            results = [future.result() for future in futures]

        # Verify all creations succeeded
        for i, (status_code, response_data) in enumerate(results):
            with self.subTest(task_num=i+1):
                self.assertEqual(status_code, 200,
                                f"Concurrent task {i+1} creation should succeed. Got status: {status_code}")
                if response_data and 'data' in response_data:
                    self.assertIn('id', response_data['data'],
                                 f"Concurrent task {i+1} should return task ID")

        # Verify all tasks were created by fetching the list
        get_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_response.status_code, 200,
                         f"Get tasks after concurrent creation should succeed. Got status: {get_response.status_code}")

        get_data = get_response.json()
        tasks = get_data['data']

        # Count tasks with titles starting with "Concurrent Task"
        concurrent_tasks = [task for task in tasks if task['title'].startswith("Concurrent Task")]
        self.assertEqual(len(concurrent_tasks), 3,
                        f"Should have 3 concurrent tasks, got {len(concurrent_tasks)}")

        # Clean up: delete all concurrent tasks
        for task in concurrent_tasks:
            delete_response = requests.delete(
                f"{self.base_url}/api/tasks/{task['id']}",
                headers=self._get_auth_headers()
            )
            self.assertEqual(delete_response.status_code, 200,
                           f"Cleanup of concurrent task should succeed. Got status: {delete_response.status_code}")

    def test_session_isolation_between_users(self):
        """
        Test that one user's session doesn't interfere with another user's session.
        """
        # Create a second test user
        second_user_email = f"session_test_{uuid.uuid4()}@example.com"
        second_user_password = "SecurePassword456!"
        second_user_name = "Second Session Test User"

        # Register second user
        second_signup_response = requests.post(f"{self.base_url}/api/auth/signup", json={
            "email": second_user_email,
            "password": second_user_password,
            "name": second_user_name
        })

        self.assertEqual(second_signup_response.status_code, 200,
                         f"Second user registration should succeed. Got status: {second_signup_response.status_code}")

        second_signup_data = second_signup_response.json()
        second_user_token = second_signup_data['jwt_token']
        second_user_data = second_signup_data['user']

        # Create a task with first user
        first_user_task_title = "First User Task"
        first_create_response = requests.post(
            f"{self.base_url}/api/tasks",
            json={
                "title": first_user_task_title,
                "description": "Task created by first user",
                "completed": False
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(first_create_response.status_code, 200,
                         f"First user task creation should succeed. Got status: {first_create_response.status_code}")

        first_task_id = first_create_response.json()['data']['id']
        self.assertIsNotNone(first_task_id, "First user task should be created")

        # Create a task with second user
        second_user_task_title = "Second User Task"
        second_headers = {
            'Authorization': f'Bearer {second_user_token}',
            'Content-Type': 'application/json'
        }

        second_create_response = requests.post(
            f"{self.base_url}/api/tasks",
            json={
                "title": second_user_task_title,
                "description": "Task created by second user",
                "completed": False
            },
            headers=second_headers
        )

        self.assertEqual(second_create_response.status_code, 200,
                         f"Second user task creation should succeed. Got status: {second_create_response.status_code}")

        second_task_id = second_create_response.json()['data']['id']
        self.assertIsNotNone(second_task_id, "Second user task should be created")

        # Verify first user only sees their own task
        first_user_tasks_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(first_user_tasks_response.status_code, 200,
                         f"First user get tasks should succeed. Got status: {first_user_tasks_response.status_code}")

        first_user_tasks = first_user_tasks_response.json()['data']
        first_user_task_titles = [task['title'] for task in first_user_tasks]

        self.assertIn(first_user_task_title, first_user_task_titles,
                     "First user should see their own task")
        self.assertNotIn(second_user_task_title, first_user_task_titles,
                        "First user should not see second user's task")

        # Verify second user only sees their own task
        second_user_tasks_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=second_headers
        )

        self.assertEqual(second_user_tasks_response.status_code, 200,
                         f"Second user get tasks should succeed. Got status: {second_user_tasks_response.status_code}")

        second_user_tasks = second_user_tasks_response.json()['data']
        second_user_task_titles = [task['title'] for task in second_user_tasks]

        self.assertIn(second_user_task_title, second_user_task_titles,
                     "Second user should see their own task")
        self.assertNotIn(first_user_task_title, second_user_task_titles,
                        "Second user should not see first user's task")

        # Clean up: delete tasks
        first_cleanup = requests.delete(
            f"{self.base_url}/api/tasks/{first_task_id}",
            headers=self._get_auth_headers()
        )
        self.assertEqual(first_cleanup.status_code, 200,
                        f"First user task cleanup should succeed")

        second_cleanup = requests.delete(
            f"{self.base_url}/api/tasks/{second_task_id}",
            headers=second_headers
        )
        self.assertEqual(second_cleanup.status_code, 200,
                        f"Second user task cleanup should succeed")

if __name__ == '__main__':
    unittest.main()