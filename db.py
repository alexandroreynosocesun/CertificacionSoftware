# Base de datos SQLite para la tienda

import sqlite3
import os
from models import Producto

DB_FILE = "tienda.db"


def conectar():
    """Crea conexión a la base de datos"""
    conexion = sqlite3.connect(DB_FILE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    """Crea la tabla de productos si no existe"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')
    
    conexion.commit()
    conexion.close()


def inicializar_db():
    """Inicializa la base de datos con algunos productos de ejemplo"""
    if not os.path.exists(DB_FILE):
        crear_tabla()
        conexion = conectar()
        cursor = conexion.cursor()
        
        # Datos de ejemplo
        productos_ejemplo = [
            ("Laptop", "Electrónica", 799.99, 5),
            ("Mouse", "Electrónica", 25.99, 20),
            ("Camiseta", "Ropa", 19.99, 15),
            ("Pantalones", "Ropa", 49.99, 10),
            ("Arroz", "Alimentos", 3.50, 50),
            ("Python 101", "Libros", 29.99, 8),
            ("Almohada", "Hogar", 15.99, 12),
        ]
        
        for nombre, categoria, precio, cantidad in productos_ejemplo:
            cursor.execute('''
                INSERT INTO productos (nombre, categoria, precio, cantidad)
                VALUES (?, ?, ?, ?)
            ''', (nombre, categoria, precio, cantidad))
        
        conexion.commit()
        conexion.close()
