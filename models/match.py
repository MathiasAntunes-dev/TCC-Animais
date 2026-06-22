from models.database import conectar

def curtir_pet(usuario_id, pet_id):
    """
    Registra uma curtida em um pet.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Evita curtidas duplicadas
    cursor.execute(""" SELECT id FROM matches WHERE usuario_id = ? AND pet_id = ? """, (usuario_id, pet_id))

    match_existente = cursor.fetchone()

    if match_existente:
        conexao.close()
        return False

    cursor.execute(""" INSERT INTO matches (usuario_id, pet_id) VALUES (?, ?) """, (usuario_id, pet_id))

    conexao.commit()
    conexao.close()

    return True


def listar_matches_usuario(usuario_id):
    """
    Lista todos os pets curtidos por um usuário.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pets.*
        FROM matches

        INNER JOIN pets
            ON pets.id = matches.pet_id

        WHERE matches.usuario_id = ?

        ORDER BY matches.criado_em DESC
    """, (usuario_id,))

    matches = cursor.fetchall()

    conexao.close()

    return matches


def verificar_match(usuario_id, pet_id):
    """
    Verifica se o usuário já curtiu o pet.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM matches WHERE usuario_id = ? AND pet_id = ? """, (usuario_id, pet_id))

    match = cursor.fetchone()

    conexao.close()

    return match


def remover_match(usuario_id, pet_id):
    """
    Remove uma curtida.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" DELETE FROM matches WHERE usuario_id = ? AND pet_id = ? """, (usuario_id, pet_id))

    conexao.commit()
    conexao.close()