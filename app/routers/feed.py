from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def feed_page():
    return "feed main paaaage"