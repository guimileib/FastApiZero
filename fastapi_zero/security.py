from pwdlib import PasswordHash

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
