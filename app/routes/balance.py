from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.user import User
from models.balance import Balance, BalanceUpdate
from models.transaction import Transaction
from services.crud import user as UserService
from services.crud import balance as BalanceService
from services.crud import transaction as TransactionService
from typing import List, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)

balance_route = APIRouter()

@balance_route.post(
    '/add_balance',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")
async def add_balance(data: Balance, user_id: int, session=Depends(get_session)) -> Dict[str, str]:
    """
    """
    try:
        balance = Balance(
            value=data.value,
            user_id=user_id,
        )
        BalanceService.create_balance(balance, session)
        logger.info(f"New Balance: {user_id}, {data.value}")
        return {"message": "New balance complite"}

    except Exception as e:
        logger.error(f"Error during add_balance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during balance"
        )

@balance_route.get(
    '/get_balance_by_user_id',
    response_model=List[Balance],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")   
async def get_balance_by_user_id(user_id: int, session=Depends(get_session)) -> Balance:
    """l
    """
    try:
        user = UserService.get_user_by_id(user_id, session)
        balance = await BalanceService.getbalance_by_user_id(user_id, session)
        logger.info(f"Retrieved {user}: {balance}")
        return balance
    except Exception as e:
        logger.error(f"Error retrieving balance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving userbalance"
        )

@balance_route.post(
    '/update_balance',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")   
async def update_balance(data: BalanceUpdate, session=Depends(get_session)) -> Dict[str, str]:
    
    try:
        balance = BalanceService.getbalance_by_user_id(data.user_id, session)
        new_balance = Balance(
            value=balance[0].value + data.value,
            user_id=data.user_id,
        )
        transaction = Transaction(
            cost=data.value,
            type='in',
            user_id=data.user_id)
        TransactionService.create_transaction(transaction, session)
        BalanceService.updatebalance(new_balance, data.user_id, session)
        logger.info(f"Balance: {data.user_id}, {data.value}")
        return {"result": 'true'}

    except Exception as e:
        logger.error(f"Error during update_balance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during balance"
        )