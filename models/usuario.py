from models.database import conectar
from werkzeug.security import generate_password_hash, check_password_hash


def criar_usuario(nome, email, senha):
    """
    Cadastra um novo usuário.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    senha_hash = generate_password_hash(senha)

    try:
        cursor.execute(""" INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?) """, (nome, email, senha_hash))

        conexao.commit()
        return True

    except Exception:
        return False

    finally:
        conexao.close()


def buscar_usuario_por_email(email):
    """
    Busca um usuário pelo email.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM usuarios WHERE email = ? """, (email,))

    usuario = cursor.fetchone()

    conexao.close()

    return usuario


def buscar_usuario_por_id(usuario_id):
    """
    Busca um usuário pelo ID.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM usuarios WHERE id = ? """, (usuario_id,))

    usuario = cursor.fetchone()

    conexao.close()

    return usuario


def verificar_login(email, senha):
    """
    Verifica se o email e senha estão corretos.
    """

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return None

    if check_password_hash(usuario["senha"], senha):
        return usuario

    return None