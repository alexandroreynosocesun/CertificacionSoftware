# MANUAL DE USUARIO - SISTEMA DE TIENDA

## Descripción General
**Tienda_Sistema** es una aplicación de gestión de productos para un negocio. Permite crear, leer, actualizar y eliminar productos de una tienda, con una interfaz gráfica amigable y fácil de usar.

---

## Requisitos del Sistema
- **Sistema Operativo:** Windows 7 o superior
- **Memoria RAM:** Mínimo 512 MB
- **Espacio en disco:** 20 MB aproximadamente
- **No requiere instalación adicional de Python**

---

## Cómo Ejecutar la Aplicación

### Opción 1: Desde el Archivo Ejecutable (Recomendado)
1. Navega a la carpeta `dist/`
2. Haz doble clic en `Tienda_Sistema.exe`
3. La aplicación se abrirá automáticamente con la base de datos inicializada

### Opción 2: Desde el Código Fuente (Requiere Python)
```bash
python main.py
```

---

## 📱 Interfaz de la Aplicación

### Elementos Principales

#### 1. **Panel Superior**
- Título: "SISTEMA DE GESTIÓN DE TIENDA"

#### 2. **Formulario de Producto (Lado Izquierdo)**
- **Nombre:** Ingresa el nombre del producto
- **Categoría:** Selecciona de las opciones disponibles
  - Electrónica
  - Ropa
  - Alimentos
  - Libros
  - Hogar
- **Precio ($):** Ingresa el precio del producto
- **Cantidad:** Ingresa la cantidad en stock

#### 3. **Botones de Acción**
- **Crear Producto:** Añade un nuevo producto a la tienda
- **Actualizar:** Modifica un producto existente
- **Eliminar:** Borra un producto de la tienda
- **Limpiar Formulario:** Limpia todos los campos

#### 4. **Buscador**
- Campo de búsqueda para encontrar productos por nombre o categoría

#### 5. **Lista de Productos (Lado Derecho)**
- Tabla con todos los productos
- Columnas: ID, Nombre, Categoría, Precio, Stock

---

## Guía de Uso Paso a Paso

### **Crear un Nuevo Producto**
1. Rellena todos los campos del formulario:
   - Nombre (ej: "Laptop")
   - Categoría (selecciona de la lista)
   - Precio (ej: 999.99)
   - Cantidad (ej: 5)
2. Haz clic en **"Crear Producto"**
3. Verás un mensaje de confirmación: **"Producto creado correctamente"**
4. El nuevo producto aparecerá en la tabla

### **Ver Todos los Productos**
- Los productos se muestran automáticamente en la tabla de la derecha
- Puedes ver: ID, Nombre, Categoría, Precio y Stock

### **Actualizar un Producto**
1. Haz clic en el producto que deseas modificar en la tabla
2. Los datos se cargarán automáticamente en el formulario
3. Modifica los campos que necesites
4. Haz clic en **" Actualizar"**
5. Verás el mensaje: **"Producto actualizado correctamente"**

### **Eliminar un Producto**
1. Selecciona el producto en la tabla
2. Haz clic en **"Eliminar"**
3. Se te pedirá confirmación: **"¿Estás seguro de que quieres eliminar este producto?"**
4. Haz clic en **"Sí"** para confirmar
5. Verás: **"Producto eliminado correctamente"**

### **Buscar Productos**
1. Escribe en el campo **"Buscar:"** (ej: "Electrónica")
2. La tabla se filtrará automáticamente
3. Para ver todos nuevamente, borra el campo de búsqueda

### **Limpiar el Formulario**
- Haz clic en **"Limpiar Formulario"** para vaciar todos los campos y resetear la selección

---

## Datos de Ejemplo

La aplicación viene preconfigurada con estos productos de ejemplo:

| ID | Nombre | Categoría | Precio | Stock |
|----|--------|-----------|--------|-------|
| 1 | Laptop | Electrónica | $799.99 | 5 |
| 2 | Mouse | Electrónica | $25.99 | 20 |
| 3 | Camiseta | Ropa | $19.99 | 15 |
| 4 | Pantalones | Ropa | $49.99 | 10 |
| 5 | Arroz | Alimentos | $3.50 | 50 |
| 6 | Python 101 | Libros | $29.99 | 8 |
| 7 | Almohada | Hogar | $15.99 | 12 |

---

## Mensajes y Significado

### Mensajes de Éxito 
- **"Producto creado correctamente"** → El producto fue añadido exitosamente
- **"Producto actualizado correctamente"** → Los cambios fueron guardados
- **"Producto eliminado correctamente"** → El producto fue borrado

### Mensajes de Advertencia 
- **"Selecciona un producto para actualizar"** → Debes seleccionar un producto en la tabla
- **"Selecciona un producto para eliminar"** → Debes seleccionar un producto antes de eliminar

### Mensajes de Error 
- **"El nombre es requerido"** → Llena el campo de nombre
- **"La categoría es requerida"** → Selecciona una categoría
- **"El precio es requerido"** → Ingresa el precio
- **"La cantidad es requerida"** → Ingresa la cantidad
- **"Precio debe ser un número y cantidad debe ser entero"** → Verifica los datos ingresados

---

## Base de Datos

- **Tipo:** SQLite
- **Archivo:** `tienda.db` (se crea automáticamente)
- **Ubicación:** En la misma carpeta que el ejecutable
- **Tablas:** 
  - **productos** (id, nombre, categoria, precio, cantidad)

---

## 🔧 Validaciones del Sistema

✅ El nombre del producto es obligatorio
✅ La categoría debe ser seleccionada de las opciones disponibles
✅ El precio debe ser un número (decimal)
✅ La cantidad debe ser un número entero
✅ No permite crear productos sin datos completos
✅ Valida antes de actualizar o eliminar

---

## Solución de Problemas

### **La aplicación no abre**
- Verifica que tu sistema sea Windows 7 o superior
- Intenta ejecutarla nuevamente haciendo doble clic
- Descarga nuevamente el ejecutable

### **No aparecen los productos**
- Verifica que el archivo `tienda.db` exista en la carpeta
- Si no existe, la aplicación lo creará automáticamente al ejecutarse

### **Cambios no se guardan**
- Verifica que tienes permisos de escritura en la carpeta
- Cierra otros programas que puedan estar usando la base de datos

### **Mensajes de error al crear producto**
- Revisa que todos los campos estén llenos
- Verifica que el precio sea un número válido
- Verifica que la cantidad sea un número entero

---

## Notas Importantes

- La aplicación guarda automáticamente todos los cambios en la base de datos
- No es necesario hacer clic en "Guardar" (todo se guarda en tiempo real)
- Puedes ejecutar la aplicación tantas veces como necesites
- Los datos persisten entre ejecuciones
- Para eliminar un producto, debes seleccionarlo primero en la tabla

---

**Desarrollado en:** Python con Tkinter + SQLite
