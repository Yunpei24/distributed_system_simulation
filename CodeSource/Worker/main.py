from fastapi import FastAPI
from routes.worker import router, do_task
import uvicorn

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    do_task()