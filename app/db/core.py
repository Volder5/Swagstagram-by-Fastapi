from app.db.models import metadata_obj
from app.db.database import engine
from sqlalchemy import text
import bcrypt
import secrets
import hashlib
import random
from app.config.utils import send_email


def create_tables():
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)


def insert_data():
    with engine.connect() as conn:
        stmnt = """INSERT INTO users (username) VALUES (:u1), (:u2);"""
        conn.execute(text(stmnt), {"u1": "Bobr", "u2": "Volk"})
        conn.commit()


def registrate_user(token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    with engine.connect() as conn:
        stmnt = """SELECT username, email, password FROM users_on_verification WHERE token = :token;"""
        result = conn.execute(text(stmnt), {"token": hashed_token})
        rows = result.fetchall()
        data = [dict(row._mapping) for row in rows]
        
        stmnt = """DELETE FROM users_on_verification WHERE token = :token;"""
        conn.execute(text(stmnt), {"token": hashed_token})
        stmnt = """DELETE FROM email_verification WHERE token = :token;"""
        conn.execute(text(stmnt), {"token": hashed_token})
        
        for user in data:
            insert_stmt = """
                INSERT INTO users (username, email, password)
                VALUES (:username, :email, :password)
            """
            conn.execute(text(insert_stmt), {
                "username": user["username"],
                "email": user["email"],
                "password": user["password"]
            })

        conn.commit()

    return data if data else {"False": False}


def login_func(username, input_password):
    with engine.connect() as conn:
        stmnt = """SELECT password FROM users WHERE username = :username"""
        get_actual_password = conn.execute(
            text(stmnt), {"username": username}).fetchone()
        actual_password = get_actual_password[0]

    is_password_passes = bcrypt.checkpw(str(input_password).encode(
        "utf-8"), str(actual_password).encode("utf-8"))


def create_verification_code(email, username):
    token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    verification_code = random.randint(100000, 999999)

    with engine.connect() as conn:
        stmnt = """INSERT INTO email_verification (email, token, verification_code) VALUES (:email, :token, :verification_code);"""
        conn.execute(text(stmnt), {
                     "email": email, "token": hashed_token, "verification_code": verification_code})
        conn.commit()

    email_text = f"Hello dear {username}!\nHere is your verification code: {verification_code}"
    send_email(to_email=email, subject="Welcome to Swagstargram!",
               content=email_text)

    return token


def check_verification_code(token, input_code):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    with engine.connect() as conn:
        stmnt = """SELECT verification_code FROM email_verification WHERE token = :token"""
        verification_code = conn.execute(
            text(stmnt), {"token": hashed_token}).fetchone()
        if verification_code[0] == input_code:
            return True
        else:
            return False


def user_on_verification(username, password, email, token):
    with engine.connect() as conn:
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        hashed_password = bcrypt.hashpw(str(password).encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")
        stmnt = """INSERT INTO users_on_verification (username, email, password, token) VALUES (:username, :email, :password, :token);"""
        conn.execute(text(stmnt), {"username": username, "email": email,
                     "password": hashed_password, "token": hashed_token})
        conn.commit()
