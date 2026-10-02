from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

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
