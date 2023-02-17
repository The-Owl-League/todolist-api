from fastapi import FastAPI
from routers import v1


app = FastAPI()

app.include_router(v1.router)
