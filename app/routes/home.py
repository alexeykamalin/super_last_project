from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from auth.authenticate import authenticate_cookie, authenticate
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.database import get_session
from services.auth.loginform import LoginForm
from services.crud import user as UsersService
from services.crud import balance as BalanceService
from services.crud import transaction as TransactionService
from services.crud import prediction as PredictionService
from database.config import get_settings
from typing import Dict

settings = get_settings()
home_route = APIRouter()
hash_password = HashPassword()
templates = Jinja2Templates(directory='views')

@home_route.get(
    "/", 
    response_class=HTMLResponse
)
async def index(request: Request, session=Depends(get_session)):
    token = request.cookies.get('token')
    if token is not None:
        user = await authenticate_cookie(token)

        cur_user = UsersService.get_user_by_email(user, session)
        if cur_user.is_admin:
            users = UsersService.get_all_users(session)
        else:
            users = []
        balance = BalanceService.getbalance_by_user_id(cur_user.id, session)
        context = {
            "balance": balance,
            "user": cur_user,
            "users": users,
            "request": request
        }
        return templates.TemplateResponse("index.html", context)
    else:
        context = {
            "result": False,
            "request": request
        }
        return templates.TemplateResponse("login.html", context)

@home_route.get(
    "/registration", 
    response_class=HTMLResponse
)
async def index(request: Request, session=Depends(get_session)):
    token = request.cookies.get('token')
    if token:
        user = await authenticate_cookie(token)
        cur_user = UsersService.get_user_by_email(user, session)
        balance = BalanceService.getbalance_by_user_id(cur_user.id, session)
        context = {
            "balance": balance,
            "user": cur_user,
            "request": request
        }
        return templates.TemplateResponse("index.html", context)
    else:
        context = {
            "result": False,
            "request": request
        }
        return templates.TemplateResponse("registration.html", context)
    
@home_route.get(
    "/transactions", 
    response_class=HTMLResponse
)
async def transaction(request: Request, session=Depends(get_session)):
    token = request.cookies.get('token')
    if token:
        user = await authenticate_cookie(token)
        cur_user = UsersService.get_user_by_email(user, session)
        balance = BalanceService.getbalance_by_user_id(cur_user.id, session)
        tranactions = TransactionService.get_all_transactions_by_user_id(cur_user.id, session)
        context = {
            "transactions": tranactions,
            "user": cur_user,
            "request": request,
            "balance": balance
        }
        return templates.TemplateResponse("transactions.html", context)
    else:
        context = {
            "result": False,
            "request": request
        }
        return templates.TemplateResponse("login.html", context)

@home_route.get(
    "/predictions", 
    response_class=HTMLResponse
)
async def prediction(request: Request, session=Depends(get_session)):
    token = request.cookies.get('token')
    if token:
        user = await authenticate_cookie(token)
        cur_user = UsersService.get_user_by_email(user, session)
        balance = BalanceService.getbalance_by_user_id(cur_user.id, session)
        predictions = PredictionService.get_all_predictions_by_user_id(cur_user.id, session)
        context = {
            "predictions": predictions,
            "user": cur_user,
            "request": request,
            "balance": balance
        }
        return templates.TemplateResponse("predictions.html", context)
    else:
        context = {
            "result": False,
            "request": request
        }
        return templates.TemplateResponse("login.html", context)

@home_route.get(
    "/health",
    response_model=Dict[str, str],
    summary="Health check endpoint",
    description="Returns service health status"
)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.

    Returns:
        Dict[str, str]: Health status message
    
    Raises:
        HTTPException: If service is unhealthy
    """
    try:
        # Add actual health checks here
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail="Service unavailable"
        )

