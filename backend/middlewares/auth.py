from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from utils.jwt import verify_token

# Initialize security scheme
security = HTTPBearer(auto_error=False)

async def auth_middleware(credentials: HTTPAuthorizationCredentials = None) -> Dict[str, Any]:
    """
    Authentication middleware to verify JWT tokens and extract user information
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        user_data = verify_token(token)
        return user_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )