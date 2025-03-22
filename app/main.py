import uvicorn
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="RESTfulAPI",
    description="A FastAPI application",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RESTfulAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
