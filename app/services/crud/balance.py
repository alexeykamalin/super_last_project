from sqlmodel import Session, select, update
from typing import List, Optional
from datetime import datetime
from models.balance import Balance



def create_balance(balance: Balance, session: Session) -> Balance:
    """
    """
    try:
        session.add(balance)
        session.commit()
        session.refresh(balance)
        return balance
    except Exception as e:
        session.rollback()
        raise

def getbalance_by_user_id(user_id: int, session: Session) -> Balance:

    """
    """
    try:
        statement = select(Balance).where(Balance.user_id == user_id)
        balance = session.exec(statement).all()
        return balance
    except Exception as e:
        raise

def updatebalance(balance: Balance, user_id: int, session: Session) -> Balance:
    """
    """
    try:
        new_balance = session.exec(select(Balance).where(Balance.user_id == user_id)).one()
        new_balance.value = balance.value
        session.commit()
        return balance
    except Exception as e:
        session.rollback()
        raise