import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app

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
