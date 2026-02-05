'use client';

import { useState, useEffect } from 'react';
import { Task } from '../../types';
import { apiClient } from '../../lib/api-client';
import { useAuth } from '../../hooks/useAuth';
import ProtectedRoute from '../../components/auth/ProtectedRoute';
import TaskList from '../../components/ui/TaskList';
import CreateTaskForm from '../../components/ui/CreateTaskForm';
import EditTaskModal from '../../components/ui/EditTaskModal';

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { token, logout } = useAuth();

  // Set token in API client when it's available
  useEffect(() => {
    if (token) {
      apiClient.setToken(token);
    }
  }, [token]);

  // Load tasks on component mount
  useEffect(() => {
    const fetchTasks = async () => {
      if (!token) return; // Don't fetch if not authenticated

      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.getTasks();
        if (response.status === 401) {
          // Token might be expired, log out user
          logout();
          return;
        }

        if (response.data) {
          // After API response format change, response.data is { tasks: [...] }
          setTasks(response.data.tasks || []);
        } else {
          setError(typeof response.error === 'string' ? response.error : 'Failed to load tasks');
        }
      } catch (error) {
        console.error('Error fetching tasks:', error);
        setError('Failed to load tasks. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [token, logout]);

  const handleCreateTask = async (taskData: { title: string; description?: string; completed: boolean }) => {
    // Optimistic update: add the task to the list immediately
    const tempId = `temp-${Date.now()}`;
    const newTask: Task = {
      id: tempId,
      userId: '', // Will be set by the server
      title: taskData.title,
      description: taskData.description,
      completed: taskData.completed,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setTasks(prev => [newTask, ...prev]);

    try {
      const response = await apiClient.createTask(taskData.title, taskData.description, taskData.completed);
      if (response.status === 401) {
        // Token might be expired, log out user
        logout();
        return;
      }

      if (response.data) {
        // Replace the temporary task with the server response
        // After API response format change, response.data is the task object directly
        setTasks(prev => prev.map(t =>
          t.id === tempId ? response.data : t
        ));
      } else {
        // Rollback if the server request failed
        setTasks(prev => prev.filter(t => t.id !== tempId));
        setError(typeof response.error === 'string' ? response.error : 'Failed to create task');
      }
    } catch (error) {
      // Rollback if the request threw an error
      setTasks(prev => prev.filter(t => t.id !== tempId));
      console.error('Error creating task:', error);
      setError('Failed to create task. Please try again.');
    }
  };

  const handleUpdateTask = async (updatedTask: Task) => {
    // Optimistic update: update the task in the list immediately
    setTasks(prev => prev.map(t =>
      t.id === updatedTask.id ? updatedTask : t
    ));

    try {
      const response = await apiClient.updateTask(updatedTask.id, updatedTask.title, updatedTask.description, updatedTask.completed);
      if (response.status === 401) {
        // Token might be expired, log out user
        logout();
        return;
      }

      if (response.data) {
        // Update with server response in case anything changed
        // After API response format change, response.data is the task object directly
        setTasks(prev => prev.map(t =>
          t.id === updatedTask.id ? response.data : t
        ));
        setEditingTask(null);
      } else {
        // Rollback if the server request failed
        setError(typeof response.error === 'string' ? response.error : 'Failed to update task');
        // Reload tasks to revert the optimistic update
        const reloadResponse = await apiClient.getTasks();
        if (reloadResponse.data) {
          setTasks(reloadResponse.data.tasks || []);
        }
      }
    } catch (error) {
      console.error('Error updating task:', error);
      setError('Failed to update task. Please try again.');
      // Reload tasks to revert the optimistic update
      try {
        const reloadResponse = await apiClient.getTasks();
        if (reloadResponse.data) {
          setTasks(reloadResponse.data.tasks || []);
        }
      } catch (reloadError) {
        console.error('Error reloading tasks:', reloadError);
      }
    }
  };

  const handleDeleteTask = async (id: string) => {
    // Optimistic update: remove the task from the list immediately
    const taskToDelete = tasks.find(t => t.id === id);
    setTasks(prev => prev.filter(t => t.id !== id));

    try {
      const response = await apiClient.deleteTask(id);
      if (response.status === 401) {
        // Token might be expired, log out user
        logout();
        return;
      }

      if (response.status !== 200) {
        // Rollback if the server request failed
        if (taskToDelete) {
          setTasks(prev => [taskToDelete, ...prev]);
        }
        setError(typeof response.error === 'string' ? response.error : 'Failed to delete task');
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task. Please try again.');
      // Rollback if the request threw an error
      if (taskToDelete) {
        setTasks(prev => [taskToDelete, ...prev]);
      }
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleCloseModal = () => {
    setEditingTask(null);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900">
        {/* Header */}
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
            <span className="text-lg font-semibold">Todo App</span>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {useAuth().user?.email || 'User'}</span>
              <a
                href="/logout"
                className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
              >
                Logout
              </a>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 py-8">
          <div className="mx-auto max-w-4xl px-6">
            <div className="mb-6">
              <h1 className="text-2xl font-bold">My Tasks</h1>
              <p className="text-gray-600">Manage your personal todo items</p>
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <p>{error}</p>
              </div>
            )}

            <CreateTaskForm onCreate={handleCreateTask} />

            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
              <TaskList
                tasks={tasks}
                onEdit={handleEditTask}
                onUpdate={handleUpdateTask}
                onDelete={handleDeleteTask}
                loading={loading}
                emptyMessage="No tasks yet. Create your first task above!"
              />
            </div>

            {editingTask && (
              <EditTaskModal
                task={editingTask}
                onSave={handleUpdateTask}
                onClose={handleCloseModal}
              />
            )}
          </div>
        </main>

        {/* Footer */}
        <footer className="border-t bg-white py-6">
          <div className="mx-auto max-w-6xl px-6 text-center">
            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} Todo App
            </p>
          </div>
        </footer>
      </div>
    </ProtectedRoute>
  );
};

export default TasksPage;