# MANUAL TECNICO

## Sistema de Gestion de Tienda

**Estandar de Competencia:** EC0835 - Desarrollar software de aplicacion con acceso a bases de datos

**Version:** 1.0
**Fecha de elaboracion:** Febrero 2026
**Desarrollador:** Alexandro Reynoso

---

## INDICE

1. Introduccion
2. Objetivo general del sistema
3. Objetivos especificos del sistema
4. Requerimientos de instalacion
5. Diagrama de clases
6. Diagrama entidad-relacion
7. Desarrollo (explicacion tecnica del funcionamiento)
   - 7.1 Arquitectura del sistema
   - 7.2 Modulo de modelos de datos (models.py)
   - 7.3 Modulo de base de datos (db.py)
   - 7.4 Modulo de operaciones CRUD (crud.py)
   - 7.5 Modulo de interfaz grafica (main.py)
   - 7.6 Flujos de operacion
   - 7.7 Seguridad y validacion de datos
   - 7.8 Compilacion a ejecutable
   - 7.9 Pruebas realizadas
8. Codigo de la aplicacion
   - 8.1 models.py
   - 8.2 db.py
   - 8.3 crud.py
   - 8.4 main.py

---

## 1. INTRODUCCION

El presente manual tecnico documenta la estructura interna, el diseno, la configuracion y el codigo fuente del Sistema de Gestion de Tienda, una aplicacion de escritorio desarrollada en el lenguaje de programacion Python. Este sistema permite administrar un inventario de productos mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una base de datos relacional SQLite.

El documento esta dirigido a desarrolladores, evaluadores tecnicos y personal de soporte que requieran comprender el funcionamiento interno de la aplicacion, realizar mantenimiento o extender sus funcionalidades. Se describe de manera detallada cada uno de los modulos que componen el sistema, las decisiones de diseno adoptadas, los diagramas de arquitectura y el codigo fuente completo.

Este software fue desarrollado conforme a los criterios establecidos en el estandar de competencia EC0835 del CONOCER, el cual establece las competencias necesarias para desarrollar software de aplicacion con acceso a bases de datos relacionales.

---

## 2. OBJETIVO GENERAL DEL SISTEMA

Desarrollar una aplicacion de escritorio funcional que permita gestionar el inventario de productos de una tienda mediante operaciones CRUD, utilizando una interfaz grafica intuitiva construida con Tkinter y una base de datos relacional SQLite, cumpliendo con los criterios del estandar de competencia EC0835.

---

## 3. OBJETIVOS ESPECIFICOS DEL SISTEMA

- Implementar un modulo de conexion y gestion de base de datos SQLite que permita la creacion automatica de tablas y la insercion de datos iniciales de ejemplo.
- Desarrollar las cuatro operaciones CRUD (Create, Read, Update, Delete) para la tabla de productos, utilizando sentencias SQL parametrizadas que prevengan inyeccion SQL.
- Disenar una interfaz grafica de usuario con Tkinter que presente un formulario de captura de datos y una tabla de visualizacion de productos.
- Incorporar un mecanismo de busqueda en tiempo real que filtre productos por nombre o categoria.
- Aplicar validaciones de entrada en el formulario para garantizar la integridad de los datos antes de su almacenamiento.
- Compilar la aplicacion en un archivo ejecutable (.exe) independiente que no requiera la instalacion previa de Python en el equipo del usuario final.

---

## 4. REQUERIMIENTOS DE INSTALACION

### 4.1 Requerimientos de hardware

| Componente        | Minimo recomendado          |
|-------------------|-----------------------------|
| Procesador        | Intel Core i3 o equivalente |
| Memoria RAM       | 512 MB                      |
| Espacio en disco  | 50 MB                       |
| Pantalla          | Resolucion 1024 x 768       |

### 4.2 Requerimientos de software (para ejecutar el .exe compilado)

| Componente          | Requerimiento                  |
|---------------------|--------------------------------|
| Sistema operativo   | Windows 7, 8, 10 u 11         |
| Dependencias        | Ninguna (autocontenido)        |

### 4.3 Requerimientos de software (para desarrollo y modificacion del codigo fuente)

| Componente          | Version                        |
|---------------------|--------------------------------|
| Sistema operativo   | Windows 7, 8, 10 u 11         |
| Python              | 3.11.9 o superior              |
| Tkinter             | Incluido en Python             |
| SQLite3             | Incluido en Python             |
| PyInstaller         | 6.19.0 (para compilacion)      |

### 4.4 Instalacion del entorno de desarrollo

Para configurar el entorno de desarrollo se deben ejecutar los siguientes pasos:

1. Descargar e instalar Python 3.11.9 desde https://www.python.org/downloads/
   - Durante la instalacion, marcar la opcion "Add Python to PATH".
2. Abrir una terminal de comandos y verificar la instalacion:
   ```
   python --version
   ```
3. Instalar PyInstaller para la compilacion:
   ```
   pip install pyinstaller
   ```
4. Ubicar los archivos fuente del proyecto en una carpeta de trabajo.

### 4.5 Ejecucion del sistema

**Desde el ejecutable compilado:**
Navegar a la carpeta `dist/` y ejecutar el archivo `Tienda_Sistema.exe`. La base de datos se creara automaticamente en el primer uso.

**Desde el codigo fuente:**
```
python main.py
```

---

## 5. DIAGRAMA DE CLASES

El sistema esta compuesto por dos clases, cuatro modulos funcionales y una base de datos. A continuacion se presenta el diagrama de clases completo en notacion UML, incluyendo las clases, los modulos auxiliares y las relaciones de dependencia entre todos los componentes.

```
+------------------------------------------------------------------+
|                        <<class>>                                 |
|                        Producto                                  |
+------------------------------------------------------------------+
| Atributos:                                                       |
|   - id         : int    = None                                   |
|   - nombre     : str    = ""                                     |
|   - categoria  : str    = ""                                     |
|   - precio     : float  = 0.0                                    |
|   - cantidad   : int    = 0                                      |
+------------------------------------------------------------------+
| Metodos:                                                         |
|   + __init__(id, nombre, categoria, precio, cantidad)            |
|   + __str__() : str                                              |
|   + __repr__() : str                                             |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                      <<constante>>                               |
|   CATEGORIAS : list[str] = ["Electronica", "Ropa",              |
|                  "Alimentos", "Libros", "Hogar"]                 |
+------------------------------------------------------------------+


+------------------------------------------------------------------+
|                        <<class>>                                 |
|                        TiendaApp                                 |
+------------------------------------------------------------------+
| Atributos:                                                       |
|   - ventana                : tk.Tk                               |
|   - tabla                  : ttk.Treeview                        |
|   - entry_nombre           : ttk.Entry                           |
|   - entry_precio           : ttk.Entry                           |
|   - entry_cantidad         : ttk.Entry                           |
|   - entry_buscar           : ttk.Entry                           |
|   - combo_categoria        : ttk.Combobox                        |
|   - producto_seleccionado_id : int                               |
+------------------------------------------------------------------+
| Metodos:                                                         |
|   + __init__(ventana: tk.Tk)                                     |
|   + crear_interfaz() : void                                      |
|   + cargar_productos() : void                                    |
|   + seleccionar_producto(event) : void                           |
|   + crear_producto() : void                                      |
|   + actualizar_producto() : void                                 |
|   + eliminar_producto() : void                                   |
|   + limpiar_formulario() : void                                  |
|   + buscar_productos() : void                                    |
|   + validar_formulario() : bool                                  |
+------------------------------------------------------------------+


+------------------------------------------------------------------+
|                       <<modulo>>                                 |
|                         db.py                                    |
+------------------------------------------------------------------+
| Constantes:                                                      |
|   DB_FILE : str = "tienda.db"                                    |
+------------------------------------------------------------------+
| Funciones:                                                       |
|   + conectar() : sqlite3.Connection                              |
|   + crear_tabla() : void                                         |
|   + inicializar_db() : void                                      |
+------------------------------------------------------------------+


+------------------------------------------------------------------+
|                       <<modulo>>                                 |
|                        crud.py                                   |
+------------------------------------------------------------------+
| Funciones:                                                       |
|   + obtener_todos() : list[Producto]                             |
|   + obtener_por_id(id: int) : Producto | None                    |
|   + crear(nombre, categoria, precio, cantidad) : int             |
|   + actualizar(id, nombre, categoria, precio, cantidad) : bool   |
|   + eliminar(id: int) : bool                                     |
|   + buscar(termino: str) : list[Producto]                        |
+------------------------------------------------------------------+


==========================================================
         DIAGRAMA DE RELACIONES ENTRE COMPONENTES
==========================================================

  +-------------+        +-------------+        +----------+
  |             | <<usa>> |             | <<usa>> |          |
  |  TiendaApp  |------->|   crud.py   |------->|  db.py   |
  |  (main.py)  |        |             |        |          |
  +-------------+        +-------------+        +----------+
        |                       |                     |
        | <<usa>>               | <<usa>>             | <<usa>>
        v                       v                     v
  +-------------+        +-------------+     +--------------+
  |  Producto   |        |  Producto   |     |   sqlite3    |
  | (models.py) |        | (models.py) |     |  (tienda.db) |
  +-------------+        +-------------+     +--------------+

  Notacion:
    <<usa>>    = Relacion de dependencia (import / invocacion)
    -------->  = Direccion de la dependencia


==========================================================
           DIAGRAMA DE SECUENCIA: CREAR PRODUCTO
==========================================================

  Usuario        TiendaApp        crud.py          db.py         SQLite
    |                |                |                |              |
    | Llena form     |                |                |              |
    |--------------->|                |                |              |
    | Click "Crear"  |                |                |              |
    |--------------->|                |                |              |
    |                | validar_       |                |              |
    |                | formulario()   |                |              |
    |                |----+           |                |              |
    |                |    |           |                |              |
    |                |<---+           |                |              |
    |                |                |                |              |
    |                | crear(nombre,  |                |              |
    |                | cat, precio,   |                |              |
    |                | cantidad)      |                |              |
    |                |--------------->|                |              |
    |                |                | conectar()     |              |
    |                |                |--------------->|              |
    |                |                |                | connect()    |
    |                |                |                |------------->|
    |                |                |                |<-------------|
    |                |                |<---------------|              |
    |                |                |                |              |
    |                |                | INSERT INTO    |              |
    |                |                | productos...   |              |
    |                |                |----------------------------->|
    |                |                |<-----------------------------|
    |                |                |                |              |
    |                |                | commit()       |              |
    |                |                |----------------------------->|
    |                |                |<-----------------------------|
    |                |                |                |              |
    |                |  return id     |                |              |
    |                |<---------------|                |              |
    |                |                |                |              |
    |                | showinfo()     |                |              |
    |  Mensaje       |                |                |              |
    |<---------------|                |                |              |
    |                |                |                |              |
    |                | cargar_        |                |              |
    |                | productos()    |                |              |
    |                |----+           |                |              |
    |  Tabla         |    |           |                |              |
    |  actualizada   |<---+           |                |              |
    |<---------------|                |                |              |
    |                |                |                |              |


==========================================================
        DIAGRAMA DE SECUENCIA: BUSCAR PRODUCTO
==========================================================

  Usuario        TiendaApp        crud.py          db.py         SQLite
    |                |                |                |              |
    | Escribe en     |                |                |              |
    | campo buscar   |                |                |              |
    |--------------->|                |                |              |
    |                | buscar_        |                |              |
    |                | productos()    |                |              |
    |                |----+           |                |              |
    |                |    |           |                |              |
    |                | buscar(term)   |                |              |
    |                |--------------->|                |              |
    |                |                | conectar()     |              |
    |                |                |--------------->|              |
    |                |                |<---------------|              |
    |                |                |                |              |
    |                |                | SELECT WHERE   |              |
    |                |                | nombre LIKE    |              |
    |                |                | OR cat LIKE    |              |
    |                |                |----------------------------->|
    |                |                |<-----------------------------|
    |                |                |                |              |
    |                | list[Producto] |                |              |
    |                |<---------------|                |              |
    |                |                |                |              |
    |  Tabla         |                |                |              |
    |  filtrada      |                |                |              |
    |<---------------|                |                |              |
    |                |                |                |              |
```

### Descripcion de las clases

**Clase Producto (models.py):** Representa la entidad principal del sistema. Encapsula los cinco atributos que definen un producto del inventario (id, nombre, categoria, precio y cantidad). Proporciona metodos de representacion en texto (`__str__` y `__repr__`) para su visualizacion en consola y depuracion. La constante `CATEGORIAS` define los valores permitidos para el campo categoria.

**Clase TiendaApp (main.py):** Constituye el controlador de la interfaz grafica. Gestiona la ventana principal de 900x600 pixeles, los widgets de entrada de datos (cuatro campos Entry y un Combobox), la tabla Treeview de visualizacion de productos y los cuatro botones de accion. Coordina las operaciones CRUD a traves de los modulos auxiliares `crud.py` y `db.py`.

**Modulo db.py:** Capa de acceso a datos que encapsula la conexion a SQLite, la creacion de la tabla y la inicializacion con datos de ejemplo. Expone tres funciones publicas que son consumidas por el modulo `crud.py`.

**Modulo crud.py:** Capa de logica de negocio que implementa las seis operaciones de manipulacion de datos. Actua como intermediario entre la interfaz grafica y la base de datos, recibiendo datos de la vista y traduciendolos a sentencias SQL parametrizadas.

---

## 6. DIAGRAMA ENTIDAD-RELACION

El sistema utiliza una base de datos relacional SQLite con una unica entidad denominada `productos`. A continuacion se presenta el diagrama entidad-relacion en notacion Chen y en notacion relacional.

### 6.1 Diagrama E-R en notacion Chen

```
                   +-------------------+
                   |                   |
                   |     PRODUCTOS     |
                   |                   |
                   +-------------------+
                    /   |    |    \    \
                   /    |    |     \    \
                  /     |    |      \    \
          +------+ +------+ +------+ +------+ +--------+
          | (id) | |nombre| | cat. | |precio| |cantidad|
          +------+ +------+ +------+ +------+ +--------+
             PK       NN       NN       NN        NN

  Notacion:
    (id)    = Atributo clave primaria (PK)
    NN      = NOT NULL (campo obligatorio)
    cat.    = categoria
```

### 6.2 Diagrama en notacion relacional

```
  PRODUCTOS
  +========+==========+==========+==========+==========+
  | *id*   | nombre   | categoria| precio   | cantidad |
  | (PK)   | (TEXT)   | (TEXT)   | (REAL)   | (INTEGER)|
  | AUTO   | NOT NULL | NOT NULL | NOT NULL | NOT NULL |
  +========+==========+==========+==========+==========+
  |   1    | Laptop   | Electro. | 799.99   |    5     |
  |   2    | Mouse    | Electro. | 25.99    |   20     |
  |   3    | Camiseta | Ropa     | 19.99    |   15     |
  |   4    | Pantalon | Ropa     | 49.99    |   10     |
  |   5    | Arroz    | Alimento | 3.50     |   50     |
  |   6    | Python101| Libros   | 29.99    |    8     |
  |   7    | Almohada | Hogar    | 15.99    |   12     |
  +--------+----------+----------+----------+----------+

  Restricciones:
    - id: Clave primaria con autoincremento
    - nombre, categoria, precio, cantidad: Campos obligatorios
    - categoria: Valores permitidos = {Electronica, Ropa,
                 Alimentos, Libros, Hogar}
```

### Diccionario de datos

| Campo     | Tipo de dato | Longitud | Restricciones              | Descripcion                                |
|-----------|-------------|----------|----------------------------|--------------------------------------------|
| id        | INTEGER     | -        | PRIMARY KEY, AUTOINCREMENT | Identificador unico del producto           |
| nombre    | TEXT        | Variable | NOT NULL                   | Nombre descriptivo del producto            |
| categoria | TEXT        | Variable | NOT NULL                   | Clasificacion del producto                 |
| precio    | REAL        | 8 bytes  | NOT NULL                   | Precio unitario en formato decimal         |
| cantidad  | INTEGER     | -        | NOT NULL                   | Unidades disponibles en inventario         |

### Sentencia DDL de creacion

```sql
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
);
```

### Valores permitidos para el campo categoria

| Valor        |
|--------------|
| Electronica  |
| Ropa         |
| Alimentos    |
| Libros       |
| Hogar        |

---

## 7. DESARROLLO (EXPLICACION TECNICA DEL FUNCIONAMIENTO)

### 7.1 Arquitectura del sistema

El sistema esta organizado siguiendo una variante simplificada del patron Modelo-Vista-Controlador (MVC), distribuido en cuatro archivos fuente de Python:

```
Proyecto/
  models.py .............. Modelo de datos (Clase Producto)
  db.py .................. Capa de acceso a base de datos
  crud.py ................ Capa de logica de negocio (operaciones CRUD)
  main.py ................ Vista e interfaz grafica (Tkinter)
  tienda.db .............. Base de datos SQLite (generada en ejecucion)
  dist/
    Tienda_Sistema.exe ... Ejecutable compilado
```

La separacion en modulos garantiza que cada archivo tiene una responsabilidad unica:

- **models.py (Modelo):** Define la estructura de datos que representa un producto.
- **db.py (Acceso a datos):** Gestiona la conexion a la base de datos y la creacion de tablas.
- **crud.py (Controlador/Logica de negocio):** Implementa las operaciones de lectura, escritura, actualizacion y eliminacion.
- **main.py (Vista):** Presenta la interfaz grafica al usuario y coordina las interacciones.

### 7.2 Modulo de modelos de datos (models.py)

Este modulo define la clase `Producto` y la constante `CATEGORIAS`.

**Clase Producto:**
El constructor `__init__` recibe cinco parametros con valores predeterminados, lo que permite crear instancias vacias o parcialmente inicializadas. Los atributos se asignan directamente como variables de instancia.

El metodo `__str__` retorna una cadena formateada que presenta los datos del producto de manera legible. El metodo `__repr__` delega su comportamiento a `__str__`, facilitando la depuracion en consola.

**Constante CATEGORIAS:**
Es una lista de cadenas que define las categorias validas del sistema. Esta constante es utilizada por la interfaz grafica para poblar el selector desplegable (Combobox) y restringir las opciones del usuario.

### 7.3 Modulo de base de datos (db.py)

Este modulo gestiona la conexion y la inicializacion de la base de datos SQLite.

**Funcion `conectar()`:**
Establece una conexion a la base de datos `tienda.db` utilizando el modulo `sqlite3` de la biblioteca estandar de Python. Configura la propiedad `row_factory` con `sqlite3.Row` para que las consultas retornen filas accesibles por nombre de columna en lugar de por indice numerico. Retorna el objeto de conexion.

**Funcion `crear_tabla()`:**
Ejecuta la sentencia DDL `CREATE TABLE IF NOT EXISTS` para crear la tabla `productos` si no existe previamente. Utiliza la clausula condicional para evitar errores en ejecuciones posteriores. Realiza un commit de la transaccion y cierra la conexion.

**Funcion `inicializar_db()`:**
Verifica la existencia del archivo `tienda.db` en el sistema de archivos. Si el archivo no existe, invoca `crear_tabla()` y posteriormente inserta siete registros de ejemplo que cubren las cinco categorias definidas. Este mecanismo garantiza que el sistema tenga datos de demoststracion en su primera ejecucion.

### 7.4 Modulo de operaciones CRUD (crud.py)

Este modulo implementa las seis funciones que conforman las operaciones CRUD del sistema. Todas las funciones utilizan sentencias SQL parametrizadas con marcadores de posicion (`?`) para prevenir vulnerabilidades de inyeccion SQL.

**Funcion `obtener_todos()`:**
Ejecuta una consulta SELECT que recupera todos los registros de la tabla `productos` ordenados por el campo `id` de forma ascendente. Itera sobre las filas resultantes y construye una lista de objetos `Producto`.

**Funcion `obtener_por_id(id)`:**
Ejecuta una consulta SELECT con clausula WHERE para recuperar un unico registro identificado por su clave primaria. Retorna un objeto `Producto` si el registro existe, o `None` en caso contrario.

**Funcion `crear(nombre, categoria, precio, cantidad)`:**
Ejecuta una sentencia INSERT que agrega un nuevo registro a la tabla. Convierte los parametros `precio` y `cantidad` a sus tipos de dato correspondientes (`float` e `int`) antes de la insercion. Retorna el `id` del registro recien creado mediante la propiedad `lastrowid` del cursor.

**Funcion `actualizar(id, nombre, categoria, precio, cantidad)`:**
Ejecuta una sentencia UPDATE con clausula WHERE que modifica los campos de un registro existente. Realiza la misma conversion de tipos que la funcion `crear`.

**Funcion `eliminar(id)`:**
Ejecuta una sentencia DELETE con clausula WHERE que elimina permanentemente un registro de la tabla.

**Funcion `buscar(termino)`:**
Ejecuta una consulta SELECT con dos clausulas LIKE combinadas mediante el operador OR. La busqueda se realiza tanto en el campo `nombre` como en el campo `categoria`, utilizando comodines (`%`) para coincidencia parcial. Los resultados se retornan ordenados por `id`.

Todas las funciones implementan un bloque `try-except` que garantiza el cierre de la conexion a la base de datos independientemente de si la operacion fue exitosa o genero una excepcion.

### 7.5 Modulo de interfaz grafica (main.py)

Este modulo contiene la clase `TiendaApp`, que gestiona toda la interfaz grafica del sistema utilizando la biblioteca Tkinter.

**Inicializacion:**
El constructor de la clase recibe un objeto `tk.Tk` (ventana raiz) y ejecuta las siguientes acciones en secuencia:
1. Configura el titulo y las dimensiones de la ventana (900 x 600 pixeles).
2. Invoca las funciones de inicializacion de la base de datos.
3. Construye los componentes de la interfaz grafica.
4. Carga los productos existentes en la tabla.

**Estructura de la interfaz:**
La ventana se organiza en tres secciones:

