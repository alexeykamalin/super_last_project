from typing import Dict
from fastapi import APIRouter, HTTPException
from services.rm.rm import send_task

ml_route = APIRouter()

@ml_route.post(
    "/send_task", 
    response_model=Dict[str, str],
    summary="ML endpoint",
    description="Send ml request"
)
async def index(message:str, id: int) -> Dict[str, str]:
    try:
        send_task(message, id)
        return {"result": 'true'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
