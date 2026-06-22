from models.database import conectar


def criar_pet(nome, idade, especie, raca, sexo, descricao, foto, whatsapp, usuario_id):
    """
    Cadastra um novo pet.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO pets (
            nome,
            idade,
            especie,
            raca,
            sexo,
            descricao,
            foto,
            whatsapp,
            usuario_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, idade, especie, raca, sexo, descricao, foto, whatsapp, usuario_id))

    conexao.commit()
    conexao.close()


def listar_pets():
    """
    Retorna todos os pets disponíveis.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM pets WHERE disponivel = 1 ORDER BY criado_em DESC """)

    pets = cursor.fetchall()

    conexao.close()

    return pets


def buscar_pet_por_id(pet_id):
    """
    Busca um pet pelo ID.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM pets WHERE id = ? """, (pet_id,))

    pet = cursor.fetchone()

    conexao.close()

    return pet


def listar_pets_usuario(usuario_id):
    """
    Lista os pets cadastrados por um usuário.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" SELECT * FROM pets WHERE usuario_id = ? ORDER BY criado_em DESC """, (usuario_id,))

    pets = cursor.fetchall()

    conexao.close()

    return pets


def excluir_pet(pet_id):
    """
    Remove um pet do sistema.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" DELETE FROM pets WHERE id = ? """, (pet_id,))

    conexao.commit()
    conexao.close()


def atualizar_pet(pet_id, nome, idade, especie, raca, sexo, descricao, whatsapp):
    """
    Atualiza os dados de um pet.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE pets
        SET
            nome = ?,
            idade = ?,
            especie = ?,
            raca = ?,
            sexo = ?,
            descricao = ?,
            whatsapp = ?
        WHERE id = ?
    """, (nome, idade, especie, raca, sexo, descricao, whatsapp, pet_id))

    conexao.commit()
    conexao.close()