# MANUAL TÉCNICO - SISTEMA DE TIENDA

## Objetivo del Proyecto

Desarrollar una aplicación de escritorio que implemente un **Sistema de Gestión de Tienda** con acceso a una base de datos relacional (SQLite) y una interfaz gráfica usando Tkinter, cumpliendo con el estándar **EC0835 – Desarrollar software de aplicación con acceso a bases de datos**.

---

## Arquitectura del Sistema

### Estructura de Archivos

```
Tareas/
├── models.py           # Definición de modelos (Producto)
├── db.py              # Conexión y creación de base de datos
├── crud.py            # Operaciones CRUD (Create, Read, Update, Delete)
├── main.py            # Interfaz gráfica con Tkinter
├── tienda.db          # Base de datos SQLite (generada automáticamente)
├── dist/
│   └── Tienda_Sistema.exe  # Ejecutable compilado
└── MANUAL_DE_USUARIO.md    # Documentación de usuario
```

### Patrones de Diseño Utilizados

1. **Modelo-Vista-Controlador (MVC) Simplificado**
   - **Modelo:** `models.py` - Define la estructura de datos
   - **Controlador:** `crud.py` - Lógica de negocios y operaciones
   - **Vista:** `main.py` - Interfaz gráfica

2. **Patrón de Acceso a Datos (DAO)**
   - `crud.py` actúa como intermediario entre la vista y la base de datos

---

## Esquema de la Base de Datos

### Tabla: `productos`

```sql
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
)
```

#### Descripción de Campos

| Campo | Tipo | Descripción | Restricción |
|-------|------|-------------|-------------|
| `id` | INTEGER | Identificador único | PRIMARY KEY, AUTOINCREMENT |
| `nombre` | TEXT | Nombre del producto | NOT NULL |
| `categoria` | TEXT | Categoría del producto | NOT NULL |
| `precio` | REAL | Precio unitario | NOT NULL |
| `cantidad` | INTEGER | Stock disponible | NOT NULL |

#### Categorías Válidas
- Electrónica
- Ropa
- Alimentos
- Libros
- Hogar

---

## Descripción Técnica de Módulos

### 1. **models.py** - Modelos de Datos

```python
class Producto:
    """Define la estructura de un producto con atributos y métodos"""
```

**Atributos:**
- `id`: Identificador único del producto
- `nombre`: Nombre descriptivo
- `categoria`: Clasificación del producto
- `precio`: Precio unitario en formato decimal
- `cantidad`: Cantidad disponible en inventario

**Métodos:**
- `__str__()`: Representación legible del producto
- `__repr__()`: Representación para debugging

**Constantes:**
- `CATEGORIAS`: Lista predefinida de categorías

### 2. **db.py** - Gestión de Base de Datos

**Funciones Principales:**

#### `conectar()`
- Establece conexión a SQLite
- Configura `row_factory` para retornar tuplas nombradas
- Retorna objeto conexión

#### `crear_tabla()`
- Crea la estructura de tabla `productos`
- Ejecuta sentencia SQL CREATE TABLE IF NOT EXISTS

#### `inicializar_db()`
- Verifica si la base de datos existe
- Si no existe, la crea con datos de ejemplo
- Inserta 7 productos preconfigurados

**Características de Seguridad:**
- Usa **prepared statements** con placeholders (`?`) para prevenir SQL injection
- Cierra conexiones después de cada operación

### 3. **crud.py** - Operaciones CRUD

**Operaciones Implementadas:**

#### **CREATE: `crear(nombre, categoria, precio, cantidad)`**
```sql
INSERT INTO productos (nombre, categoria, precio, cantidad) 
VALUES (?, ?, ?, ?)
```
- Valida y convierte tipos de datos
- Retorna el ID del nuevo producto
- Manejo de excepciones

