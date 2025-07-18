from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.prediction import Prediction, PredictionUpdate
from models.balance import Balance
from models.transaction import Transaction
from services.crud import prediction as PredictionService
from services.crud import user as UserService
from services.crud import balance as BalanceService
from services.crud import transaction as TransactionService
from services.rm import rm as RmTask
from typing import List, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)

prediction_route = APIRouter()

@prediction_route.post(
    '/create_prediction',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")
async def create_prediction(data: Prediction, session=Depends(get_session)) -> Dict[str, str]:
    """
    """
    try:
        balance = BalanceService.getbalance_by_user_id(data.user_id, session)
        if balance[0].value < 500:
            return {"result": "false", "message": "no limits"}
        else:
            prediction = Prediction(
                status='in_progress',
                user_id=data.user_id,
                image=data.image,
                result='in_progress'
            )
            result = PredictionService.create_prediction(prediction, session)
            task = RmTask.send_task(data.image, result.id)
            
            new_value = balance[0].value - 500
            
            new_balance = Balance(
                value=new_value,
                user_id=data.user_id,
            )
            transaction = Transaction(
                cost=500,
                type='out',
                user_id=data.user_id)
            TransactionService.create_transaction(transaction, session)
            BalanceService.updatebalance(new_balance, data.user_id, session)

            logger.info(f"New prediction: {data.user_id}, {data.status}, {task}")
            return {"result": "true"}

    except Exception as e:
        logger.error(f"Error during add_prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during add_prediction"
        )

@prediction_route.get(
    "/get_all_predictions_by_user_id",
    response_model=List[Prediction],
    summary="",
    response_description=""
)
async def get_all_predictions_by_user_id(user_id: int, session=Depends(get_session)) -> List[Prediction]:
    """l
    """
    try:
        user = UserService.get_user_by_id(user_id, session)
        predictions = PredictionService.get_all_predictions_by_user_id(user_id, session)
        logger.info(f"Retrieved {user}: {predictions}")
        return predictions
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving usetransactionsrs"
        )

@prediction_route.post(
    '/update_prediction',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="")   
async def update_prediction(data: PredictionUpdate, session=Depends(get_session)) -> Dict[str, str]:
    
    try:
        new_prediction = Prediction(
            result=data.result,
            status='done',
            id=data.id,
        )
        PredictionService.updateprediction(new_prediction, data.id, session)
        logger.info(f"Balance: {data.user_id}, {data.value}")
        return {"result": 'true'}

    except Exception as e:
        logger.error(f"Error during update_prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during prediction"
        )