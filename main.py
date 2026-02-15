# Interfaz gráfica con Tkinter para la tienda

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import crear_tabla, inicializar_db
from crud import obtener_todos, crear, actualizar, eliminar, buscar
from models import CATEGORIAS


class TiendaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("🏪 Sistema de Tienda - CRUD")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)
        
        # Inicializar base de datos
        crear_tabla()
        inicializar_db()
        
        # Variable para guardar el ID del producto seleccionado
        self.producto_seleccionado_id = None
        
        # Crear interfaz
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        
        # Panel superior - Título
        panel_titulo = tk.Frame(self.ventana, bg="#2c3e50", height=50)
        panel_titulo.pack(fill=tk.X)
        
        titulo = tk.Label(
            panel_titulo,
            text="🏪 SISTEMA DE GESTIÓN DE TIENDA",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=10)
        
        # Panel principal con dos secciones
        panel_principal = tk.Frame(self.ventana)
        panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección izquierda - Formulario
        panel_izquierda = ttk.LabelFrame(panel_principal, text="📝 Formulario de Producto", padding=10)
        panel_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Nombre
        ttk.Label(panel_izquierda, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(panel_izquierda, width=25)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Categoría
        ttk.Label(panel_izquierda, text="Categoría:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_categoria = ttk.Combobox(panel_izquierda, values=CATEGORIAS, width=22, state="readonly")
        self.combo_categoria.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Precio
        ttk.Label(panel_izquierda, text="Precio ($):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_precio = ttk.Entry(panel_izquierda, width=25)
        self.entry_precio.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Cantidad
        ttk.Label(panel_izquierda, text="Cantidad:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_cantidad = ttk.Entry(panel_izquierda, width=25)
        self.entry_cantidad.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Botones de acción
        panel_botones = tk.Frame(panel_izquierda)
        panel_botones.grid(row=4, column=0, columnspan=2, pady=20)
        
        btn_crear = tk.Button(
            panel_botones,
            text="➕ Crear Producto",
            command=self.crear_producto,
            bg="#27ae60",
            fg="white",
            width=18
        )
        btn_crear.pack(pady=5)
        
        btn_actualizar = tk.Button(
            panel_botones,
            text="✏️ Actualizar",
            command=self.actualizar_producto,
            bg="#f39c12",
            fg="white",
            width=18
        )
        btn_actualizar.pack(pady=5)
        
        btn_eliminar = tk.Button(
            panel_botones,
            text="🗑️ Eliminar",
            command=self.eliminar_producto,
            bg="#e74c3c",
            fg="white",
            width=18
        )
        btn_eliminar.pack(pady=5)
        
        btn_limpiar = tk.Button(
            panel_botones,
            text="🔄 Limpiar Formulario",
            command=self.limpiar_formulario,
            bg="#95a5a6",
            fg="white",
            width=18
        )
        btn_limpiar.pack(pady=5)
        
        # Buscador
        ttk.Label(panel_izquierda, text="Buscar:").grid(row=5, column=0, sticky=tk.W, pady=10)
        self.entry_buscar = ttk.Entry(panel_izquierda, width=25)
        self.entry_buscar.grid(row=5, column=1, sticky=tk.W, pady=10)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.buscar_productos())
        
        # Sección derecha - Tabla de productos
        panel_derecha = ttk.LabelFrame(panel_principal, text="📊 Lista de Productos", padding=10)
        panel_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Crear tabla (Treeview)
        columns = ("ID", "Nombre", "Categoría", "Precio", "Stock")
        self.tabla = ttk.Treeview(panel_derecha, columns=columns, height=20, show="headings")
        
        # Definir columnas
        self.tabla.column("ID", width=40)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Categoría", width=100)
        self.tabla.column("Precio", width=80)
        self.tabla.column("Stock", width=60)
        
        # Definir encabezados
        for col in columns:
            self.tabla.heading(col, text=col)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(panel_derecha, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.tabla.bind('<<TreeviewSelect>>', self.seleccionar_producto)
    
    def cargar_productos(self):
        """Carga todos los productos en la tabla"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Insertar productos
        productos = obtener_todos()
        for producto in productos:
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.cantidad
                )
            )
    
    def seleccionar_producto(self, event):
        """Carga el producto seleccionado en el formulario"""
        seleccion = self.tabla.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tabla.item(item, "values")
            
            self.producto_seleccionado_id = valores[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.combo_categoria.set(valores[2])
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, valores[3].replace("$", ""))
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, valores[4])
    
    def crear_producto(self):
        """Crea un nuevo producto"""
        if not self.validar_formulario():
            return
        
        try:
            nombre = self.entry_nombre.get()
            categoria = self.combo_categoria.get()
            precio = float(self.entry_precio.get())
            cantidad = int(self.entry_cantidad.get())
            
            crear(nombre, categoria, precio, cantidad)
            messagebox.showinfo("Éxito", "✅ Producto creado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except ValueError:
            messagebox.showerror("Error", "❌ Precio debe ser un número y cantidad debe ser entero")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al crear: {str(e)}")
    
    def actualizar_producto(self):
        """Actualiza el producto seleccionado"""
        if not self.producto_seleccionado_id:
            messagebox.showwarning("Advertencia", "⚠️ Selecciona un producto para actualizar")
            return
        
        if not self.validar_formulario():
            return
        
        try:
            nombre = self.entry_nombre.get()
            categoria = self.combo_categoria.get()
            precio = float(self.entry_precio.get())
            cantidad = int(self.entry_cantidad.get())
            
            actualizar(self.producto_seleccionado_id, nombre, categoria, precio, cantidad)
            messagebox.showinfo("Éxito", "✅ Producto actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except ValueError:
            messagebox.showerror("Error", "❌ Precio debe ser un número y cantidad debe ser entero")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al actualizar: {str(e)}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado_id:
            messagebox.showwarning("Advertencia", "⚠️ Selecciona un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?"):
            try:
                eliminar(self.producto_seleccionado_id)
                messagebox.showinfo("Éxito", "✅ Producto eliminado correctamente")
                self.limpiar_formulario()
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al eliminar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.combo_categoria.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_buscar.delete(0, tk.END)
        self.producto_seleccionado_id = None
        self.cargar_productos()
    
    def buscar_productos(self):
        """Busca productos según el término"""
        termino = self.entry_buscar.get().strip()
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        if termino:
            productos = buscar(termino)
        else:
            productos = obtener_todos()
        
        # Insertar productos filtrados
        for producto in productos:
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.cantidad
                )
            )
    
    def validar_formulario(self):
        """Valida que los campos no estén vacíos"""
        if not self.entry_nombre.get():
            messagebox.showwarning("Validación", "❌ El nombre es requerido")
            return False
        if not self.combo_categoria.get():
            messagebox.showwarning("Validación", "❌ La categoría es requerida")
            return False
        if not self.entry_precio.get():
            messagebox.showwarning("Validación", "❌ El precio es requerido")
            return False
        if not self.entry_cantidad.get():
            messagebox.showwarning("Validación", "❌ La cantidad es requerida")
            return False
        return True


if __name__ == "__main__":
    ventana = tk.Tk()
    app = TiendaApp(ventana)
    ventana.mainloop()
