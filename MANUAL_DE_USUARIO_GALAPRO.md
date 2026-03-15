# MANUAL DE USUARIO

## Sistema de Gestion de Clientes y Eventos — GalaPro

---

## PORTADA

**GalaPro — Sistema de Gestion de Clientes y Eventos**

Software de aplicacion con acceso a base de datos

Estandar de Competencia: EC0835

Desarrollador: Alexandro Reynoso

Fecha: Marzo 2026

Version: 1.0

---

## PAGINA DE TITULO

**Nombre del sistema:** GalaPro — Sistema de Gestion de Clientes y Eventos

**Tipo de aplicacion:** Aplicacion de escritorio

**Lenguaje de programacion:** Python 3.11.9

**Base de datos:** SQLite

**Interfaz grafica:** Tkinter

**Archivo ejecutable:** GalaPro_Sistema.exe

---

## INDICE

1. Introduccion
2. Requisitos de instalacion
3. Instrucciones de instalacion y configuracion
4. Guia para el uso de las funciones basicas del sistema
   - 4.1 Inicio de sesion
   - 4.2 Pantalla principal
   - 4.3 Modulo de Clientes
     - 4.3.1 Registrar un cliente
     - 4.3.2 Consultar clientes
     - 4.3.3 Actualizar un cliente
     - 4.3.4 Eliminar un cliente
     - 4.3.5 Buscar clientes
   - 4.4 Modulo de Eventos
     - 4.4.1 Registrar un evento
     - 4.4.2 Consultar eventos
     - 4.4.3 Actualizar un evento
     - 4.4.4 Cambiar el estatus de un evento
     - 4.4.5 Eliminar un evento
   - 4.5 Reporte de Eventos por Cliente (JOIN)
   - 4.6 Reporte Total de Eventos por Cliente (GROUP BY)
   - 4.7 Respaldar la base de datos
   - 4.8 Restaurar la base de datos
5. Mensajes del sistema y solucion de problemas
6. Glosario

---

## 1. INTRODUCCION

GalaPro es una aplicacion de escritorio disenada para la agencia de eventos GalaPro. Permite registrar, organizar y consultar la cartera de clientes y los eventos contratados por cada uno de ellos.

El sistema reemplaza el registro manual en agendas y archivos de texto, ofreciendo una interfaz grafica moderna que permite gestionar toda la informacion de manera segura, rapida y sin necesidad de conexion a internet.

Con GalaPro podras:

- Registrar clientes con su codigo interno, nombre, telefono y fecha de registro.
- Registrar eventos asociados a cada cliente, con tipo, descripcion, estatus y fecha.
- Consultar reportes cruzados entre clientes y sus eventos.
- Respaldar y restaurar la base de datos desde la propia interfaz.

Todos los datos se guardan automaticamente en una base de datos local, por lo que la informacion se mantiene aunque se cierre y se vuelva a abrir el programa.

---

## 2. REQUISITOS DE INSTALACION

### Lo que necesita tu computadora

**Sistema operativo:** Windows 7, 8, 10 u 11.

**Procesador:** Intel Core i3 o equivalente como minimo.

**Memoria RAM:** Al menos 512 MB.

**Espacio en disco:** 50 MB disponibles.

**Pantalla:** Resolucion minima de 1024 x 768 pixeles.

No se necesita instalar ningun programa adicional. El archivo ejecutable ya incluye todo lo necesario para funcionar.

---

## 3. INSTRUCCIONES DE INSTALACION Y CONFIGURACION

### Paso 1: Obtener el archivo

Copia el archivo `GalaPro_Sistema.exe` a la carpeta donde deseas instalar el sistema (por ejemplo, en el Escritorio o en Documentos).

### Paso 2: Ejecutar la aplicacion

Haz doble clic en el archivo `GalaPro_Sistema.exe`.

La primera vez que se abra, se creara automaticamente la base de datos `galapro.db` en la misma carpeta donde esta el ejecutable.

### Paso 3: Iniciar sesion

Al abrir la aplicacion se mostrara la pantalla de inicio de sesion. Las credenciales iniciales son:

- **Usuario:** admin
- **Contrasena:** admin123

### Paso 4: Listo

