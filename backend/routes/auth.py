from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from typing import Dict, Optional
import uuid
from datetime import datetime, timedelta, timezone
from config.settings import settings
from utils.jwt import create_access_token
from db import get_session
from utils.response import success_response, error_response
from models.user import User, UserCreate
from passlib.context import CryptContext

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# For demo purposes, we'll use an in-memory store
# In a real application, you'd use a proper user database
user_store = {}

from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(
    request: SignupRequest,
    db: Session = Depends(get_session)
):
    """
    Register a new user
    """
    try:
        # Check if user already exists in database
        existing_user = db.exec(select(User).where(User.email == request.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response("USER_EXISTS", "User with this email already exists")
            )

        # Hash the password
        password_hash = pwd_context.hash(request.password)

        # Create new user in database
        current_time = datetime.now(timezone.utc)
        user_id = str(uuid.uuid4())
        db_user = User(
            id=user_id,
            email=request.email,
            name=request.name or request.email.split("@")[0],  # Use part of email as name if none provided
            created_at=current_time,
            updated_at=current_time,
            password_hash=password_hash
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create JWT token
        token_data = {
            "sub": db_user.id,
            "email": db_user.email,
            "name": db_user.name
        }
        jwt_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(hours=1)  # Token valid for 1 hour
        )

        # Prepare response
        user_response = {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "created_at": db_user.created_at.isoformat() if hasattr(db_user.created_at, 'isoformat') else str(db_user.created_at),
            "updatedAt": db_user.updated_at.isoformat() if hasattr(db_user.updated_at, 'isoformat') else str(db_user.updated_at)
        }

        return success_response(
            data={
                "user": user_response,
                "jwt_token": jwt_token
            },
            message="User registered successfully",
            status_code=201
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("SIGNUP_ERROR", f"Error during signup: {str(e)}")
        )


@router.post("/auth/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token
    """
    try:
        # Check if user exists in database
        db_user = db.exec(select(User).where(User.email == request.email)).first()

        if not db_user or not pwd_context.verify(request.password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_CREDENTIALS", "Invalid email or password")
            )

        # Create JWT token
        token_data = {
            "sub": db_user.id,
            "email": db_user.email,
            "name": db_user.name
        }
        jwt_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(hours=1)  # Token valid for 1 hour
        )

        # Prepare response
        user_response = {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "created_at": db_user.created_at.isoformat() if hasattr(db_user.created_at, 'isoformat') else str(db_user.created_at),
            "updatedAt": db_user.updated_at.isoformat() if hasattr(db_user.updated_at, 'isoformat') else str(db_user.updated_at)
        }

        return success_response(
            data={
                "user": user_response,
                "jwt_token": jwt_token
            },
            message="Login successful"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("LOGIN_ERROR", f"Error during login: {str(e)}")
        )


@router.post("/auth/logout")
async def logout(authorization: str = Depends(HTTPBearer(auto_error=False))):
    """
    Logout user (currently just a placeholder - in a real app, you might add the token to a blacklist)
    """
    try:
        return success_response(
            message="Logout successful"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("LOGOUT_ERROR", f"Error during logout: {str(e)}")
        )