import uvicorn
from app.db.core import create_tables, insert_data, registrate_user, login_func


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # path to the FastAPI instance
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-reload on code changes (great for dev)
    )
    
