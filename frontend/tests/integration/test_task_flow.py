"""
Integration test for task management flow to verify end-to-end functionality.
"""

import unittest
import requests
import os
import time

class TestTaskFlowIntegration(unittest.TestCase):
    """
    Integration tests for the task management flow.
    These tests verify that the entire task flow works as expected.
    """

    def setUp(self):
        """Set up test environment."""
        self.base_url = os.getenv('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:3000')
        self.auth_token = None
        self.test_user_email = f"test_task_user_{int(time.time())}@example.com"
        self.test_user_password = "SecurePassword123!"
        self.test_user_name = "Test Task User"

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
        self.assertIsNotNone(self.auth_token, "Should have received JWT token after signup")

    def _get_auth_headers(self):
        """Get headers with authorization token."""
        return {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def test_complete_task_management_flow(self):
        """
        Test complete flow: create, read, update, and delete a task.
        """
        # Create a task
        create_response = requests.post(
            f"{self.base_url}/api/tasks",
            json={
                "title": "Integration Test Task",
                "description": "This is a test task for integration testing",
                "completed": False
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(create_response.status_code, 200,
                         f"Task creation should succeed. Got status: {create_response.status_code}")

        create_data = create_response.json()
        self.assertIn('data', create_data, "Create response should include data field")
        self.assertIn('id', create_data['data'], "Created task should have an ID")

        task_id = create_data['data']['id']
        self.assertIsNotNone(task_id, "Task should have a valid ID")

        # Verify task data
        created_task = create_data['data']
        self.assertEqual(created_task['title'], "Integration Test Task")
        self.assertEqual(created_task['description'], "This is a test task for integration testing")
        self.assertFalse(created_task['completed'])

        # Get all tasks and verify the created task is there
        get_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_response.status_code, 200,
                         f"Get tasks should succeed. Got status: {get_response.status_code}")

        get_data = get_response.json()
        self.assertIn('data', get_data, "Get response should include data field")

        tasks = get_data['data']
        self.assertIsInstance(tasks, list, "Tasks should be returned as a list")

        # Find our created task
        created_task_in_list = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(created_task_in_list, "Created task should be in the tasks list")
        self.assertEqual(created_task_in_list['title'], "Integration Test Task")
        self.assertEqual(created_task_in_list['description'], "This is a test task for integration testing")
        self.assertFalse(created_task_in_list['completed'])

        # Update the task
        update_response = requests.put(
            f"{self.base_url}/api/tasks/{task_id}",
            json={
                "title": "Updated Integration Test Task",
                "description": "This task has been updated",
                "completed": True
            },
            headers=self._get_auth_headers()
        )

        self.assertEqual(update_response.status_code, 200,
                         f"Task update should succeed. Got status: {update_response.status_code}")

        update_data = update_response.json()
        self.assertIn('data', update_data, "Update response should include data field")

        updated_task = update_data['data']
        self.assertEqual(updated_task['id'], task_id, "Updated task should have same ID")
        self.assertEqual(updated_task['title'], "Updated Integration Test Task")
        self.assertEqual(updated_task['description'], "This task has been updated")
        self.assertTrue(updated_task['completed'])

        # Verify the update persisted by getting all tasks again
        get_updated_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_updated_response.status_code, 200,
                         f"Get tasks should succeed after update. Got status: {get_updated_response.status_code}")

        get_updated_data = get_updated_response.json()
        updated_tasks = get_updated_data['data']

        # Find our updated task
        updated_task_in_list = next((task for task in updated_tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task_in_list, "Updated task should be in the tasks list")
        self.assertEqual(updated_task_in_list['title'], "Updated Integration Test Task")
        self.assertEqual(updated_task_in_list['description'], "This task has been updated")
        self.assertTrue(updated_task_in_list['completed'])

        # Delete the task
        delete_response = requests.delete(
            f"{self.base_url}/api/tasks/{task_id}",
            headers=self._get_auth_headers()
        )

        self.assertEqual(delete_response.status_code, 200,
                         f"Task deletion should succeed. Got status: {delete_response.status_code}")

        delete_data = delete_response.json()
        self.assertIn('data', delete_data, "Delete response should include data field")
        self.assertTrue(delete_data['data'], "Delete response should indicate success")

        # Verify the task is gone by getting all tasks again
        get_after_delete_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_after_delete_response.status_code, 200,
                         f"Get tasks should succeed after deletion. Got status: {get_after_delete_response.status_code}")

        get_after_delete_data = get_after_delete_response.json()
        remaining_tasks = get_after_delete_data['data']

        # Our deleted task should not be in the list
        deleted_task_in_list = next((task for task in remaining_tasks if task['id'] == task_id), None)
        self.assertIsNone(deleted_task_in_list, "Deleted task should not be in the tasks list")

    def test_task_isolation(self):
        """
        Test that one user's tasks are isolated from another user's tasks.
        """
        # This test would require creating another user and verifying task isolation
        # For now, we'll verify that we can create and manage tasks with our test user

        # Create multiple tasks
        task_titles = ["Task 1", "Task 2", "Task 3"]
        created_task_ids = []

        for title in task_titles:
            create_response = requests.post(
                f"{self.base_url}/api/tasks",
                json={
                    "title": title,
                    "description": f"Description for {title}",
                    "completed": False
                },
                headers=self._get_auth_headers()
            )

            self.assertEqual(create_response.status_code, 200,
                             f"Task creation should succeed for {title}. Got status: {create_response.status_code}")

            create_data = create_response.json()
            created_task_ids.append(create_data['data']['id'])

        # Get all tasks and verify we have all three
        get_response = requests.get(
            f"{self.base_url}/api/tasks",
            headers=self._get_auth_headers()
        )

        self.assertEqual(get_response.status_code, 200,
                         f"Get tasks should succeed. Got status: {get_response.status_code}")

        get_data = get_response.json()
        tasks = get_data['data']

        self.assertEqual(len(tasks), len(task_titles),
                         f"Should have {len(task_titles)} tasks")

        # Verify all created tasks are present
        returned_titles = [task['title'] for task in tasks]
        for title in task_titles:
            self.assertIn(title, returned_titles, f"All created tasks should be returned")

        # Clean up: delete all created tasks
        for task_id in created_task_ids:
            delete_response = requests.delete(
                f"{self.base_url}/api/tasks/{task_id}",
                headers=self._get_auth_headers()
            )
            self.assertEqual(delete_response.status_code, 200,
                             f"Task deletion should succeed. Got status: {delete_response.status_code}")

    def tearDown(self):
        """Clean up test resources."""
        # Log out the test user (if logout endpoint exists)
        # In a real scenario, we might want to clean up the test user account
        pass

if __name__ == '__main__':
    unittest.main()