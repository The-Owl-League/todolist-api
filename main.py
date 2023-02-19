from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import v1


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://192.168.0.210:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)
