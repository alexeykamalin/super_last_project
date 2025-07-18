from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.database import get_session, get_settings
from models.user import TokenResponse, User, DeleteUser
from services.crud import user as UserService
from services.crud import balance as BalanceService
from models.user import UserSignup
from models.balance import Balance

from typing import List, Dict
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

user_route = APIRouter()

@user_route.post(
    '/signup',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with email and password")
async def signup(data: UserSignup, session=Depends(get_session)) -> Dict[str, str]:
    try:
        if UserService.get_user_by_email(data.email, session):
            logger.warning(f"Signup attempt with existing email: {data.email}")
            return {"result": "false",'detail': "User with this email already exists"}
        user = User(
            email=data.email,
            password=HashPassword().create_hash(data.password),
            name=data.name)
        new_user = UserService.create_user(user, session)
        balance = Balance(value=0, creator=new_user, user_id=new_user.id)
        BalanceService.create_balance(balance, session)
        logger.info(f"New user registered: {data.email}")
        return {"result": "true"}

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@user_route.post("/signin")
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict: 
    user_exist = UserService.get_user_by_email(user.username, session)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    if HashPassword().verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(key="token", value=access_token, httponly=True)
        return response 

    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

@user_route.post("/logout")
async def logout_user() -> dict: 
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("token")
    return response 

@user_route.get(
    "/get_all_users",
    response_model=List[User],
    summary="Get all users",
    response_description="List of all users"
)
async def get_all_users(session=Depends(get_session)) -> List[User]:
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        users = UserService.get_all_users(session)
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )
    
@user_route.post(
    '/create_user',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")  
async def create_user(data: User, session=Depends(get_session)) -> Dict[str, str]:
    """
    """
    try:
        user = User(
            email=data.email,
            password=data.password,
            name=data.name,
            is_admin=data.is_admin,
        )
        new_user = UserService.create_user(user, session)
        logger.info(f"New user: {new_user.id}")
        return {"message": "New user complite"}

    except Exception as e:
        logger.error(f"Error during create_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during create_user"
        )

@user_route.post(
    '/delete_user',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")  
async def delete_user(data: DeleteUser, session=Depends(get_session)) -> Dict[str, str]:
    """
    """
    try:
        UserService.delete_user(data.user_id, session)
        logger.info(f"user deleted: {data.user_id}")
        return {"result": "true"}

    except Exception as e:
        logger.error(f"Error during delete_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during delete_user"
        )