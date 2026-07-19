from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


# yield faz uma condição de parada,
# ele fecha a conexao depois de retornar o dado
def get_session():
    with Session(engine) as session:
        yield session
