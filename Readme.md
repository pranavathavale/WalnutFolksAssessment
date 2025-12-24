You do not need to run anything locally.
You can directly call the APIs using the following endpoints:
POST ENDPOINT
1. https://walnutfolksassessment.onrender.com/v1/webhooks/transactions
I have already created following transactions:
{
    "transaction_id": "txn_abc123def456" & "txn_abc123def4567" 
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR"
} 

GET ENDPOINT
2. https://walnutfolksassessment.onrender.com/v1/transactions/txn_abc123def4567

HEALTH ENDPOINT
3. https://walnutfolksassessment.onrender.com

NOTE: I am using render of free tier if inactive for 15 mins it puts my web service to sleep. 
Kindly, use the health endpoint link using browser to wake up the service before testing the assessment.
Still, in case of any issues, please let me know I will restart the service.

Requirements as per the pdf :
1. Must return 202 to indicate immediate acceptance
2. body can be empty or contain a simple acknowledgement
3. Process each transaction after receiving webhook after 30 secs delay.
4. Store in persistent storage
5. Multiple webhooks with same transaction id should only result in one processed transaction.
6. Handle gracefully without errors or duplicate processing.
7. Store processed transactions with their status and timing info.


DESIGN & ARCHITECTURE:
FRAMEWORKS & CLOUD INFRA:-
1. FastAPI -> To expose API endpoints.
2. Celery -> Python based distributed task queue system. Listens to redis and executes pending tasks in background.
3. Redis -> Using it as message broker for celery so even if web service crash task is not lost which is a key requirement.
4. PostgreSQL -> Persistent storage.
5. Render -> Cloud hosting. 


WORKFLOW:-
1. Webhook triggered
2. Perform validation to check all fields before storing the transaction in db with status as "PROCESSING"
   If a duplicate transaction id then it's ignored. 
   Using enqueue_processing, celery sends the task to redis.
   Immediately responds with 202.
3. Worker then executes the tasks asynchronously and retires up to 3 times in case of failure.
   Using time.sleep() to simulate 30 secs delay.