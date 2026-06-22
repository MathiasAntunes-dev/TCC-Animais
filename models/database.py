from sqlite3 import connect, Row
from dotenv import load_dotenv
import os

load_dotenv()
DB_PATH = os.getenv("DATABASE", "./data/forum.sqlite3")

def init_db(db_name: str = DB_PATH):
    data_dir = os.path.dirname(db_name)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY UNIQUE UNSIGNED AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            celular VARCHAR(11) NOT NULL,
            cpf_cnpj VARCHAR(14)
            tipo_conta ENUM("Pessoal", "Doador") NOT NULL,
            cidade/estado VARCHAR(50) NOT NULL,
            foto TEXT DEFAULT 'default.png'
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS pet
            id INTEGER PRIMARY KEY UNSIGNED UNIQUE AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade_aproximada VARCHAR(10) NOT NULL,
            tipo VARCHAR(25) NOT NULL,
            raca VARCHAR(30) NOT NULL,
            porte ENUM("Pequeno", "Médio", "Grande") NOT NULL,
            sexo ENUM("Macho", "Fêmea")
            descricao TEXT NOT NULL,
                     
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXIST match
        id INTERGER PRIMARY KEY UNSIGNED UNIQUE AUTOINCREMENT,
        acao ENUM("Like", "Dislike") NOT NULL,
        status_adocao ENUM("Pendente", "Em contato", "Concluído", "Cancelado") NOT NULL,
        data_interacao TIMESTAMP

        FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
        FOREING KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE
                              
        """)

def conectar():
    """Retorna uma conexão configurada para retornar dicionários (Row)."""
    conn = connect(DB_PATH)
    conn.row_factory = Row
    return conn