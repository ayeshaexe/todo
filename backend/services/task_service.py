from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import sys
import os

# Add the backend directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import Task, TaskCreate
from validators.task_schema import TaskResponse


def create_task(db_session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task associated with the authenticated user
    """
    from datetime import datetime, timezone

    # Create task instance with all required fields to avoid default_factory issues
    now = datetime.now(timezone.utc)
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id,
        created_at=now,
        updated_at=now
    )

    # Add to session and commit
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task


def get_tasks_by_user(
    db_session: Session,
    user_id: str,
    status_filter: Optional[str] = None
) -> List[Task]:
    """
    Get all tasks for a specific user with optional status filter
    """
    query = select(Task).where(Task.user_id == user_id)

    if status_filter:
        if status_filter.lower() == "completed":
            query = query.where(Task.completed == True)
        elif status_filter.lower() == "pending":
            query = query.where(Task.completed == False)
        # If "all" or any other value, return all tasks

    tasks = db_session.exec(query).all()
    return tasks


def get_task_by_id_and_user(db_session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID and ensure it belongs to the authenticated user
    """
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db_session.exec(query).first()
    return task


def update_task_by_id(
    db_session: Session,
    task_id: int,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Optional[Task]:
    """
    Update a task if it belongs to the authenticated user
    """
    from datetime import datetime, timezone
    task = get_task_by_id_and_user(db_session, task_id, user_id)
    if not task:
        return None

    # Update fields if provided
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    task.updated_at = datetime.now(timezone.utc)

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task


def update_task_completion(
    db_session: Session,
    task_id: int,
    user_id: str,
    completed: bool
) -> Optional[Task]:
    """
    Update task completion status if it belongs to the authenticated user
    """
    from datetime import datetime, timezone
    task = get_task_by_id_and_user(db_session, task_id, user_id)
    if not task:
        return None

    task.completed = completed
    task.updated_at = datetime.now(timezone.utc)

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    return task


def delete_task_by_id(db_session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task if it belongs to the authenticated user
    """
    task = get_task_by_id_and_user(db_session, task_id, user_id)
    if not task:
        return False

    db_session.delete(task)
    db_session.commit()

    return True