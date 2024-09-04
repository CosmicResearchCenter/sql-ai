from fastapi import FastAPI,APIRouter
from app.api import chat_router

app = FastAPI()

router = APIRouter()

router.include_router(chat_router, prefix="/chat", tags=["Chat"])

app.include_router(router, prefix="/api", tags=["sql-ai"])

import uvicorn

if __name__ == "__main__":
  config = uvicorn.Config("main:app", host="0.0.0.0", port=5001, reload=True)
  server = uvicorn.Server(config)
  server.run()