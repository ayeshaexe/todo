from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
import sys
import os

# Add the backend directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from utils.jwt import get_current_user
from services.task_service import (
    create_task,
    get_tasks_by_user,
    get_task_by_id_and_user,
    update_task_by_id,
    update_task_completion,
    delete_task_by_id
)
from models.task import TaskCreate
from validators.task_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskToggleCompleteRequest,
    TaskResponse,
    TaskListResponse
)
from utils.response import success_response, error_response

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
async def create_new_task(
    task_request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Create a new task associated with the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Prepare task data for creation
        task_data = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            completed=False  # Default to false
        )

        # Create task using service
        db_task = create_task(db, task_data, user_id)

        # Return the task directly to match TaskResponse schema
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("CREATE_TASK_ERROR", f"Error creating task: {str(e)}")
        )


@router.get("/tasks", response_model=TaskListResponse)
async def get_user_tasks(
    status_filter: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional status filter
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Get tasks using service
        tasks = get_tasks_by_user(db, user_id, status_filter)

        # Return tasks directly to match TaskListResponse schema
        return {"tasks": tasks}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("FETCH_TASKS_ERROR", f"Error fetching tasks: {str(e)}")
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_specific_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get a specific task by ID if it belongs to the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Get task using service
        task = get_task_by_id_and_user(db, task_id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("TASK_NOT_FOUND", "Task not found or access denied")
            )

        # Return task directly to match TaskResponse schema
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("FETCH_TASK_ERROR", f"Error fetching task: {str(e)}")
        )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task_update: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Update a task if it belongs to the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Update task using service
        updated_task = update_task_by_id(
            db,
            task_id,
            user_id,
            title=task_update.title,
            description=task_update.description,
            completed=task_update.completed
        )

        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("TASK_NOT_FOUND", "Task not found or access denied")
            )

        # Return updated task directly to match TaskResponse schema
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("UPDATE_TASK_ERROR", f"Error updating task: {str(e)}")
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    completion_data: TaskToggleCompleteRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task if it belongs to the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Update task completion using service
        updated_task = update_task_completion(
            db,
            task_id,
            user_id,
            completed=completion_data.completed
        )

        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("TASK_NOT_FOUND", "Task not found or access denied")
            )

        # Return updated task directly to match TaskResponse schema
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("UPDATE_COMPLETION_ERROR", f"Error updating completion status: {str(e)}")
        )


@router.delete("/tasks/{task_id}")
async def delete_specific_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Delete a task if it belongs to the authenticated user
    """
    try:
        # Extract user_id from JWT token
        user_id = current_user.get("userId") or current_user.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_TOKEN", "Invalid token: missing user ID")
            )

        # Delete task using service
        deleted = delete_task_by_id(db, task_id, user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("TASK_NOT_FOUND", "Task not found or access denied")
            )

        # Return 204 No Content for successful deletion
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("DELETE_TASK_ERROR", f"Error deleting task: {str(e)}")
        )