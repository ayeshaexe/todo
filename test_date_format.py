#!/usr/bin/env python
"""
Test script to check the exact datetime format being sent by the backend
"""

from datetime import datetime, timezone

def test_datetime_serialization():
    # Test the Pydantic model datetime serialization directly
    from backend.validators.task_schema import TaskResponse
    from backend.models.task import Task

    # Create a sample task with timezone-aware datetime
    sample_datetime = datetime.now(timezone.utc)

    # Create a mock task object to test serialization
    print(f"Original datetime: {sample_datetime}")
    print(f"Datetime type: {type(sample_datetime)}")
    print(f"Datetime isoformat(): {sample_datetime.isoformat()}")

    # Test creating a Task object directly
    task_obj = Task(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id="test_user",
        created_at=sample_datetime,
        updated_at=sample_datetime
    )
    print(f"SQLModel Task object: {task_obj}")
    print(f"Created at: {task_obj.created_at}")
    print(f"Updated at: {task_obj.updated_at}")

    # Convert to dict to see how it would be serialized in Pydantic
    # Using dict() method which is compatible with older Pydantic versions
    task_dict = {k: v for k, v in task_obj.__dict__.items() if k in ['id', 'user_id', 'title', 'description', 'completed', 'created_at', 'updated_at']}
    print(f"Task attributes dict: {task_dict}")
    print(f"Created at in dict: {task_dict.get('created_at')}")
    print(f"Type of created_at in dict: {type(task_dict.get('created_at'))}")

    # Test conversion to Pydantic response model
    try:
        # For newer Pydantic versions
        task_response = TaskResponse.model_validate(task_obj)
    except AttributeError:
        # For older Pydantic versions, create from attributes
        task_response = TaskResponse(
            id=getattr(task_obj, 'id', 1),
            user_id=task_obj.user_id,
            title=task_obj.title,
            description=task_obj.description,
            completed=task_obj.completed,
            created_at=task_obj.created_at,
            updated_at=task_obj.updated_at
        )

    print(f"Pydantic TaskResponse: {task_response}")

    # Convert to dict to see serialization format
    try:
        task_dict_serialized = task_response.model_dump()
    except AttributeError:
        # For older Pydantic versions
        task_dict_serialized = task_response.dict()

    print(f"Serialized dict: {task_dict_serialized}")
    print(f"Created at in serialized dict: {task_dict_serialized.get('created_at')}")
    print(f"Type of created_at in serialized dict: {type(task_dict_serialized.get('created_at'))}")

if __name__ == "__main__":
    test_datetime_serialization()