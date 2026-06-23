from sqlite3 import connect, Row
from dotenv import load_dotenv
import os

load_dotenv()
DB_PATH = os.getenv("DATABASE", "./data/lupin.sqlite3")

def init_db(db_name: str = DB_PATH):
    data_dir = os.path.dirname(db_name)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            celular VARCHAR(11) NOT NULL,
            cpf_cnpj VARCHAR(14),
            tipo_conta CHAR(1) NOT NULL,
            cidade_estado VARCHAR(50) NOT NULL,
            foto TEXT DEFAULT 'default.png'
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade_aproximada VARCHAR(10) NOT NULL,
            tipo VARCHAR(25) NOT NULL,
            raca VARCHAR(30) NOT NULL,
            porte TEXT NOT NULL,
            sexo CHAR(1),
            descricao TEXT NOT NULL,
                     
            FOREIGN KEY (id) REFERENCES usuario(id)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acao CHAR(1) NOT NULL,
            status_adocao TEXT NOT NULL,
            data_interacao TIMESTAMP NOT NULL,

            FOREIGN KEY (id) REFERENCES usuario(id) ON DELETE CASCADE,
            FOREIGN KEY (id) REFERENCES pet(id) ON DELETE CASCADE
        )
        """)

def conectar():
    """Retorna uma conexão configurada para retornar dicionários (Row)."""
    conn = connect(DB_PATH)
    conn.row_factory = Row
    return conn