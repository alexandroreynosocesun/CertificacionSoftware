class Cliente:
    def __init__(self, id=None, codigo="", nombre="", telefono="", fecha_registro=""):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.telefono = telefono
        self.fecha_registro = fecha_registro


class Evento:
    def __init__(self, id=None, nombre_tipo="", descripcion="", estatus="Cotizado",
                 fecha_evento="", cliente_id=None, cliente_nombre=""):
        self.id = id
        self.nombre_tipo = nombre_tipo
        self.descripcion = descripcion
        self.estatus = estatus
        self.fecha_evento = fecha_evento
        self.cliente_id = cliente_id
        self.cliente_nombre = cliente_nombre


ESTATUSES = ["Cotizado", "Confirmado", "Realizado", "Cancelado"]