#### **READ: `obtener_todos()`**
```sql
SELECT * FROM productos ORDER BY id
```
- Retorna lista de objetos Producto
- Ordenados por ID ascendente

#### **READ: `obtener_por_id(id)`**
```sql
SELECT * FROM productos WHERE id = ?
```
- Busca producto específico
- Retorna None si no existe

#### **READ: `buscar(termino)`**
```sql
SELECT * FROM productos 
WHERE nombre LIKE ? OR categoria LIKE ?
ORDER BY id
```
- Búsqueda case-insensitive
- Filtra por nombre o categoría

#### **UPDATE: `actualizar(id, nombre, categoria, precio, cantidad)`**
```sql
UPDATE productos 
SET nombre = ?, categoria = ?, precio = ?, cantidad = ? 
WHERE id = ?
```
- Modifica producto existente
- Valida tipos de datos

#### **DELETE: `eliminar(id)`**
```sql
DELETE FROM productos WHERE id = ?
```
- Eliminación permanente de registros
- Requiere confirmación en la UI

**Manejo de Errores:**
- Try-catch en todas las operaciones
- Cierre seguro de conexiones
- Propagación de excepciones a la UI

### 4. **main.py** - Interfaz Gráfica

**Framework:** Tkinter (incluido en Python)

**Componentes Principales:**

#### Clase `TiendaApp`
Controlador principal de la interfaz gráfica

**Inicialización:**
- Crea ventana principal
- Inicializa base de datos
- Construye interfaz
- Carga productos

**Variables de Instancia:**
- `ventana`: Objeto raíz de Tkinter
- `tabla`: Widget Treeview para mostrar productos
- `entry_*`: Campos de entrada del formulario
- `combo_categoria`: Selector de categoría
- `producto_seleccionado_id`: ID del producto en edición

**Métodos Principales:**

##### `crear_interfaz()`
- Construye layout de dos paneles
- Panel izquierdo: Formulario de entrada
- Panel derecho: Tabla de productos
- Implementa binding de eventos

##### `cargar_productos()`
- Obtiene productos de CRUD
- Limpia tabla anterior
- Inserta nuevas filas formateadas

##### `crear_producto()`
- Valida formulario
- Llama a CRUD.crear()
- Muestra mensaje de confirmación
- Recarga tabla

##### `actualizar_producto()`
- Verifica selección
- Valida formulario
- Llama a CRUD.actualizar()
- Limpia formulario

##### `eliminar_producto()`
- Verifica selección
- Solicita confirmación
- Llama a CRUD.eliminar()
- Recarga interfaz

##### `buscar_productos()`
- Obtiene término de búsqueda
- Filtra productos con CRUD.buscar()
- Actualiza tabla dinámicamente

##### `validar_formulario()`
- Verifica campos no vacíos
- Muestra advertencias específicas
- Retorna booleano

**Estilos y UX:**
- Colores temáticos (azul, verde, naranja, rojo)
- Iconos emoji para mejor legibilidad
- Mensajes emergentes contextuales
- Validación preventiva

---

## Funcionalidades de Seguridad y Validación

### 1. **Validación de Entrada**
- ✅ Campos obligatorios verificados
- ✅ Tipo de dato validado (precio REAL, cantidad INTEGER)
- ✅ Rango de valores permitidos

### 2. **Prevención de SQL Injection**
- ✅ Uso de prepared statements (`?`)
- ✅ Nunca concatenación de strings SQL
- ✅ Escapes automáticos de caracteres especiales

### 3. **Gestión de Errores**
- ✅ Try-catch en operaciones de BD
- ✅ Mensajes de error descriptivos
- ✅ Cierre seguro de conexiones
- ✅ Recuperación de estados inconsistentes

### 4. **Validación de Negocio**
- ✅ Categorías predefinidas
- ✅ Precios y cantidades positivos
- ✅ Confirmación antes de eliminar

---

## Operaciones Típicas del Sistema

### Flujo de Creación de Producto

