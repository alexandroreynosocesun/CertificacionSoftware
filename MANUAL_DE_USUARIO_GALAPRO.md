# MANUAL DE USUARIO — GalaPro

**Sistema de Gestion de Clientes y Eventos**
Desarrollador: Alexandro Reynoso | Version 1.0 | Marzo 2026

---

## 1. Introduccion

GalaPro es una aplicacion de escritorio para registrar y consultar clientes y eventos de una agencia. No requiere internet ni instalacion adicional.

---

## 2. Requisitos

- Windows 7, 8, 10 u 11
- 512 MB de RAM minimo
- 50 MB de espacio libre

---

## 3. Instalacion

1. Copia `GalaPro_Sistema.exe` a la carpeta que prefieras.
2. Haz doble clic para abrirlo. Se creara `galapro.db` automaticamente.
3. Si Windows muestra un aviso de seguridad, haz clic en **"Mas informacion" → "Ejecutar de todas formas"**.

---

## 4. Inicio de sesion

Credenciales por defecto:
- **Usuario:** admin
- **Contrasena:** admin123

Escribe los datos y presiona **"Ingresar"** o **Enter**.

---

## 5. Pantalla principal

La ventana tiene cuatro pestanas:

| Pestana | Funcion |
|---------|---------|
| Clientes | Registrar y gestionar clientes |
| Eventos | Registrar y gestionar eventos |
| Eventos por Cliente | Reporte combinado (JOIN) |
| Total por Cliente | Conteo de eventos por cliente (GROUP BY) |

En la barra superior estan los botones **Respaldar BD** y **Restaurar BD**.

---

## 6. Modulo de Clientes

### Registrar
1. Ve a la pestana **Clientes**.
2. Llena los campos: Codigo Interno, Nombre, Telefono, Fecha (DD/MM/AAAA).
3. Clic en **Agregar**.

> El Codigo Interno debe ser unico (puede ser RFC u otro identificador).

### Consultar
Los clientes registrados aparecen en la tabla inferior automaticamente.

### Actualizar
1. Haz clic en el cliente en la tabla (se cargan sus datos).
2. Modifica lo necesario y haz clic en **Actualizar**.

### Eliminar
1. Haz clic en el cliente en la tabla.
2. Clic en **Eliminar** y confirma.

> Al eliminar un cliente se eliminan tambien todos sus eventos.

### Buscar
Escribe en el campo **Buscar** y la tabla se filtra automaticamente.

---

## 7. Modulo de Eventos

### Registrar
1. Ve a la pestana **Eventos**.
2. Selecciona el cliente del menu desplegable.
3. Llena: Tipo de Evento, Estatus, Fecha (DD/MM/AAAA), Descripcion.
4. Clic en **Agregar**.

### Estatus disponibles

| Estatus | Significado |
|---------|-------------|
| Cotizado | Se entrego cotizacion al cliente |
| Confirmado | El cliente acepto el evento |
| Realizado | El evento ya se llevo a cabo |
| Cancelado | El evento fue cancelado |

Para cambiar el estatus: selecciona el evento en la tabla, cambia el campo Estatus y haz clic en **Cambiar Estatus**.

### Actualizar / Eliminar
Igual que en Clientes: selecciona el evento en la tabla y usa el boton correspondiente.

---

## 8. Reportes

### Eventos por Cliente (JOIN)
Muestra todos los eventos con los datos del cliente. Usa **Actualizar** para refrescar.

### Total de Eventos por Cliente (GROUP BY)
Muestra cuantos eventos tiene cada cliente, de mayor a menor. Usa **Actualizar** para refrescar.

---

## 9. Respaldo y Restauracion

### Respaldar
Clic en **Respaldar BD**. Se guarda automaticamente en la carpeta `backup\` con la fecha y hora en el nombre.

### Restaurar
Clic en **Restaurar BD**, selecciona el archivo de respaldo y confirma.

> Al restaurar, los datos actuales son reemplazados por los del respaldo.

---

## 10. Mensajes comunes

| Mensaje | Que significa |
|---------|---------------|
| "Cliente registrado correctamente" | Alta exitosa |
| "El codigo [X] ya existe" | Usa un codigo diferente |
| "Fecha invalida. Use DD/MM/AAAA" | Corrige el formato de fecha |
| "Selecciona un cliente/evento primero" | Haz clic en la tabla antes de operar |
| "Acceso denegado" | Usuario o contrasena incorrectos |

### Problemas frecuentes

**La app no abre:** Verifica que sea Windows 7 o superior. Acepta el aviso de seguridad si aparece.

**El menu de clientes en Eventos aparece vacio:** Registra al menos un cliente primero, luego cambia de pestana y regresa.

**Base de datos bloqueada:** Asegurate de tener solo una instancia del programa abierta.

---

## 11. Glosario

- **CRUD:** Crear, Leer, Actualizar, Eliminar.
- **Codigo interno:** Identificador unico del cliente (RFC u otro).
- **JOIN:** Consulta que combina datos de dos tablas.
- **GROUP BY:** Consulta que agrupa y cuenta registros.
- **Respaldo:** Copia de seguridad de la base de datos.
- **SQLite:** Base de datos local en un solo archivo, sin servidor.

---

*Version 1.0 | Marzo 2026 | Alexandro Reynoso*
