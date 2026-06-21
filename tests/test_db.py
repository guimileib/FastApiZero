from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    new_user = User(username="test", email="email@teste", password="secret")

    session.add(new_user)
    session.commit()

    # pedindo o resultado do que foi inserido
    # é a volta do orm de dado para objeto python
    user = session.scalar(select(User).where(User.username == "test"))
    # isso é a mesma coisa de SELECT * FROM USER WHERE username = 'test
    # asidct converte isso em dicionario
    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "email@test",
        "password": "secret",
    }
