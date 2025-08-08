import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.tools import (authenticate_user, create_access_token,
                        decode_access_token)
from models import User
from schemas.user import UserBase, UserOut
from settings import get_db

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"Authorization": "Bearer"},
)


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credentials_exception

    data_payload = {"sub": str(user.id), "email": user.email, "is_admin": user.is_admin}
    access_token = create_access_token(payload=data_payload)
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_access_token(token)
    if not user:
        raise credentials_exception
    return user


def require_admin(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    return user


@app.get("/hello")
async def hello_user(
    username: str = Query("Anonymous", description="Ім'я користувача")
):
    return {"message": f"hello {username}"}


@app.get("/user/me")
async def user_me_data(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/user/admin/me")
async def only_for_admin(current_user: User = Depends(require_admin)):
    return {"is admin": current_user}


@app.post("/user", response_model=UserOut)
async def create_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)
