from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from sqlmodel import Session
from routes.home import home_route
from routes.user import user_route
from routes.balance import balance_route
from routes.prediction import prediction_route
from routes.tranaction import transaction_route
from routes.ml import ml_route
from database.database import init_db
from database.config import get_settings
from models.user import User
from models.prediction import Prediction
from models.transaction import Transaction
from models.balance import Balance
from services.crud.user import create_user, get_all_users
from services.crud.transaction import create_transaction
from services.crud.prediction import create_prediction
from services.crud.balance import create_balance
import uvicorn
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(home_route, tags=['Home'])
    app.include_router(user_route, prefix='/api/users', tags=['Users'])
    app.include_router(transaction_route, prefix='/api/tranactions', tags=['Tranactions'])
    app.include_router(balance_route, prefix='/api/balance', tags=['Balance'])
    app.include_router(prediction_route, prefix='/api/prediction', tags=['Prediction'])
    app.include_router(ml_route, prefix='/api/ml', tags=['ML'])

    return app

app = create_application()
init_db(drop_all=True)

app.mount(
    "/static",
    StaticFiles(directory="/app/views/assets"), 
    name="static"
)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
    )
    uvicorn.run(
        'api:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
        log_level="info"
    )