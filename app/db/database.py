from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(
    url=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True,
    pool_size=5,
    max_overflow=10
)

with engine.connect() as conn: 
    res = conn.execute(text("SELECT VERSION()"))
    print(f"{res.first()}")
    
    
