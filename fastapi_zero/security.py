from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User

# direcionamento para endpoint /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# provisorio
SECRET_KEY = "reguacabelo123"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()


# le a função limpa e gera o hash
def get_password_hash(password: str):
    return pwd_context.hash(password)  # transforma a senha em um hash


# função que valida encripta e vê se é a mesma coisa
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password, hashed_password
    )  # chama o contexto, chama o verificador


# compara a senha com o hash que tem no banco de dados
def create_acess_token(data: dict):
    # data = {'sub': email, ...}
    to_encode = data.copy()  # aqui é a claim
    # calculando a hora de agora, para durar 30 minutos
    # do tempo que for chamado + o tempo do token expirar
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    # retorne o tempo de expiração
    to_encode.update({"exp": expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# funcao para verificar o que veio do usuario
def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # tentamos fazer decode do token, mas pode
        # ser que enviem coisas que nao sejam token
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user_db = session.scalar(
            select(User).where(User.email == subject_email)
    )

    if not user_db:
        raise credentials_exception

    return user_db
