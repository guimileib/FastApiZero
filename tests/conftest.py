from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry

"""
Esse teste tem 3 etapas (AAA)
- A: Arrange - Arranjo - Carregar dados
- A: Act - Chama o bloco de código executa (SUT)
- A: Assert - Garanta que A é A
"""


# Arrange
@pytest.fixture
def client(session):
    def get_session_override():
        return session  # troca  a session do banco de prod pela de baixo

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()  # Limpa as dependências


@pytest.fixture
def session():
    # criando a engine via memoria
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # criando de fato a estrutura de banco em memoria
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # retorna um de cada vez ao inves de todos

    table_registry.metadata.drop_all(engine)  # depois que usar deleta todas


# gerenciador de contexto, apenas no momentoo
@contextmanager
def _mock_db_item(model, time=datetime(2026, 6, 21)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)
    event.listen(model, "before_update", fake_time_hook)
    yield time

    event.remove(model, "before_insert", fake_time_hook)
    event.remove(model, "before_update", fake_time_hook)


# crio uma estrutura para sempre reutilizar, quando tem created_at
@pytest.fixture
def mock_db_time():
    return _mock_db_item


# criando uma fixture para que o usuario esteja presente
@pytest.fixture
def user(session):
    user = User(username="Teste", email="teste@test.com", password="testtest")
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
