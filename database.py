import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "clinica.db"))


def get_connection():
    """Abre e retorna uma conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Cria as tabelas do banco de dados se ainda não existirem."""
    banco_novo = not os.path.exists(DB_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            data_nascimento TEXT
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            motivo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
        );
        """
    )

    if banco_novo:
        cursor.executemany(
            "INSERT INTO pacientes (nome, telefone, data_nascimento) VALUES (?, ?, ?);",
            [
                ("Ana Clara Silva", "(11) 98765-4321", "2004-05-12"),
                ("Bruno Oliveira", "(11) 91234-5678", "1998-11-23"),
                ("Carla Mendes", "(11) 99887-7665", "1985-03-08"),
            ],
        )
        cursor.executemany(
            "INSERT INTO consultas (paciente_id, data, hora, motivo) VALUES (?, ?, ?, ?);",
            [
                (2, "2026-11-26", "14:30", "Retorno clínico"),
                (1, "2026-11-25", "09:00", "Consulta de rotina"),
                (3, "2026-11-25", "08:15", "Exame preventivo"),
            ],
        )

    conn.commit()
    conn.close()
