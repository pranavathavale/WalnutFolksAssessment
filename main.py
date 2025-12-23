from fastapi import FastAPI
from datetime import datetime, timezone
from controller.webhook_controller import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }
