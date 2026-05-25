from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá mundo!"}


@app.get(
    "/exercicio00", status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def read_root2():
    return """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>"""