```
Usuario ingresa datos → Validación → SQL INSERT → Confirmación → Recarga tabla
```

### Flujo de Búsqueda

```
Usuario escribe término → Evento KeyRelease → SQL LIKE → Tabla filtrada (real-time)
```

### Flujo de Actualización

```
Usuario selecciona en tabla → Datos cargan formulario → Modifica campos → SQL UPDATE → Confirmación
```

---

## Tecnologías Utilizadas

| Componente | Versión | Propósito |
|-----------|---------|----------|
| Python | 3.11.9 | Lenguaje base |
| Tkinter | Incluida en Python | Interfaz gráfica |
| SQLite3 | 3.x | Base de datos relacional |
| PyInstaller | 6.19.0 | Compilación a ejecutable |

---

## Compilación a Ejecutable

### Comando Utilizado
```bash
pyinstaller --onefile --windowed --name "Tienda_Sistema" main.py
```

### Parámetros
- `--onefile`: Genera un único archivo .exe
- `--windowed`: Sin consola (modo GUI)
- `--name`: Nombre del ejecutable
- `main.py`: Archivo principal

### Resultado
- Archivo: `Tienda_Sistema.exe` (11.8 MB)
- Ubicación: `dist/` carpeta
- Requisitos: Windows 7+, 512 MB RAM

### Dependencias Incluidas
- Python runtime (3.11.9)
- Tkinter con Tcl/Tk
- SQLite3
- Librerías del sistema

---

## Pruebas Realizadas

### Pruebas Funcionales 

- [x] **Crear Producto**: Inserta correctamente con validación
- [x] **Leer Productos**: Lista completa carga sin errores
- [x] **Buscar**: Filtrado real-time por nombre/categoría
- [x] **Actualizar**: Modifica y persiste cambios
- [x] **Eliminar**: Elimina con confirmación
- [x] **Validación**: Rechaza datos incompletos
- [x] **Base de Datos**: Conexión y persistencia funcional

### Pruebas de Ejecución 

- [x] Ejecutable abre sin errores
- [x] No requiere Python instalado
- [x] Base de datos se crea automáticamente
- [x] Datos de ejemplo cargan correctamente

---

## Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~450 |
| Funciones CRUD | 6 |
| Tablas BD | 1 |
| Registros de ejemplo | 7 |
| Campos validados | 4 |
| Campos UI | 4 |
| Botones funcionales | 5 |
| Categorías disponibles | 5 |
| Tamaño ejecutable | 11.8 MB |

---

## Ciclo de Vida de la Aplicación

```
1. INICIO
   ↓
2. Cargar archivo ejecutable
   ↓
3. Conectar a BD (crear si no existe)
   ↓
4. Cargar datos de ejemplo (primera vez)
   ↓
5. Mostrar interfaz gráfica
   ↓
6. Esperar entrada del usuario
   ↓
7. Procesar operación CRUD
   ↓
8. Actualizar vista
   ↓
9. Mostrar confirmación/error
   ↓
10. Volver a 6 o SALIR
```

---

##  Consideraciones del Estándar EC0835

✅ **Acceso a base de datos relacional**
- Implementado con SQLite

✅ **Diseño de tablas relacionales**
- 1 tabla (productos) con estructura normalizada

✅ **Operaciones CRUD completas**
- Create, Read, Update, Delete implementadas

✅ **Interfaz gráfica con Tkinter**
- Ventana principal con formularios y tabla

✅ **Mensajes de confirmación y error**
- Implementados con messageboxes contextuales

✅ **Validación de datos**
- Prevención de duplicados (ID autoincrement)
- Validación de tipos y campos obligatorios

✅ **Control de interfaz**
- Estados sincronizados entre formulario y tabla

---
**Versión:** 1.0
**Fecha:** Febrero 2026
**Desarrollador:** Alexandro Reynoso
**Estado:** Completado y compilado
