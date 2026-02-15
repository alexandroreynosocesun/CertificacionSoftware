# Operaciones CRUD para la tienda

from db import conectar
from models import Producto


def obtener_todos():
    """Obtiene todos los productos"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM productos ORDER BY id')
    filas = cursor.fetchall()
    conexion.close()
    
    productos = []
    for fila in filas:
        producto = Producto(
            id=fila['id'],
            nombre=fila['nombre'],
            categoria=fila['categoria'],
            precio=fila['precio'],
            cantidad=fila['cantidad']
        )
        productos.append(producto)
    
    return productos


def obtener_por_id(id):
    """Obtiene un producto por su ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    fila = cursor.fetchone()
    conexion.close()
    
    if fila:
        return Producto(
            id=fila['id'],
            nombre=fila['nombre'],
            categoria=fila['categoria'],
            precio=fila['precio'],
            cantidad=fila['cantidad']
        )
    return None


def crear(nombre, categoria, precio, cantidad):
    """Crea un nuevo producto"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, cantidad)
            VALUES (?, ?, ?, ?)
        ''', (nombre, categoria, float(precio), int(cantidad)))
        
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id
    except Exception as e:
        conexion.close()
        raise e


def actualizar(id, nombre, categoria, precio, cantidad):
    """Actualiza un producto existente"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, categoria = ?, precio = ?, cantidad = ?
            WHERE id = ?
        ''', (nombre, categoria, float(precio), int(cantidad), id))
        
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        conexion.close()
        raise e


def eliminar(id):
    """Elimina un producto"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        conexion.close()
        raise e


def buscar(termino):
    """Busca productos por nombre o categoría"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('''
        SELECT * FROM productos 
        WHERE nombre LIKE ? OR categoria LIKE ?
        ORDER BY id
    ''', (f'%{termino}%', f'%{termino}%'))
    
    filas = cursor.fetchall()
    conexion.close()
    
    productos = []
    for fila in filas:
        producto = Producto(
            id=fila['id'],
            nombre=fila['nombre'],
            categoria=fila['categoria'],
            precio=fila['precio'],
            cantidad=fila['cantidad']
        )
        productos.append(producto)
    
    return productos
