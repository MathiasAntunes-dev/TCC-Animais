import sqlite3
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path("data/petbanco.sqlite3")


def conectar():
    """
    Cria uma conexão com o banco de dados.
    """
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    """
    Cria todas as tabelas do sistema caso não existam.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Pets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            especie TEXT NOT NULL,
            raca TEXT,
            sexo TEXT,
            descricao TEXT,
            foto TEXT,
            whatsapp TEXT NOT NULL,
            disponivel INTEGER DEFAULT 1,
            usuario_id INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id)
        )
    """)

    # Curtidas / Matches
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            pet_id INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id),

            FOREIGN KEY (pet_id)
            REFERENCES pets(id)
        )
    """)

    conexao.commit()
    conexao.close()


def inicializar_banco():
    """
    Inicializa o banco de dados.
    """
    criar_tabelas()