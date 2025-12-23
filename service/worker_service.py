from celery_app import celery

def enqueue_processing(transaction_id):
    celery.send_task(
        "worker.process_transaction",
        args=[transaction_id]
    )
