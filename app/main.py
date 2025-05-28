from fastapi import FastAPI
from app.routers import feed
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(feed.router, prefix="/feed", tags=["Feed"])