from fastapi import FastAPI
from app.routers import feed, auth
from fastapi.staticfiles import StaticFiles
from app.db import models


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(feed.router, prefix="/feed", tags=["Feed"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])



