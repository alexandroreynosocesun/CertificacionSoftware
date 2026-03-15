import hashlib
from db import conectar
from models import Cliente, Evento


# ─── AUTENTICACION ────────────────────────────────────────────────────────────

def verificar_usuario(usuario, password):
    h = hashlib.sha256(password.encode()).hexdigest()
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM usuarios WHERE usuario = ? AND password_hash = ?",
        (usuario, h)
    )
    row = cur.fetchone()
    conn.close()
    return row is not None


# ─── CLIENTES ─────────────────────────────────────────────────────────────────

def _fila_a_cliente(r):
    return Cliente(
        id=r["id"], codigo=r["codigo"], nombre=r["nombre"],
        telefono=r["telefono"] or "", fecha_registro=r["fecha_registro"]
    )


def get_clientes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [_fila_a_cliente(r) for r in rows]


def buscar_clientes(termino):
    conn = conectar()
    cur = conn.cursor()
    t = f"%{termino}%"
    cur.execute(
        "SELECT * FROM clientes WHERE codigo LIKE ? OR nombre LIKE ? OR telefono LIKE ? ORDER BY id",
        (t, t, t)
    )
    rows = cur.fetchall()
    conn.close()
    return [_fila_a_cliente(r) for r in rows]


def crear_cliente(codigo, nombre, telefono, fecha_registro):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clientes (codigo, nombre, telefono, fecha_registro) VALUES (?,?,?,?)",
        (codigo, nombre, telefono, fecha_registro)
    )
    conn.commit()
    conn.close()


def actualizar_cliente(id, codigo, nombre, telefono, fecha_registro):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "UPDATE clientes SET codigo=?, nombre=?, telefono=?, fecha_registro=? WHERE id=?",
        (codigo, nombre, telefono, fecha_registro, id)
    )
    conn.commit()
    conn.close()


def eliminar_cliente(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ─── EVENTOS ──────────────────────────────────────────────────────────────────

_SQL_EVENTOS = """
    SELECT e.id, e.nombre_tipo, e.descripcion, e.estatus, e.fecha_evento,
           e.cliente_id, c.nombre AS cliente_nombre
    FROM eventos e
    JOIN clientes c ON e.cliente_id = c.id
"""


def _fila_a_evento(r):
    return Evento(
        id=r["id"], nombre_tipo=r["nombre_tipo"],
        descripcion=r["descripcion"] or "", estatus=r["estatus"],
        fecha_evento=r["fecha_evento"], cliente_id=r["cliente_id"],
        cliente_nombre=r["cliente_nombre"]
    )


def get_eventos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute(_SQL_EVENTOS + " ORDER BY e.id")
    rows = cur.fetchall()
    conn.close()
    return [_fila_a_evento(r) for r in rows]


def buscar_eventos(termino):
    conn = conectar()
    cur = conn.cursor()
    t = f"%{termino}%"
    cur.execute(
        _SQL_EVENTOS +
        " WHERE e.nombre_tipo LIKE ? OR e.descripcion LIKE ? OR e.estatus LIKE ? OR c.nombre LIKE ? ORDER BY e.id",
        (t, t, t, t)
    )
    rows = cur.fetchall()
    conn.close()
    return [_fila_a_evento(r) for r in rows]


def get_evento_por_id(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(_SQL_EVENTOS + " WHERE e.id = ?", (id,))
    r = cur.fetchone()
    conn.close()
    return _fila_a_evento(r) if r else None


def crear_evento(nombre_tipo, descripcion, estatus, fecha_evento, cliente_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO eventos (nombre_tipo, descripcion, estatus, fecha_evento, cliente_id) VALUES (?,?,?,?,?)",
        (nombre_tipo, descripcion, estatus, fecha_evento, cliente_id)
    )
    conn.commit()
    conn.close()


def actualizar_evento(id, nombre_tipo, descripcion, estatus, fecha_evento, cliente_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "UPDATE eventos SET nombre_tipo=?, descripcion=?, estatus=?, fecha_evento=?, cliente_id=? WHERE id=?",
        (nombre_tipo, descripcion, estatus, fecha_evento, cliente_id, id)
    )
    conn.commit()
    conn.close()


def actualizar_estatus_evento(id, estatus):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE eventos SET estatus=? WHERE id=?", (estatus, id))
    conn.commit()
    conn.close()


def eliminar_evento(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM eventos WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ─── REPORTES ─────────────────────────────────────────────────────────────────

def reporte_join():
    """JOIN: detalle de cada evento con código y nombre del cliente."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, c.codigo, c.nombre, e.nombre_tipo, e.descripcion, e.estatus, e.fecha_evento
        FROM eventos e
        JOIN clientes c ON e.cliente_id = c.id
        ORDER BY c.nombre, e.fecha_evento
    """)
    rows = cur.fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def reporte_groupby():
    """GROUP BY: total de eventos por cliente."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.codigo, c.nombre, COUNT(e.id) AS total_eventos
        FROM clientes c
        LEFT JOIN eventos e ON c.id = e.cliente_id
        GROUP BY c.id, c.codigo, c.nombre
        ORDER BY total_eventos DESC, c.nombre
    """)
    rows = cur.fetchall()
    conn.close()
    return [tuple(r) for r in rows]
