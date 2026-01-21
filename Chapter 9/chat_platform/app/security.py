from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, WebSocketException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.ws_password_bearer import (
    OAuth2WebSocketPasswordBearer,
)

oauth2_scheme_for_ws = OAuth2WebSocketPasswordBearer(
    tokenUrl="/token"
)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "hashed_password": "hashedsecret2",
    }
}

def get_username_from_token(
        token: str = Depends(oauth2_scheme_for_ws),
) -> str:
    user = fake_token_resolver(token)
    if not user:
        raise WebSocketException(
            code = status.HTTP_401_UNAUTHORIZED,
            reason=(
                "Invalid authentication credentials"
            )
        )
    return user.username

class User(BaseModel):
    username: str

def fakely_hashed_password(password: str):
    return f"hashed{password}"

def fake_token_resolver(
        token: str,
) -> User | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user
    
def fake_token_generator(username: str) -> str:
    return f"tokenized{username}"
    
def get_user(
        db: dict[str, str], username: str
) -> User | None:
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    
router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_dict = fake_users_db.get(form_data.username)
    print(user_dict)
    print(form_data.username, form_data.password)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    hashed_password = fakely_hashed_password(
        form_data.password
    )
    print(hashed_password)
    if not hashed_password == user_dict.get('hashed_password'):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    
    token = fake_token_generator(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get('/login')
async def login_form(
    request: Request,
    redirecturl: Optional[str] = None,
) -> HTMLResponse:
    templates = Jinja2Templates(directory="templates")
    if redirecturl:
        context = {"redirection_url": redirecturl}
    else:
        context = {}
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=context,
    )