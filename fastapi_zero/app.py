from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_zero.models import User
from fastapi_zero.settings import Settings

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title="FastAPI Succeed")
database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá mundo!"}


@app.get(
    "/exercicio00", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def return_html():
    return """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>"""


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    session = Session(engine)
    # ou retorna User | None
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    
    if db_user:
        # Se ele já existir
        if db_user.username == user.username:
            raise HTTPException(
                deltail='Username alredy exists',
                status_code=HTTPStatus.CONFLICT
            )
        elif db_user.email == user.email:
            raise HTTPException(
            detail='Username alredy exists',
            status_code=HTTPStatus.CONFLICT
            )
    # Se nao der erro
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user) # adiciona na sessão
    session.commit() # efetiva a transação
    session.refresh(db_user) # traz o dado que ta dentro do banco de dados para sessão

    return db_user

@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


# para alterar dados
@app.put(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    # Se estou passando id 3, ele está na psoição 2 da lista,
    # pois ela começa em 0
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    "/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return database.pop(user_id - 1)


@app.get("/users/{user_id}", status_code=HTTPStatus.OK)
def read_user_name(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    user = database[user_id - 1]
    return {"username": user.username}