No hay nada mas que configurar. La aplicacion esta lista para usarse.

**Nota:** Si Windows muestra un aviso de seguridad al abrir el archivo por primera vez, haz clic en "Mas informacion" y luego en "Ejecutar de todas formas".

---

## 4. GUIA PARA EL USO DE LAS FUNCIONES BASICAS DEL SISTEMA

### 4.1 Inicio de sesion

Al abrir la aplicacion aparece la ventana de acceso con dos campos:

- **Usuario:** Escribe tu nombre de usuario.
- **Contrasena:** Escribe tu contrasena.

Presiona el boton **"Ingresar"** o la tecla **Enter** para entrar al sistema.

Si los datos son incorrectos, aparecera un mensaje de error y podras intentarlo de nuevo.

### 4.2 Pantalla principal

Despues de iniciar sesion se muestra la ventana principal del sistema. Tiene:

- **Barra superior:** Muestra el nombre del sistema y los botones de Respaldar y Restaurar la base de datos.
- **Pestanas de navegacion:** Cuatro pestanas para acceder a cada modulo:
  - Clientes
  - Eventos
  - Eventos por Cliente (JOIN)
  - Total de Eventos por Cliente (GROUP BY)

### 4.3 Modulo de Clientes

#### 4.3.1 Registrar un cliente

Para dar de alta un nuevo cliente:

1. Ve a la pestana **"Clientes"**.
2. Llena los campos del formulario en la parte superior:
   - **Codigo Interno (RFC/No.):** El identificador unico del cliente. Ejemplo: RFC001 o 1234567.
   - **Nombre Completo:** El nombre completo del cliente.
   - **Telefono:** Numero de telefono de contacto.
   - **Fecha de Registro (DD/MM/AAAA):** La fecha en que se registra el cliente. Ejemplo: 15/03/2026.
3. Haz clic en el boton **"Agregar"**.
4. Si todo esta correcto, aparecera el mensaje "Cliente registrado correctamente".
5. El nuevo cliente se mostrara en la tabla inferior.

**Importante:** El Codigo Interno debe ser unico. No se puede registrar dos clientes con el mismo codigo.

#### 4.3.2 Consultar clientes

Los clientes registrados se muestran automaticamente en la tabla con las columnas:

- **ID:** Numero unico asignado automaticamente por el sistema.
- **Codigo:** El codigo interno del cliente (RFC o numero).
- **Nombre:** Nombre completo del cliente.
- **Telefono:** Numero de contacto.
- **Fecha de Registro:** Fecha en que fue registrado.

#### 4.3.3 Actualizar un cliente

Para modificar los datos de un cliente existente:

1. Haz clic sobre el cliente en la tabla. Sus datos se cargaran en el formulario.
2. Modifica los campos que necesites.
3. Haz clic en el boton **"Actualizar"**.
4. Aparecera el mensaje "Cliente actualizado".

#### 4.3.4 Eliminar un cliente

Para borrar un cliente:

1. Haz clic sobre el cliente en la tabla.
2. Haz clic en el boton **"Eliminar"**.
3. Aparecera un mensaje de confirmacion.
4. Haz clic en **"Si"** para confirmar.

**Atencion:** Al eliminar un cliente se eliminaran tambien TODOS sus eventos asociados.

#### 4.3.5 Buscar clientes

1. Escribe en el campo **"Buscar"** el nombre, codigo o telefono del cliente.
2. La tabla se filtrara automaticamente conforme escribes.
3. Para volver a ver todos los clientes, borra el texto del campo de busqueda.

### 4.4 Modulo de Eventos

#### 4.4.1 Registrar un evento

Para dar de alta un nuevo evento:

1. Ve a la pestana **"Eventos"**.
2. Llena los campos del formulario:
   - **Cliente:** Selecciona del menu desplegable el cliente al que pertenece el evento.
   - **Nombre / Tipo de Evento:** Selecciona o escribe el tipo. Ejemplos: Boda, Cumpleanos, Conferencia.
   - **Estatus:** Selecciona el estatus inicial. Por defecto es "Cotizado".
   - **Fecha del Evento (DD/MM/AAAA):** Fecha en que se realizara el evento. Ejemplo: 20/04/2026.
   - **Descripcion:** Descripcion breve de los requerimientos del evento.
3. Haz clic en el boton **"Agregar"**.
4. Aparecera el mensaje "Evento registrado correctamente".

#### 4.4.2 Consultar eventos

La tabla de eventos muestra las columnas:

- **ID:** Numero unico del evento.
- **Cliente:** Nombre del cliente al que pertenece.
- **Nombre/Tipo:** El tipo de evento.
- **Descripcion:** Los requerimientos del evento.
- **Estatus:** Estado actual (Cotizado, Confirmado, Realizado o Cancelado).
- **Fecha Evento:** Fecha en que se realizara.

#### 4.4.3 Actualizar un evento

1. Haz clic sobre el evento en la tabla.
2. Modifica los campos necesarios en el formulario.
3. Haz clic en **"Actualizar"**.

#### 4.4.4 Cambiar el estatus de un evento

El estatus indica en que etapa se encuentra el evento. Los valores posibles son:

| Estatus    | Significado                                      |
|------------|--------------------------------------------------|
| Cotizado   | Se entrego una cotizacion al cliente             |
| Confirmado | El cliente acepto y confirmo el evento           |
| Realizado  | El evento ya se llevo a cabo                     |
| Cancelado  | El evento fue cancelado                          |

Para cambiar el estatus:

1. Haz clic sobre el evento en la tabla.
2. Cambia el campo **"Estatus"** al nuevo valor en el menu desplegable.
3. Haz clic en el boton **"Cambiar Estatus"** (color morado).
4. Aparecera el mensaje con el nuevo estatus asignado.

#### 4.4.5 Eliminar un evento

1. Haz clic sobre el evento en la tabla.
2. Haz clic en **"Eliminar"**.
3. Confirma la accion en el mensaje que aparece.

### 4.5 Reporte de Eventos por Cliente (JOIN)

Esta pestana muestra una tabla combinada con la informacion completa de cada evento junto con los datos del cliente al que pertenece.

Columnas que muestra:

- ID del Evento
- Codigo del Cliente
- Nombre del Cliente
- Tipo de Evento
- Descripcion
- Estatus
- Fecha del Evento

Usa el boton **"Actualizar"** para refrescar los datos si realizaste cambios recientes.

### 4.6 Reporte Total de Eventos por Cliente (GROUP BY)

Esta pestana muestra cuantos eventos tiene registrados cada cliente. Es util para saber que clientes son los mas activos.

Columnas que muestra:

- Codigo del Cliente
- Nombre del Cliente
- Total de Eventos

Los resultados se ordenan de mayor a menor cantidad de eventos.

Usa el boton **"Actualizar"** para refrescar los datos.

### 4.7 Respaldar la base de datos

Para crear una copia de seguridad de todos los datos:

