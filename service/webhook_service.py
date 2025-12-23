from model.transactions_db import insert_transaction, fetch_transaction
from service.worker_service import enqueue_processing
from fastapi import HTTPException

REQUIRED_FIELDS = {
    "transaction_id",
    "source_account",
    "destination_account",
    "amount",
    "currency"
}

def create_transaction(payload: dict):
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing fields: {', '.join(missing)}"
        )

    insert_transaction(payload)
    enqueue_processing(payload["transaction_id"])


def get_transaction(transaction_id: str):
    transaction =  fetch_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction