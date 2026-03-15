# DIAGRAMAS DEL SISTEMA — GalaPro
**Sistema de Gestión de Clientes y Eventos**
Desarrollador: Alexandro Reynoso | Versión 1.0 | 2026

---

## 1. DIAGRAMA ENTIDAD-RELACIÓN (ER)

```
┌─────────────────────────┐               ┌──────────────────────────────┐
│        CLIENTES         │               │           EVENTOS            │
├─────────────────────────┤               ├──────────────────────────────┤
│ PK  id   INTEGER        │               │ PK  id          INTEGER      │
│     codigo   TEXT UNIQUE│  1 ────────N  │ FK  cliente_id  INTEGER      │
│     nombre   TEXT       │               │     nombre_tipo TEXT         │
│     telefono TEXT       │               │     descripcion TEXT         │
│     fecha_registro TEXT │               │     estatus     TEXT         │
└─────────────────────────┘               │     fecha_evento TEXT        │
                                          └──────────────────────────────┘

┌─────────────────────────┐
│        USUARIOS         │
├─────────────────────────┤
│ PK  id            INTEGER│
│     usuario  TEXT UNIQUE │   (independiente — control de acceso)
│     password_hash TEXT   │
└─────────────────────────┘
```

### Reglas de la base de datos
| Regla | Detalle |
|---|---|
| `clientes.codigo` es UNIQUE | No se permiten dos clientes con el mismo código |
| `eventos.cliente_id` es FK | Todo evento debe pertenecer a un cliente existente |
| ON DELETE CASCADE | Al eliminar un cliente se eliminan todos sus eventos |
| Contraseñas | Almacenadas como hash SHA-256, nunca en texto plano |

---

## 2. DIAGRAMA DE CLASES

```
         models.py
┌──────────────────────────┐     ┌──────────────────────────────┐
│       Cliente            │     │           Evento             │
├──────────────────────────┤     ├──────────────────────────────┤
│ + id            : int    │     │ + id            : int        │
│ + codigo        : str    │     │ + nombre_tipo   : str        │
│ + nombre        : str    │     │ + descripcion   : str        │
│ + telefono      : str    │     │ + estatus       : str        │
│ + fecha_registro: str    │     │ + fecha_evento  : str        │
└──────────────────────────┘     │ + cliente_id    : int        │
                                 │ + cliente_nombre: str        │
                                 └──────────────────────────────┘

         db.py                              crud.py
┌──────────────────────────┐     ┌──────────────────────────────┐
│       Database           │     │           CRUD               │
├──────────────────────────┤     ├──────────────────────────────┤
│ DB_FILE : str            │     │ + verificar_usuario()        │
├──────────────────────────┤     │ ─────────────────────────    │
│ + conectar()             │     │ + get_clientes()             │
│ + crear_tablas()         │     │ + buscar_clientes()          │
└──────────────────────────┘     │ + crear_cliente()            │
            ▲                    │ + actualizar_cliente()       │
            │ usa                │ + eliminar_cliente()         │
            │                    │ ─────────────────────────    │
┌──────────────────────────┐     │ + get_eventos()              │
│       main.py            │     │ + buscar_eventos()           │
├──────────────────────────┤     │ + get_evento_por_id()        │
│ LoginWindow              │     │ + crear_evento()             │
│ GalaProApp               │     │ + actualizar_evento()        │
│  - _tab_clientes()       │◄────│ + actualizar_estatus_evento()│
│  - _tab_eventos()        │     │ + eliminar_evento()          │
│  - _tab_join()           │     │ ─────────────────────────    │
│  - _tab_groupby()        │     │ + reporte_join()             │
│  - _respaldar()          │     │ + reporte_groupby()          │
│  - _restaurar()          │     └──────────────────────────────┘
└──────────────────────────┘
```

---

## 3. ARQUITECTURA DEL SISTEMA (CAPAS)

```
┌─────────────────────────────────────────────────────┐
│               CAPA DE PRESENTACIÓN                  │
│                    main.py                          │
│   LoginWindow │ Clientes │ Eventos │ JOIN │ GROUP BY│
└─────────────────────────┬───────────────────────────┘
                          │ llama a
┌─────────────────────────▼───────────────────────────┐
│                 CAPA DE LÓGICA                       │
│                    crud.py                          │
│     Validaciones │ Consultas │ Reportes │ Auth       │
└─────────────────────────┬───────────────────────────┘
                          │ usa
┌─────────────────────────▼───────────────────────────┐
│                 CAPA DE DATOS                        │
│                db.py + galapro.db                   │
│         SQLite │ Tablas │ Relaciones │ FK            │
└─────────────────────────────────────────────────────┘
```
