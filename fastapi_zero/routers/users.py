from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
    FilterPage,
)
from fastapi_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterPage = Annotated[FilterPage, Depends(filter_users)]


@router.get(
    "/exercicio00", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def return_html():
    return """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>"""


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        # Se ele já existir
        if db_user.username == user.username:
            raise HTTPException(
                detail="Username alredy exists",
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail="Email alredy exists",
                status_code=HTTPStatus.CONFLICT,
            )

    # Se nao der erro
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)  # adiciona na sessão
    session.commit()  # efetiva a transação
    session.refresh(
        db_user
    )  # traz o dado que ta dentro do banco de dados para sessão

    return db_user


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):

    users = session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {"users": users}


# para alterar dados
@router.put(
    "/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session=Session,
    current_user: User = CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            detail="Username or Email alredy exists",
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete("/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session=Session,
    current_user=CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted"}


# Endpoint Listagem de por Id
@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_name(user_id: int, session=Session):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    else:
        return user_db