1. Haz clic en el boton **"Respaldar BD"** (azul) en la barra superior.
2. El sistema creara automaticamente un archivo de respaldo en la carpeta:
   `[carpeta del ejecutable]\backup\`
3. El archivo tendra un nombre con la fecha y hora. Ejemplo:
   `galapro_backup_20260315_143022.db`
4. Aparecera un mensaje confirmando la ruta donde se guardo.

Se recomienda hacer un respaldo antes de realizar cambios importantes o al finalizar cada jornada de trabajo.

### 4.8 Restaurar la base de datos

Para recuperar los datos desde un respaldo:

1. Haz clic en el boton **"Restaurar BD"** (naranja) en la barra superior.
2. Se abrira el explorador de archivos directamente en la carpeta de respaldos.
3. Selecciona el archivo de respaldo que deseas restaurar.
4. Confirma la accion en el mensaje que aparece.
5. Los datos se restauraran y la pantalla se actualizara automaticamente.

**Atencion:** Al restaurar, los datos actuales seran reemplazados por los del respaldo seleccionado.

---

## 5. MENSAJES DEL SISTEMA Y SOLUCION DE PROBLEMAS

### Mensajes de exito

**"Cliente registrado correctamente":** El cliente se dio de alta en el sistema.

**"Cliente actualizado":** Los cambios del cliente se guardaron.

**"Cliente eliminado":** El cliente y sus eventos fueron borrados.

**"Evento registrado correctamente":** El evento se dio de alta en el sistema.

**"Evento actualizado":** Los cambios del evento se guardaron.

**"Estatus actualizado a: [estatus]":** El estatus del evento cambio correctamente.

**"Evento eliminado":** El evento fue borrado.

**"Respaldo guardado exitosamente en: [ruta]":** El respaldo se creo correctamente.

**"Base de datos restaurada correctamente":** Los datos se recuperaron del respaldo.

### Mensajes de advertencia

**"El codigo interno es obligatorio":** El campo Codigo no puede estar vacio.

**"El nombre del cliente es obligatorio":** El campo Nombre no puede estar vacio.

**"Fecha de registro invalida. Use DD/MM/AAAA":** Verifica que la fecha tenga el formato correcto. Ejemplo: 15/03/2026.

**"Selecciona un cliente":** Elige un cliente del menu desplegable antes de registrar el evento.

**"El nombre/tipo del evento es obligatorio":** El campo Nombre/Tipo no puede estar vacio.

**"Fecha del evento invalida. Use DD/MM/AAAA":** Verifica el formato de la fecha del evento.

**"Selecciona un evento de la tabla primero":** Haz clic en un evento antes de presionar Actualizar, Cambiar Estatus o Eliminar.

### Mensajes de error

**"El codigo [codigo] ya existe":** El codigo interno que intentas usar ya esta registrado para otro cliente. Usa un codigo diferente.

**"Acceso denegado. Usuario o contrasena incorrectos":** Verifica que el usuario y la contrasena sean correctos.

### Problemas comunes

**La aplicacion no abre:**
- Verifica que tu sistema sea Windows 7 o superior.
- Si aparece un aviso de seguridad, haz clic en "Mas informacion" y luego en "Ejecutar de todas formas".

**El combo de clientes en Eventos aparece vacio:**
- Primero registra al menos un cliente en la pestana "Clientes".
- Cambia de pestana y vuelve a "Eventos", el combo se actualizara automaticamente.

**No puedo copiar el ejecutable (archivo ocupado):**
- Cierra la aplicacion completamente antes de mover o reemplazar el archivo .exe.

**La base de datos aparece bloqueada:**
- Asegurate de tener solo una instancia del programa abierta a la vez.

---

## 6. GLOSARIO

**CRUD:** Las cuatro operaciones basicas de datos: Crear, Leer, Actualizar y Eliminar.

**Base de datos:** Archivo donde se almacena toda la informacion de clientes y eventos de forma organizada.

**SQLite:** El sistema de base de datos que usa la aplicacion. Guarda todo en un solo archivo local sin necesidad de servidor.

**Interfaz grafica:** La ventana con botones y campos que el usuario ve y usa para interactuar con el sistema.

**Codigo interno:** El identificador unico de cada cliente, puede ser su RFC, numero de cliente u otro codigo que use la empresa.

**Estatus:** El estado en que se encuentra un evento: Cotizado, Confirmado, Realizado o Cancelado.

**JOIN:** Consulta que combina informacion de dos tablas. En este sistema muestra los eventos junto con los datos del cliente al que pertenecen.

**GROUP BY:** Consulta que agrupa registros. En este sistema muestra cuantos eventos tiene cada cliente.

**Respaldo (Backup):** Copia de seguridad de la base de datos guardada en un archivo aparte.

**Restaurar (Restore):** Recuperar los datos de un respaldo previo.

**Hash SHA-256:** Funcion de seguridad que convierte la contrasena en un codigo cifrado antes de guardarla. La contrasena real nunca se almacena en texto visible.

**Ejecutable (.exe):** El archivo que permite abrir la aplicacion sin necesidad de instalar Python.

**Tkinter:** La herramienta de Python que se uso para crear la ventana y los botones de la aplicacion.

**Campo:** Cada espacio del formulario donde se escribe informacion.

**Pestana:** Cada seccion de la aplicacion (Clientes, Eventos, JOIN, GROUP BY).

**Filtrar:** Mostrar solo los registros que coinciden con lo que se busca.

---

**Fin del Manual de Usuario**

Version: 1.0 | Fecha: Marzo 2026 | Desarrollador: Alexandro Reynoso
