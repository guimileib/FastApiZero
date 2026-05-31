from http import HTTPStatus

from fastapi import FastAPI

from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message, UserSchema, UserPublic

app = FastAPI(title='FastAPI Succeed')


@app.get("/", 
        status_code=HTTPStatus.OK, 
        response_model=Message)
def read_root():
    return {"message": "Olá mundo!"}


@app.get(
    "/exercicio00", 
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse
)
def return_html():
    return """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>"""

@app.post(
    "/users/", 
    status_code=HTTPStatus.CREATED, 
    response_model=UserPublic
)
def creat_user(user: UserSchema):
    return user
