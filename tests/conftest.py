import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import table_registry

from sqlalchemy import event
from fastapi_zero.models import User 

"""
Esse teste tem 3 etapas (AAA)
- A: Arrange - Arranjo - Carregar dados
- A: Act - Chama o bloco de código executa (SUT)
- A: Assert - Garanta que A é A
"""


@pytest.fixture
def client():
    # Arrange
    return TestClient(app)


@pytest.fixture
def session():
    # criando a engine via memoria
    engine = create_engine("sqlite:///:memory:")
    # criando de fato a estrutura de banco em memoria
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # retorna um de cada vez ao inves de todos

    table_registry.metadata.drop_all(engine)  # depois que usar deleta todas

def _mock_db_item():
    
    def fake_time_hook(mapper, connection, target):
        ...    
    
    event.listen(User, 'before_insert', fake_time_hook)