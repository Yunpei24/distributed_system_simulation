from fastapi import FastAPI
from routes.master_api import router
import uvicorn
#from models.model import ip_address

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.131.63", port=8000)