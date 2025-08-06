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
import json

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
    print(f"Received data: {data}")
    print('lol')
    try:
        prediction = Prediction(
            status='in_progress',
            user_id=data.user_id,
            a1=data.a1,
            a2=data.a2,
            a3=data.a3,
            ag=data.ag,
            g1=data.g1,
            g2=data.g2,
            g3=data.g3,
            gg=data.gg,
            i1=data.i1,
            i2=data.i2,
            i3=data.i3,
            ia=data.ia,
            ig=data.ig,
            f1=data.f1,
            f2=data.f2,
            f3=data.f3,
            fa=data.fa,
            fg=data.fg,
            r1=data.r1,
            r2=data.r2,
            r3=data.r3,
            ra=data.ra,
            rg=data.rg,
            pri=data.pri,
            prm=data.prm,
            prf=data.prf,
            prr=data.prr,
            egkr=data.egkr,
            result='in_progress'
        )
        result = PredictionService.create_prediction(prediction, session)
        
        # Создаем словарь с данными для отправки
        task_data = {
            'a1': data.a1,
            'a2': data.a2,
            'a3': data.a3,
            'ag': data.ag,
            'g1': data.g1,
            'g2': data.g2,
            'g3': data.g3,
            'gg': data.gg,
            'i1': data.i1,
            'i2': data.i2,
            'i3': data.i3,
            'ia': data.ia,
            'ig': data.ig,
            'f1': data.f1,
            'f2': data.f2,
            'f3': data.f3,
            'fa': data.fa,
            'fg': data.fg,
            'r1': data.r1,
            'r2': data.r2,
            'r3': data.r3,
            'ra': data.ra,
            'rg': data.rg,
            'pri': data.pri,
            'prm': data.prm,
            'prf': data.prf,
            'prr': data.prr,
            'egkr': data.egkr
        }
        
        # Преобразуем словарь в строку JSON для отправки
        message = json.dumps(task_data)
        task = RmTask.send_task(message, result.id)
        
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