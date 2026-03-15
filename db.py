import sqlite3
import hashlib
import os
import sys

# Ruta de la BD junto al ejecutable (cuando es .exe) o junto al script
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(_BASE, "galapro.db")


def conectar():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def crear_tablas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario       TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo         TEXT    NOT NULL UNIQUE,
            nombre         TEXT    NOT NULL,
            telefono       TEXT,
            fecha_registro TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_tipo  TEXT    NOT NULL,
            descripcion  TEXT,
            estatus      TEXT    NOT NULL DEFAULT 'Cotizado',
            fecha_evento TEXT    NOT NULL,
            cliente_id   INTEGER NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)

    # Usuario admin por defecto si no hay ninguno
    cur.execute("SELECT COUNT(*) FROM usuarios")
    if cur.fetchone()[0] == 0:
        h = hashlib.sha256("admin123".encode()).hexdigest()
        cur.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            ("admin", h)
        )

    conn.commit()
    conn.close()
