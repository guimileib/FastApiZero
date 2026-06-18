from http import HTTPStatus


def test_root_dev_retornar_hello_world(client):

    response = client.get("/")

    assert response.json() == {"message": "Olá mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_root_dev_retornar_hello_world_in_html(client):
    response = client.get("/exercicio00")

    assert response.status_code == HTTPStatus.OK
    assert (
        """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>"""
        in response.text
    )


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "email": "bob@example.com",
        "username": "bob",
    }


# smell code, quando um teste fica grudado em outro
def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "bob",
                "email": "bob@example.com"
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret'
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1
    }


def test_update_not_found(client):
    user_id = '999'  # id que o usuario esta tentando alterar

    response = client.put(
        f'/users/{user_id}',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1
    }


def test_delete_not_found(client):
    user_id = '999'  # id que o usuario esta tentando alterar

    response = client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
