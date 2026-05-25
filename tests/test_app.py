from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_dev_retornar_hello_world():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo - Carregar dados
    - A: Act - Chama o bloco de código executa (SUT)
    - A: Assert - Garanta que A é A
    """

    # Arrange
    client = TestClient(app)  # importou o client do fastapi

    response = client.get("/")

    assert response.json() == {"message": "Olá mundo!"}
    assert response.status_code == HTTPStatus.OK

    response = client.get("/exercicio00")
    assert response.status_code == HTTPStatus.OK
    assert "<h1>Hello World!</h1>" in response.text
