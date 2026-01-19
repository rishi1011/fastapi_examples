from fastapi import APIRouter, Depends, HTTPException, WebSocketException, status
from fastapi.security import OAuth2PasswordRequestForm
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
        "hashedpassword": "hashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "hashedpassword": "hashedsecret2",
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
    if not user_dict:
        raise HTTPException(
            status_code=404,
            detail="Incorrect username and password",
        )
    hashed_password = fakely_hashed_password(
        form_data.password
    )
    