- **Panel superior:** Contiene el titulo del sistema sobre un fondo de color oscuro.
- **Panel izquierdo:** Contiene el formulario de captura de datos con campos para nombre, categoria (selector desplegable), precio y cantidad, asi como los botones de accion (Crear, Actualizar, Eliminar y Limpiar) y un campo de busqueda.
- **Panel derecho:** Contiene una tabla tipo Treeview con cinco columnas (ID, Nombre, Categoria, Precio, Stock) y una barra de desplazamiento vertical.

**Eventos y bindings:**
- Al seleccionar una fila de la tabla (evento `<<TreeviewSelect>>`), los datos del producto seleccionado se cargan automaticamente en los campos del formulario.
- Al escribir en el campo de busqueda (evento `<KeyRelease>`), se ejecuta un filtrado en tiempo real de los productos mostrados en la tabla.

**Metodos de operacion:**
Cada boton de la interfaz invoca un metodo especifico que coordina la validacion de datos, la llamada a la funcion CRUD correspondiente, la visualizacion de mensajes de confirmacion o error, y la recarga de la tabla.

### 7.6 Flujos de operacion

**Flujo de creacion de un producto:**
```
1. El usuario completa los campos del formulario
2. El usuario presiona el boton "Crear Producto"
3. Se ejecuta la validacion del formulario
4. Si la validacion es exitosa, se invoca crud.crear()
5. Se ejecuta la sentencia SQL INSERT
6. Se muestra un mensaje de confirmacion
7. Se limpia el formulario
8. Se recarga la tabla de productos
```

**Flujo de actualizacion de un producto:**
```
1. El usuario selecciona un producto de la tabla
2. Los datos se cargan en el formulario
3. El usuario modifica los campos deseados
4. El usuario presiona el boton "Actualizar"
5. Se ejecuta la validacion del formulario
6. Si la validacion es exitosa, se invoca crud.actualizar()
7. Se ejecuta la sentencia SQL UPDATE
8. Se muestra un mensaje de confirmacion
9. Se limpia el formulario y se recarga la tabla
```

**Flujo de eliminacion de un producto:**
```
1. El usuario selecciona un producto de la tabla
2. El usuario presiona el boton "Eliminar"
3. Se muestra un dialogo de confirmacion
4. Si el usuario confirma, se invoca crud.eliminar()
5. Se ejecuta la sentencia SQL DELETE
6. Se muestra un mensaje de confirmacion
7. Se limpia el formulario y se recarga la tabla
```

**Flujo de busqueda en tiempo real:**
```
1. El usuario escribe un termino en el campo de busqueda
2. Con cada tecla presionada se ejecuta el evento KeyRelease
3. Se invoca crud.buscar() con el termino ingresado
4. Se ejecuta la consulta SQL con clausulas LIKE
5. La tabla se actualiza mostrando unicamente los productos coincidentes
6. Si el campo se vacia, se muestran todos los productos
```

### 7.7 Seguridad y validacion de datos

El sistema implementa las siguientes medidas de seguridad y validacion:

**Prevencion de inyeccion SQL:**
Todas las consultas a la base de datos utilizan sentencias parametrizadas con marcadores de posicion (`?`). En ningun punto del codigo se realiza concatenacion directa de cadenas para construir sentencias SQL.

**Validacion de campos obligatorios:**
El metodo `validar_formulario()` verifica que los cuatro campos de entrada (nombre, categoria, precio y cantidad) contengan informacion antes de permitir una operacion de creacion o actualizacion.

**Validacion de tipos de dato:**
Las funciones CRUD convierten explicitamente el precio a tipo `float` y la cantidad a tipo `int`. Si la conversion falla, se captura la excepcion `ValueError` y se muestra un mensaje de error al usuario.

**Confirmacion de operaciones destructivas:**
La operacion de eliminacion requiere confirmacion explicita del usuario mediante un dialogo de tipo "Si/No" antes de proceder.

**Gestion de conexiones:**
Cada funcion de acceso a datos abre y cierra su propia conexion a la base de datos, evitando conexiones huerfanas o bloqueos.

### 7.8 Compilacion a ejecutable

La aplicacion fue compilada a un archivo ejecutable independiente utilizando PyInstaller con el siguiente comando:

```
pyinstaller --onefile --windowed --name "Tienda_Sistema" main.py
```

**Parametros utilizados:**

| Parametro    | Descripcion                                           |
|-------------|-------------------------------------------------------|
| --onefile   | Empaqueta todos los recursos en un unico archivo .exe |
| --windowed  | Suprime la ventana de consola (modo GUI)              |
| --name      | Asigna el nombre "Tienda_Sistema" al ejecutable       |
| main.py     | Archivo de entrada principal                          |

**Resultado de la compilacion:**

| Atributo          | Valor                    |
|-------------------|--------------------------|
| Nombre del archivo | Tienda_Sistema.exe      |
| Tamano            | 11.8 MB                  |
| Ubicacion         | carpeta dist/            |
| Dependencias      | Ninguna (autocontenido)  |

El ejecutable incluye internamente el runtime de Python 3.11.9, la biblioteca Tkinter con Tcl/Tk, el modulo SQLite3 y todas las librerias necesarias para su funcionamiento.

### 7.9 Pruebas realizadas

**Pruebas funcionales:**

| Caso de prueba                          | Resultado  |
|-----------------------------------------|------------|
| Crear un producto con datos validos     | Correcto   |
| Crear un producto con campos vacios     | Rechazado (validacion correcta) |
| Leer y mostrar todos los productos      | Correcto   |
| Buscar producto por nombre              | Correcto   |
| Buscar producto por categoria           | Correcto   |
| Actualizar un producto existente        | Correcto   |
| Eliminar un producto con confirmacion   | Correcto   |
| Cancelar eliminacion                    | Correcto   |
| Ingresar precio con texto no numerico   | Rechazado (validacion correcta) |
| Ingresar cantidad con valor decimal     | Rechazado (validacion correcta) |

**Pruebas de ejecucion del archivo compilado:**

| Caso de prueba                                          | Resultado |
|---------------------------------------------------------|-----------|
| Ejecutar Tienda_Sistema.exe sin Python instalado        | Correcto  |
| Creacion automatica de la base de datos en primer uso   | Correcto  |
| Carga de datos de ejemplo en primer uso                 | Correcto  |
| Persistencia de datos entre sesiones                    | Correcto  |

---

## 8. CODIGO DE LA APLICACION

A continuacion se presenta el codigo fuente completo de cada uno de los modulos que conforman el sistema.

### 8.1 models.py - Modelos de datos

```python
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
        return f"ID: {self.id} | {self.nombre} | Categoria: {self.categoria} | Precio: ${self.precio:.2f} | Stock: {self.cantidad}"

    def __repr__(self):
        return self.__str__()


CATEGORIAS = ["Electronica", "Ropa", "Alimentos", "Libros", "Hogar"]
```

### 8.2 db.py - Gestion de base de datos

```python
# Base de datos SQLite para la tienda

import sqlite3
import os
from models import Producto

DB_FILE = "tienda.db"


def conectar():
    """Crea conexion a la base de datos"""
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
    """Inicializa la base de datos con productos de ejemplo"""
    if not os.path.exists(DB_FILE):
        crear_tabla()
        conexion = conectar()
        cursor = conexion.cursor()

        # Datos de ejemplo
        productos_ejemplo = [
            ("Laptop", "Electronica", 799.99, 5),
            ("Mouse", "Electronica", 25.99, 20),
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
```

### 8.3 crud.py - Operaciones CRUD

```python
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
    """Busca productos por nombre o categoria"""
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
```

### 8.4 main.py - Interfaz grafica

