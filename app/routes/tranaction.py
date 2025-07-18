from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.user import User
from models.transaction import Transaction
from services.crud import user as UserService
from services.crud import transaction as TransactionService
from typing import List, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)

transaction_route = APIRouter()

@transaction_route.post(
    '/add_transaction',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")
async def add_transaction(data: Transaction, user_id: int, session=Depends(get_session)) -> Dict[str, str]:
    """
    """
    try:
        transaction = Transaction(
            type=data.type,
            cost=data.cost,
            user_id=user_id,
        )
        TransactionService.create_transaction(transaction, session)
        logger.info(f"New transaction: {user_id}, {data.cost}, {data.type}")
        return {"message": "New transaction complite"}

    except Exception as e:
        logger.error(f"Error during add_tranaction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during add_tranaction"
        )

@transaction_route.get(
    "/get_all_tranactions_by_user_id",
    response_model=List[Transaction],
    summary="",
    response_description=""
)
async def get_all_tranactions_by_user_id(user_id: int, session=Depends(get_session)) -> List[Transaction]:
    """
    """
    try:
        user = UserService.get_user_by_id(user_id, session)
        transactions = TransactionService.get_all_transactions_by_user_id(user_id, session)
        logger.info(f"Retrieved {user}: {transactions}")
        return transactions
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving usetransactionsrs"
        )