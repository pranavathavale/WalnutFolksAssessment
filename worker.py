import time
from celery_app import celery
from model.transactions_db import update_transaction_processed


@celery.task(
    name="worker.process_transaction",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5}
)
def process_transaction(transaction_id):
    time.sleep(30)
    update_transaction_processed(transaction_id)