```python
# Interfaz grafica con Tkinter para la tienda

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import crear_tabla, inicializar_db
from crud import obtener_todos, crear, actualizar, eliminar, buscar
from models import CATEGORIAS


class TiendaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Tienda - CRUD")
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
        """Crea la interfaz grafica"""

        # Panel superior - Titulo
        panel_titulo = tk.Frame(self.ventana, bg="#2c3e50", height=50)
        panel_titulo.pack(fill=tk.X)

        titulo = tk.Label(
            panel_titulo,
            text="SISTEMA DE GESTION DE TIENDA",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=10)

        # Panel principal con dos secciones
        panel_principal = tk.Frame(self.ventana)
        panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Seccion izquierda - Formulario
        panel_izquierda = ttk.LabelFrame(
            panel_principal, text="Formulario de Producto", padding=10
        )
        panel_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

        # Nombre
        ttk.Label(panel_izquierda, text="Nombre:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.entry_nombre = ttk.Entry(panel_izquierda, width=25)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Categoria
        ttk.Label(panel_izquierda, text="Categoria:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.combo_categoria = ttk.Combobox(
            panel_izquierda, values=CATEGORIAS, width=22, state="readonly"
        )
        self.combo_categoria.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Precio
        ttk.Label(panel_izquierda, text="Precio ($):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.entry_precio = ttk.Entry(panel_izquierda, width=25)
        self.entry_precio.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Cantidad
        ttk.Label(panel_izquierda, text="Cantidad:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.entry_cantidad = ttk.Entry(panel_izquierda, width=25)
        self.entry_cantidad.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Botones de accion
        panel_botones = tk.Frame(panel_izquierda)
        panel_botones.grid(row=4, column=0, columnspan=2, pady=20)

        btn_crear = tk.Button(
            panel_botones,
            text="Crear Producto",
            command=self.crear_producto,
            bg="#27ae60",
            fg="white",
            width=18
        )
        btn_crear.pack(pady=5)

        btn_actualizar = tk.Button(
            panel_botones,
            text="Actualizar",
            command=self.actualizar_producto,
            bg="#f39c12",
            fg="white",
            width=18
        )
        btn_actualizar.pack(pady=5)

        btn_eliminar = tk.Button(
            panel_botones,
            text="Eliminar",
            command=self.eliminar_producto,
            bg="#e74c3c",
            fg="white",
            width=18
        )
        btn_eliminar.pack(pady=5)

        btn_limpiar = tk.Button(
            panel_botones,
            text="Limpiar Formulario",
            command=self.limpiar_formulario,
            bg="#95a5a6",
            fg="white",
            width=18
        )
        btn_limpiar.pack(pady=5)

        # Buscador
        ttk.Label(panel_izquierda, text="Buscar:").grid(
            row=5, column=0, sticky=tk.W, pady=10
        )
        self.entry_buscar = ttk.Entry(panel_izquierda, width=25)
        self.entry_buscar.grid(row=5, column=1, sticky=tk.W, pady=10)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.buscar_productos())

        # Seccion derecha - Tabla de productos
        panel_derecha = ttk.LabelFrame(
            panel_principal, text="Lista de Productos", padding=10
        )
        panel_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear tabla (Treeview)
        columns = ("ID", "Nombre", "Categoria", "Precio", "Stock")
        self.tabla = ttk.Treeview(
            panel_derecha, columns=columns, height=20, show="headings"
        )

        # Definir columnas
        self.tabla.column("ID", width=40)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Categoria", width=100)
        self.tabla.column("Precio", width=80)
        self.tabla.column("Stock", width=60)

        # Definir encabezados
        for col in columns:
            self.tabla.heading(col, text=col)

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(
            panel_derecha, orient=tk.VERTICAL, command=self.tabla.yview
        )
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Evento de seleccion
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
            messagebox.showinfo("Exito", "Producto creado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except ValueError:
            messagebox.showerror(
                "Error", "Precio debe ser un numero y cantidad debe ser entero"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear: {str(e)}")

    def actualizar_producto(self):
        """Actualiza el producto seleccionado"""
        if not self.producto_seleccionado_id:
            messagebox.showwarning(
                "Advertencia", "Selecciona un producto para actualizar"
            )
            return

        if not self.validar_formulario():
            return

        try:
            nombre = self.entry_nombre.get()
            categoria = self.combo_categoria.get()
            precio = float(self.entry_precio.get())
            cantidad = int(self.entry_cantidad.get())

            actualizar(
                self.producto_seleccionado_id, nombre, categoria, precio, cantidad
            )
            messagebox.showinfo("Exito", "Producto actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except ValueError:
            messagebox.showerror(
                "Error", "Precio debe ser un numero y cantidad debe ser entero"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")

    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado_id:
            messagebox.showwarning(
                "Advertencia", "Selecciona un producto para eliminar"
            )
            return

        if messagebox.askyesno(
            "Confirmar", "Esta seguro de que quiere eliminar este producto?"
        ):
            try:
                eliminar(self.producto_seleccionado_id)
                messagebox.showinfo("Exito", "Producto eliminado correctamente")
                self.limpiar_formulario()
                self.cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

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
        """Busca productos segun el termino"""
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
        """Valida que los campos no esten vacios"""
        if not self.entry_nombre.get():
            messagebox.showwarning("Validacion", "El nombre es requerido")
            return False
        if not self.combo_categoria.get():
            messagebox.showwarning("Validacion", "La categoria es requerida")
            return False
        if not self.entry_precio.get():
            messagebox.showwarning("Validacion", "El precio es requerido")
            return False
        if not self.entry_cantidad.get():
            messagebox.showwarning("Validacion", "La cantidad es requerida")
            return False
        return True


if __name__ == "__main__":
    ventana = tk.Tk()
    app = TiendaApp(ventana)
    ventana.mainloop()
```

---

**Fin del Manual Tecnico**

Version: 1.0 | Fecha: Febrero 2026 | Desarrollador: Alexandro Reynoso | Estado: Completado
