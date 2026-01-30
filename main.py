from fastapi import FastAPI
from database import engine
from routers import booking
from fastapi.middleware.cors import CORSMiddleware

import models

app = FastAPI()

origins = [
    "http://localhost:4200",  # Angular
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # CRA/Next dev
    "https://yourdomain.com",  # production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for local-only testing (see note below)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # Authorization, Content-Type, etc
)

models.Base.metadata.create_all(bind=engine)
app.include_router(booking.router, prefix='/api')
