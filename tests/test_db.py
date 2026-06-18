from fastapi_zero.models import User


def test_create_user():
    user = User(username='username', email='email@teste', password='secret')

    assert user.email == 'email@teste' 
