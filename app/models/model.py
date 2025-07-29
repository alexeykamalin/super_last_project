from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

class MLModel:
    """
    Класс ML. Надеюсь модель будет получать картинку и возвращать есть ли на ней машина или нет.
    
    Attributes:
        Нужна помощь не понимаю, что тут  должно быть
    """
    
    def put_image(self) -> None:
        pass
    def get_prediction(self) -> None:
        pass
    def get_config(self) -> None:
        pass