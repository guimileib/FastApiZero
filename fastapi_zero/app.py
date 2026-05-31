from http import HTTPStatus

from fastapi import FastAPI

from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message, UserSchema, UserPublic, UserDB

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
def creat_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id
