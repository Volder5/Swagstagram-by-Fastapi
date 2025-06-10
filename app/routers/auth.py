from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config.config import URLS
from app.forms.forms import LoginForm, RegisterForm, VerificationForm
from app.db.core import registrate_user, check_verification_code, check_user_exists, login_func, start_registration, if_code_not_expired_and_exists
from urllib.parse import urlencode

templates = Jinja2Templates(directory="app/templates/auth")
router = APIRouter()


@router.get("/login", name="login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None, message: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "urls": URLS,"message": message, "error": error})


@router.post("/login_post", name="login_post")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        if LoginForm(username=username, password=password):
            if login_func(username=username, input_password=password):
                return {"message": "Good boy!"}
            
            query_params = urlencode({"error": "Bad login!"})
            url = f"{URLS["login"]}?{query_params}"
            return RedirectResponse(url=url, status_code=302)


    except Exception as e:
        query_params = urlencode({"error": "Please enter valid info!"})
        url = f"{URLS["register"]}?{query_params}"
        return RedirectResponse(url=url, status_code=302)


    return {"message": "idk what need to happen so it works"}


@router.get("/register", name="register", response_class=HTMLResponse)
async def register_page(request: Request, error: str = None):
    return templates.TemplateResponse("register.html", {"request": request, "urls": URLS, "error": error})


@router.post("/register_post", name="register_post")
async def register_post(request: Request, username: str = Form(...), email: str = Form(...), password1: str = Form(...), password2: str = Form(...)):
    try:
        if RegisterForm(username=username, email=email, password1=password1, password2=password2):
            if not check_user_exists(username=username, email=email):
                token = start_registration(username, email, password1)
                url_token = urlencode({"token": token})
                url = f"{URLS["email-verification"]}?{url_token}"
                return RedirectResponse(url=url, status_code=302)
            else:
                query_params = urlencode({"error": "User is already exists!"})
                url = f"{URLS["register"]}?{query_params}"
                return RedirectResponse(url=url, status_code=302)

    except ValueError:
        query_params = urlencode({"error": "Passwords don't matches"})
        url = f"{URLS["register"]}?{query_params}"
        return RedirectResponse(url=url, status_code=302)

    except Exception as e:
        query_params = urlencode({"error": "Invalid credentials"})
        url = f"{URLS["register"]}?{query_params}"
        return RedirectResponse(url=url, status_code=302)

    return {"succes": "succes"}


@router.get("/recovery", name="recovery", response_class=HTMLResponse)
async def recovery_page(request: Request, token: str = None):
    return templates.TemplateResponse("recovery.html", {"request": request, "urls": URLS})


@router.get("/verification", name="email_verification", response_class=HTMLResponse)
async def verification_page(request: Request, token: str, error: str = None):
    return templates.TemplateResponse("email_verification.html", {"request": request, "urls": URLS, "token": token, "error": error})


@router.post("/verification_post", name="email_verification_post")
async def verification_page(request: Request, token: str, verification_code: int = Form(...)):
    try:
        if VerificationForm(verification_code=verification_code):
            
            if not if_code_not_expired_and_exists(token=token):
                query_params = urlencode(
                    {"error": "Code expired or doesn't exists!"})
                url = f"{URLS["register"]}?{query_params}"
                return RedirectResponse(url=url, status_code=302)
            
            if check_verification_code(token=token, input_code=verification_code):
                if registrate_user(token):
                    query_params = urlencode({"token": token, "message": "Succesful registration"})
                    url = f"{URLS["login"]}?{query_params}"
                    return RedirectResponse(url=url, status_code=302)
                else:
                    return {"error": "Coudn't registrate user"}

            else:
                query_params = urlencode(
                    {"token": token, "error": "Verification code is not correct!"})
                url = f"{URLS["email-verification"]}?{query_params}"
                return RedirectResponse(url=url, status_code=302)
    except Exception as e:
        query_params = urlencode(
            {"token": token, "error": "Invalid credentials"})
        url = f"{URLS["email-verification"]}?{query_params}"
        return RedirectResponse(url=url, status_code=302)
