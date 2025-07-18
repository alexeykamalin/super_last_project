from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from models.transaction import Transaction


def get_all_transactions_by_user_id(user_id: int, session: Session) -> List['Transaction']:
    """
    """
    try:
        statement = select(Transaction).where(Transaction.user_id == user_id)
        transactions = session.exec(statement).all()
        return transactions
    except Exception as e:
        raise

def get_transaction_by_id(transaction_id: int, session: Session) -> Optional['Transaction']:
    """
    """
    try:
        statement = select(Transaction).where(Transaction.id == transaction_id)
        transaction = session.exec(statement).all()
        return transaction
    except Exception as e:
        raise


def create_transaction(transaction: Transaction, session: Session) -> Transaction:
    """
    """
    try:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
    except Exception as e:
        session.rollback()
        raise