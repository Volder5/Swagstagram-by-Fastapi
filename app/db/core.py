from app.db.models import metadata_obj
from app.db.database import engine
from sqlalchemy import text
import bcrypt
import secrets
import hashlib
import random
from datetime import datetime, timedelta
from app.config.utils import send_email
from app.config.config import URLS
from urllib.parse import urlencode


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

    return data if data else False


def login_func(username, input_password):
    with engine.connect() as conn:
        stmnt = """SELECT password FROM users WHERE username = :username"""
        get_actual_password = conn.execute(
            text(stmnt), {"username": username}).fetchone()
        actual_password = get_actual_password[0]

    is_password_passes = bcrypt.checkpw(str(input_password).encode(
        "utf-8"), str(actual_password).encode("utf-8"))

    return is_password_passes


def start_registration(username, email, password):
    """
    Starts registration by inserting data to table 'users_on_verification',
    creating verification code and token,
    returns registration token.
    """
    with engine.connect() as conn:

        token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        verification_code = random.randint(100000, 999999)

        hashed_password = bcrypt.hashpw(str(password).encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")

        stmnt = """INSERT INTO users_on_verification (username, email, password, token, verification_code) VALUES (:username, :email, :password, :token, :verification_code);"""
        conn.execute(text(stmnt), {"username": username, "email": email, "password": hashed_password,
                     "token": hashed_token, "verification_code": verification_code})
        conn.commit()

    email_text = f"Hello dear {username}!\nHere is your verification code: {verification_code}"
    send_email(to_email=email, subject="Welcome to Swagstargram!",
               content=email_text)

    return token


def if_code_not_expired_and_exists(token):

    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    with engine.connect() as conn:
        stmnt = """SELECT created_at FROM users_on_verification WHERE token = :token"""
        created_at = conn.execute(
            text(stmnt), {"token": hashed_token}).fetchone()

        current_time = datetime.now()
        five_minutes = current_time - timedelta(minutes=5)

        if created_at[0] > five_minutes:
            return True

        else:
            stmnt = """DELETE FROM users_on_verification WHERE token = :token;"""
            conn.execute(text(stmnt), {"token": hashed_token})
            conn.commit()
            return False


def check_verification_code(token, input_code):

    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    with engine.connect() as conn:
        stmnt = """SELECT verification_code FROM users_on_verification WHERE token = :token"""
        verification_code = conn.execute(
            text(stmnt), {"token": hashed_token}).fetchone()
        if verification_code[0] == input_code:
            return True
        else:
            return False


def check_user_exists(username, email):
    with engine.connect() as conn:
        stmnt = """
            SELECT id FROM users 
            WHERE username = :username OR email = :email;
        """
        result = conn.execute(text(stmnt), {
            "username": username,
            "email": email
        }).fetchone()

    return result is not None


def start_recovery(email):
    token = secrets.token_urlsafe(32)
    with engine.connect() as conn:
        stmnt = """SELECT id FROM users WHERE email = :email"""
        user = conn.execute(text(stmnt), {"email": email}).fetchone()
        
        if not user[0]:
            return {"error": "User doesn't exist", "status": "Failed"}
        
        stmnt = """INSERT INTO recovery (email, token) VALUES (:email, :token)"""
        conn.execute(text(stmnt), {"email": email, "token": token})
        conn.commit()
        
        stmnt = """SELECT username FROM users WHERE email = :email"""
        username = conn.execute(text(stmnt), {"email": email}).fetchone()
        
        url_token = urlencode({"token": token})
        url = f"{URLS["recovery"]}?{url_token}"
        link = f"127.0.0.1:8000{url}"
        send_email(email, "Recovery for your Swagstargram Account:", f"Hello dear {username[0]},\n We got recovery request for your account, here is link that you can use {link}")


def check_recovery_token_valid(token):
    with engine.connect() as conn:
        stmnt = """SELECT created_at FROM recovery WHERE token = :token"""
        created_at = conn.execute(
            text(stmnt), {"token": token}).fetchone()

        current_time = datetime.now()
        five_minutes = current_time - timedelta(minutes=5)
        try:
            if created_at[0] > five_minutes:
                return True

            else:
                stmnt = """DELETE FROM recovery WHERE token = :token;"""
                conn.execute(text(stmnt), {"token": token})
                conn.commit()
                return False
            
        except Exception:
            return False
        

def change_password_recovery(token, password):
    with engine.connect() as conn:
        stmnt = """SELECT email FROM recovery WHERE token = :token"""
        email = conn.execute(text(stmnt), {"token": token}).fetchone()
        
        try:
            if email:
                pass
            
        except Exception:
            return False
        
        hashed_password = bcrypt.hashpw(str(password).encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")

        stmnt = """UPDATE users SET password = :password WHERE email = :email"""
        conn.execute(text(stmnt), {"password": hashed_password, "email": email[0]})
        stmnt = """DELETE FROM recovery WHERE email = :email;"""
        conn.execute(text(stmnt), {"email": email[0]})
        conn.commit()
        
        return True
        

