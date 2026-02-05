from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import traceback

async def error_handler(request: Request, call_next: Callable[[Request], Awaitable]) -> JSONResponse:
    """
    Global error handler middleware for consistent error responses
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        # Handle HTTP exceptions with standard error format
        if isinstance(e.detail, dict):
            # Detail is already in our standard format
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )

        # Convert to standard error format
        error_content = {
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(e.detail)
            }
        }
        return JSONResponse(
            status_code=e.status_code,
            content=error_content
        )
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())

        error_content = {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error occurred"
            }
        }
        return JSONResponse(
            status_code=500,
            content=error_content
        )