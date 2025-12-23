from fastapi import APIRouter, HTTPException
from service.webhook_service import create_transaction, get_transaction

router = APIRouter(prefix="/v1")

@router.post("/webhooks/transactions", status_code=202)
def receive_webhook(payload: dict):
    create_transaction(payload)
    return

@router.get("/transactions/{transaction_id}")
def fetch_transaction(transaction_id: str):
    return get_transaction(transaction_id)