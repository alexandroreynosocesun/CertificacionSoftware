# Modelos de datos para la tienda

class Producto:
    """Modelo para productos de la tienda"""
    def __init__(self, id=None, nombre="", categoria="", precio=0.0, cantidad=0):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad
    
    def __str__(self):
        return f"ID: {self.id} | {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f} | Stock: {self.cantidad}"
    
    def __repr__(self):
        return self.__str__()


CATEGORIAS = ["Electrónica", "Ropa", "Alimentos", "Libros", "Hogar"]
