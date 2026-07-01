from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):

    # passa parametro q esta testando User, e depois pega o tempo 
    with mock_db_time(model=User) as time: 
        new_user = User(
            username="test", email="email@test", password="secret"
            )

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
            "created_at": time,
            "updated_at": time,
        }

def test_update_user(session, mock_db_time):

    with mock_db_time(model=User) as time: 
        new_user = User(
            username="test", email="email@test", password="secret"
        )
    
    session.add(new_user) # faz a inserção 
    session.commit()

    new_user.username = 'test_updated' # faz o update do user
    session.commit()
    session.refresh(new_user)

    user = session.scalar(
        select(User).where(User.username == 'test_updated')
    )
    
    assert asdict(user) == {
        "id": 1,
        "username": "test_updated",
        "email": "email@test",
        "password": "secret",
        "created_at": time,
        "updated_at": time,
    }