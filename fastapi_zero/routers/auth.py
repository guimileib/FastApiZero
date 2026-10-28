from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import JwtToken
from fastapi_zero.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post("/token", status_code=HTTPStatus.OK, response_model=JwtToken)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = OAuth2Form,
    session=Session,
):
    # uso email para verificar, mas o campo chama username
    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    # verifico a senha do banco bate com a enviada no campo
    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token({"sub": user_db.email})
    return {"access_token": access_token, "token_type": "Bearer"}
