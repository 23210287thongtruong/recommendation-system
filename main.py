from fastapi import FastAPI
from api.routes.books import router

app = FastAPI()

app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Hello from recommendation-system!"}
