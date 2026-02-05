from typing import Any, Dict, Optional
from fastapi import HTTPException, status

def success_response(data: Any = None, message: str = "", status_code: int = 200) -> Dict[str, Any]:
    """
    Create a standardized success response
    """
    response = {
        "success": True,
        "data": data,
        "message": message
    }
    return response

def error_response(error_code: str = "", error_message: str = "", status_code: int = 400) -> Dict[str, Any]:
    """
    Create a standardized error response
    """
    response = {
        "success": False,
        "error": {
            "code": error_code,
            "message": error_message
        }
    }
    return response

def handle_error(message: str, status_code: int = 400, error_code: str = "GENERIC_ERROR"):
    """
    Raise an HTTP exception with standardized error format
    """
    raise HTTPException(
        status_code=status_code,
        detail=error_response(error_code, message, status_code)
    )