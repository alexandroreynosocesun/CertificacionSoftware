import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
import re
import os
import shutil
from datetime import datetime

from db import crear_tablas, DB_FILE
from models import ESTATUSES
from crud import (
    verificar_usuario,
    get_clientes, buscar_clientes, crear_cliente, actualizar_cliente, eliminar_cliente,
    get_eventos, buscar_eventos, get_evento_por_id,
    crear_evento, actualizar_evento, actualizar_estatus_evento, eliminar_evento,
    reporte_join, reporte_groupby,
)

BACKUP_DIR = os.path.join(os.path.expanduser("~"), "Documents", "backup app")

COLOR_TOP   = "#2c3e50"
COLOR_VERDE = "#27ae60"
COLOR_AZUL  = "#2980b9"
COLOR_NARAN = "#e67e22"
COLOR_AMARI = "#f39c12"
COLOR_ROJO  = "#e74c3c"
COLOR_MORA  = "#8e44ad"
COLOR_GRIS  = "#95a5a6"


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────────────────────────────────────

def validar_fecha(fecha):
    """Verifica formato DD/MM/AAAA y que sea una fecha real."""
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha):
        return False
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def btn(parent, texto, cmd, color, ancho=14, **kw):
    return tk.Button(parent, text=texto, command=cmd,
                     bg=color, fg="white", width=ancho,
                     font=("Arial", 9, "bold"), relief=tk.FLAT,
                     activebackground=color, cursor="hand2", **kw)


# ─────────────────────────────────────────────────────────────────────────────
# Ventana de Login
# ─────────────────────────────────────────────────────────────────────────────

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("GalaPro - Acceso")
        self.root.geometry("380x270")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_TOP)
        self.autenticado = False
        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def _build(self):
        tk.Label(self.root, text="GALAPRO", font=("Arial", 26, "bold"),
                 bg=COLOR_TOP, fg="white").pack(pady=(25, 4))
        tk.Label(self.root, text="Sistema de Gestión de Clientes y Eventos",
                 font=("Arial", 9), bg=COLOR_TOP, fg="#bdc3c7").pack()

        frame = tk.Frame(self.root, bg=COLOR_TOP)
        frame.pack(pady=18)

        tk.Label(frame, text="Usuario:", bg=COLOR_TOP, fg="white",
                 font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.ent_user = ttk.Entry(frame, width=22, font=("Arial", 10))
        self.ent_user.grid(row=0, column=1, pady=6)
        self.ent_user.focus()

        tk.Label(frame, text="Contraseña:", bg=COLOR_TOP, fg="white",
                 font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.ent_pwd = ttk.Entry(frame, width=22, show="*", font=("Arial", 10))
        self.ent_pwd.grid(row=1, column=1, pady=6)
        self.ent_pwd.bind("<Return>", lambda e: self._login())

        tk.Label(self.root, text="Usuario por defecto: admin / admin123",
                 font=("Arial", 8), bg=COLOR_TOP, fg="#7f8c8d").pack()

        btn(self.root, "  Ingresar  ", self._login, COLOR_VERDE, ancho=16).pack(pady=10)

    def _login(self):
        usuario = self.ent_user.get().strip()
        password = self.ent_pwd.get()
        if not usuario or not password:
            messagebox.showwarning("Aviso", "Ingresa usuario y contraseña.", parent=self.root)
            return
        if verificar_usuario(usuario, password):
            self.autenticado = True
            self.root.destroy()
        else:
            messagebox.showerror("Acceso denegado",
                                 "Usuario o contraseña incorrectos.", parent=self.root)
            self.ent_pwd.delete(0, tk.END)


# ─────────────────────────────────────────────────────────────────────────────
# Aplicación principal
# ─────────────────────────────────────────────────────────────────────────────

class GalaProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GalaPro — Sistema de Gestión de Clientes y Eventos")
        self.root.geometry("1150x700")
        self.root.minsize(900, 600)
        self._build_ui()

    # ── Barra superior ────────────────────────────────────────────────────────

    def _build_ui(self):
        top = tk.Frame(self.root, bg=COLOR_TOP, height=52)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        tk.Label(top, text="GALAPRO  |  Clientes y Eventos",
                 font=("Arial", 15, "bold"), bg=COLOR_TOP, fg="white").pack(
                     side=tk.LEFT, padx=15, pady=13)

        btn(top, "Restaurar BD", self._restaurar, COLOR_NARAN, ancho=13).pack(
            side=tk.RIGHT, padx=6, pady=10)
        btn(top, "Respaldar BD", self._respaldar, COLOR_AZUL, ancho=13).pack(
            side=tk.RIGHT, padx=0, pady=10)

        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._tab_clientes(nb)
        self._tab_eventos(nb)
        self._tab_join(nb)
        self._tab_groupby(nb)

    # ── Helpers de tabla ──────────────────────────────────────────────────────

    def _make_treeview(self, parent, cols, widths, height=14):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        tv = ttk.Treeview(frame, columns=cols, show="headings", height=height)
        for col, w in zip(cols, widths):
            tv.heading(col, text=col)
            tv.column(col, width=w, minwidth=40)
        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscroll=sb.set)
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        return tv

    # ═════════════════════════════════════════════════════════════════════════
    # TAB CLIENTES
    # ═════════════════════════════════════════════════════════════════════════

    def _tab_clientes(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="  Clientes  ")

        # Formulario
        form = ttk.LabelFrame(f, text="Datos del Cliente", padding=8)
        form.pack(fill=tk.X, padx=8, pady=6)

        labels = ["Código Interno (RFC/No.):", "Nombre Completo:", "Teléfono:",
                  "Fecha de Registro (DD/MM/AAAA):"]
        keys   = ["codigo", "nombre", "telefono", "fecha_registro"]
        self._c = {}
        for col, (lbl, key) in enumerate(zip(labels, keys)):
            tk.Label(form, text=lbl, font=("Arial", 9)).grid(
                row=0, column=col*2, sticky="e", padx=6, pady=6)
            e = ttk.Entry(form, width=20)
            e.grid(row=0, column=col*2+1, padx=4, pady=6)
            self._c[key] = e

        # Botones
        bf = tk.Frame(f)
        bf.pack(pady=4)
        self._c_sel = None
        btn(bf, "Agregar",    self._agregar_cliente,    COLOR_VERDE).pack(side=tk.LEFT, padx=4)
        btn(bf, "Actualizar", self._actualizar_cliente, COLOR_AMARI).pack(side=tk.LEFT, padx=4)
        btn(bf, "Eliminar",   self._eliminar_cliente,   COLOR_ROJO ).pack(side=tk.LEFT, padx=4)
        btn(bf, "Limpiar",    self._limpiar_cliente,    COLOR_GRIS ).pack(side=tk.LEFT, padx=4)

        # Búsqueda
        sf = tk.Frame(f)
        sf.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(sf, text="Buscar:").pack(side=tk.LEFT)
        self._c_search = ttk.Entry(sf, width=35)
        self._c_search.pack(side=tk.LEFT, padx=5)
        self._c_search.bind("<KeyRelease>", lambda e: self._cargar_clientes())

        # Tabla
        cols   = ("ID", "Código", "Nombre", "Teléfono", "Fecha de Registro")
        widths = [40, 130, 220, 130, 140]
        self._c_tv = self._make_treeview(f, cols, widths)
        self._c_tv.bind("<<TreeviewSelect>>", self._sel_cliente)

        self._cargar_clientes()

    def _cargar_clientes(self):
        for i in self._c_tv.get_children():
            self._c_tv.delete(i)
        termino = self._c_search.get().strip()
        lista = buscar_clientes(termino) if termino else get_clientes()
        for c in lista:
            self._c_tv.insert("", tk.END,
                              values=(c.id, c.codigo, c.nombre, c.telefono, c.fecha_registro))

    def _sel_cliente(self, _event):
        sel = self._c_tv.selection()
        if not sel:
            return
        v = self._c_tv.item(sel[0], "values")
        self._c_sel = v[0]
        for key, val in zip(["codigo", "nombre", "telefono", "fecha_registro"], v[1:]):
            self._c[key].delete(0, tk.END)
            self._c[key].insert(0, val)

    def _validar_cliente(self):
        d = {k: e.get().strip() for k, e in self._c.items()}
        if not d["codigo"]:
            messagebox.showwarning("Validación", "El código interno es obligatorio.")
            return None
        if not d["nombre"]:
            messagebox.showwarning("Validación", "El nombre del cliente es obligatorio.")
            return None
        if not validar_fecha(d["fecha_registro"]):
            messagebox.showwarning("Validación",
                                   "Fecha de registro inválida.\nUse el formato DD/MM/AAAA.")
            return None
        return d

    def _agregar_cliente(self):
        d = self._validar_cliente()
        if not d:
            return
        try:
            crear_cliente(**d)
            messagebox.showinfo("OK", "Cliente registrado correctamente.")
            self._limpiar_cliente()
            self._cargar_clientes()
        except Exception as ex:
            if "UNIQUE" in str(ex):
                messagebox.showerror("Error", f"El código '{d['codigo']}' ya existe.")
            else:
                messagebox.showerror("Error", str(ex))

    def _actualizar_cliente(self):
        if not self._c_sel:
            messagebox.showwarning("Aviso", "Selecciona un cliente de la tabla primero.")
            return
        d = self._validar_cliente()
        if not d:
            return
        try:
            actualizar_cliente(self._c_sel, **d)
            messagebox.showinfo("OK", "Cliente actualizado.")
            self._limpiar_cliente()
            self._cargar_clientes()
        except Exception as ex:
            if "UNIQUE" in str(ex):
                messagebox.showerror("Error", f"El código '{d['codigo']}' ya existe.")
            else:
                messagebox.showerror("Error", str(ex))

    def _eliminar_cliente(self):
        if not self._c_sel:
            messagebox.showwarning("Aviso", "Selecciona un cliente de la tabla primero.")
            return
        nombre = self._c["nombre"].get()
        if messagebox.askyesno("Confirmar",
                               f"¿Eliminar al cliente '{nombre}' y TODOS sus eventos asociados?"):
            eliminar_cliente(self._c_sel)
            messagebox.showinfo("OK", "Cliente eliminado.")
            self._limpiar_cliente()
            self._cargar_clientes()

    def _limpiar_cliente(self):
        for e in self._c.values():
            e.delete(0, tk.END)
        self._c_sel = None

    # ═════════════════════════════════════════════════════════════════════════
    # TAB EVENTOS
    # ═════════════════════════════════════════════════════════════════════════

    def _tab_eventos(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="  Eventos  ")

        form = ttk.LabelFrame(f, text="Datos del Evento", padding=8)
        form.pack(fill=tk.X, padx=8, pady=6)

        # Fila 0
        tk.Label(form, text="Cliente:").grid(row=0, column=0, sticky="e", padx=6, pady=5)
        self._e_cli_combo = ttk.Combobox(form, width=26, state="readonly")
        self._e_cli_combo.grid(row=0, column=1, padx=4, pady=5)

        tk.Label(form, text="Nombre / Tipo de Evento:").grid(row=0, column=2, sticky="e", padx=6)
        self._e_tipo = ttk.Entry(form, width=22)
        self._e_tipo.grid(row=0, column=3, padx=4, pady=5)

        tk.Label(form, text="Estatus:").grid(row=0, column=4, sticky="e", padx=6)
        self._e_estatus = ttk.Combobox(form, values=ESTATUSES, width=14, state="readonly")
        self._e_estatus.set("Cotizado")
        self._e_estatus.grid(row=0, column=5, padx=4, pady=5)

        # Fila 1
        tk.Label(form, text="Fecha del Evento (DD/MM/AAAA):").grid(
            row=1, column=0, sticky="e", padx=6, pady=5)
        self._e_fecha = ttk.Entry(form, width=18)
        self._e_fecha.grid(row=1, column=1, padx=4, pady=5, sticky="w")

        tk.Label(form, text="Descripción:").grid(row=1, column=2, sticky="e", padx=6)
        self._e_desc = ttk.Entry(form, width=48)
        self._e_desc.grid(row=1, column=3, columnspan=3, padx=4, pady=5, sticky="ew")

        # Botones
        bf = tk.Frame(f)
        bf.pack(pady=4)
        self._e_sel = None
        btn(bf, "Agregar",        self._agregar_evento,       COLOR_VERDE).pack(side=tk.LEFT, padx=3)
        btn(bf, "Actualizar",     self._actualizar_evento,    COLOR_AMARI).pack(side=tk.LEFT, padx=3)
        btn(bf, "Cambiar Estatus",self._cambiar_estatus,      COLOR_MORA, ancho=16).pack(side=tk.LEFT, padx=3)
        btn(bf, "Eliminar",       self._eliminar_evento,      COLOR_ROJO ).pack(side=tk.LEFT, padx=3)
        btn(bf, "Limpiar",        self._limpiar_evento,       COLOR_GRIS ).pack(side=tk.LEFT, padx=3)

        # Búsqueda
        sf = tk.Frame(f)
        sf.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(sf, text="Buscar:").pack(side=tk.LEFT)
        self._e_search = ttk.Entry(sf, width=35)
        self._e_search.pack(side=tk.LEFT, padx=5)
        self._e_search.bind("<KeyRelease>", lambda e: self._cargar_eventos())

        # Tabla
        cols   = ("ID", "Cliente", "Nombre/Tipo", "Descripción", "Estatus", "Fecha Evento")
        widths = [40, 160, 140, 260, 100, 120]
        self._e_tv = self._make_treeview(f, cols, widths, height=12)
        self._e_tv.bind("<<TreeviewSelect>>", self._sel_evento)

        self._actualizar_combo_clientes()
        self._cargar_eventos()

    def _actualizar_combo_clientes(self):
        clientes = get_clientes()
        self._cli_map = {f"{c.codigo}  —  {c.nombre}": c.id for c in clientes}
        self._e_cli_combo["values"] = list(self._cli_map.keys())

    def _cargar_eventos(self):
        for i in self._e_tv.get_children():
            self._e_tv.delete(i)
        termino = self._e_search.get().strip()
        lista = buscar_eventos(termino) if termino else get_eventos()
        for ev in lista:
            self._e_tv.insert("", tk.END,
                              values=(ev.id, ev.cliente_nombre, ev.nombre_tipo,
                                      ev.descripcion, ev.estatus, ev.fecha_evento))

    def _sel_evento(self, _event):
        sel = self._e_tv.selection()
        if not sel:
            return
        v = self._e_tv.item(sel[0], "values")
        self._e_sel = v[0]
        ev = get_evento_por_id(v[0])
        if not ev:
            return
        # Poner cliente en combo
        for k, cid in self._cli_map.items():
            if cid == ev.cliente_id:
                self._e_cli_combo.set(k)
                break
        self._e_tipo.delete(0, tk.END)
        self._e_tipo.insert(0, ev.nombre_tipo)
        self._e_desc.delete(0, tk.END)
        self._e_desc.insert(0, ev.descripcion)
        self._e_estatus.set(ev.estatus)
        self._e_fecha.delete(0, tk.END)
        self._e_fecha.insert(0, ev.fecha_evento)

    def _validar_evento(self):
        cli_key = self._e_cli_combo.get()
        tipo    = self._e_tipo.get().strip()
        fecha   = self._e_fecha.get().strip()
        if not cli_key:
            messagebox.showwarning("Validación", "Selecciona un cliente.")
            return None
        if not tipo:
            messagebox.showwarning("Validación", "El nombre/tipo del evento es obligatorio.")
            return None
        if not validar_fecha(fecha):
            messagebox.showwarning("Validación",
                                   "Fecha del evento inválida.\nUse el formato DD/MM/AAAA.")
            return None
        return {
            "nombre_tipo": tipo,
            "descripcion": self._e_desc.get().strip(),
            "estatus":     self._e_estatus.get(),
            "fecha_evento": fecha,
            "cliente_id":  self._cli_map[cli_key],
        }

    def _agregar_evento(self):
        d = self._validar_evento()
        if not d:
            return
        try:
            crear_evento(**d)
            messagebox.showinfo("OK", "Evento registrado correctamente.")
            self._limpiar_evento()
            self._cargar_eventos()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _actualizar_evento(self):
        if not self._e_sel:
            messagebox.showwarning("Aviso", "Selecciona un evento de la tabla primero.")
            return
        d = self._validar_evento()
        if not d:
            return
        try:
            actualizar_evento(self._e_sel, **d)
            messagebox.showinfo("OK", "Evento actualizado.")
            self._limpiar_evento()
            self._cargar_eventos()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _cambiar_estatus(self):
        if not self._e_sel:
            messagebox.showwarning("Aviso", "Selecciona un evento de la tabla primero.")
            return
        nuevo = self._e_estatus.get()
        if not nuevo:
            messagebox.showwarning("Aviso", "Selecciona el nuevo estatus en el campo Estatus.")
            return
        actualizar_estatus_evento(self._e_sel, nuevo)
        messagebox.showinfo("OK", f"Estatus actualizado a: {nuevo}")
        self._cargar_eventos()

    def _eliminar_evento(self):
        if not self._e_sel:
            messagebox.showwarning("Aviso", "Selecciona un evento de la tabla primero.")
            return
        tipo = self._e_tipo.get()
        if messagebox.askyesno("Confirmar", f"¿Eliminar el evento '{tipo}'?"):
            eliminar_evento(self._e_sel)
            messagebox.showinfo("OK", "Evento eliminado.")
            self._limpiar_evento()
            self._cargar_eventos()

    def _limpiar_evento(self):
        self._e_cli_combo.set("")
        self._e_tipo.delete(0, tk.END)
        self._e_desc.delete(0, tk.END)
        self._e_estatus.set("Cotizado")
        self._e_fecha.delete(0, tk.END)
        self._e_sel = None

    # ═════════════════════════════════════════════════════════════════════════
    # TAB JOIN
    # ═════════════════════════════════════════════════════════════════════════

    def _tab_join(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="  Eventos por Cliente (JOIN)  ")

        hf = tk.Frame(f)
        hf.pack(fill=tk.X, padx=8, pady=8)
        tk.Label(hf, text="Detalle de cada Evento con información del Cliente asociado",
                 font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        btn(hf, "Actualizar", self._cargar_join, COLOR_AZUL, ancho=12).pack(side=tk.RIGHT)

        cols   = ("ID Evento", "Código Cliente", "Nombre Cliente",
                  "Tipo de Evento", "Descripción", "Estatus", "Fecha Evento")
        widths = [75, 120, 190, 130, 230, 100, 110]
        self._join_tv = self._make_treeview(f, cols, widths, height=20)
        self._cargar_join()

    def _cargar_join(self):
        for i in self._join_tv.get_children():
            self._join_tv.delete(i)
        for row in reporte_join():
            self._join_tv.insert("", tk.END, values=row)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB GROUP BY
    # ═════════════════════════════════════════════════════════════════════════

    def _tab_groupby(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="  Total de Eventos por Cliente (GROUP BY)  ")

        hf = tk.Frame(f)
        hf.pack(fill=tk.X, padx=8, pady=8)
        tk.Label(hf, text="Cantidad total de Eventos registrados por cada Cliente",
                 font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        btn(hf, "Actualizar", self._cargar_groupby, COLOR_AZUL, ancho=12).pack(side=tk.RIGHT)

        cols   = ("Código Cliente", "Nombre Cliente", "Total de Eventos")
        widths = [160, 380, 160]
        self._gb_tv = self._make_treeview(f, cols, widths, height=20)
        self._cargar_groupby()

    def _cargar_groupby(self):
        for i in self._gb_tv.get_children():
            self._gb_tv.delete(i)
        for row in reporte_groupby():
            self._gb_tv.insert("", tk.END, values=row)

    # ═════════════════════════════════════════════════════════════════════════
    # BACKUP / RESTORE
    # ═════════════════════════════════════════════════════════════════════════

    def _respaldar(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(BACKUP_DIR, f"galapro_backup_{ts}.db")
        try:
            shutil.copy2(DB_FILE, dest)
            messagebox.showinfo("Respaldo creado",
                                f"Respaldo guardado exitosamente en:\n{dest}")
        except Exception as ex:
            messagebox.showerror("Error al respaldar", str(ex))

    def _restaurar(self):
        # Abrir explorador ya posicionado en la carpeta de backups
        inicio = BACKUP_DIR if os.path.exists(BACKUP_DIR) else os.path.expanduser("~")
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de respaldo",
            initialdir=inicio,
            filetypes=[("Base de datos GalaPro", "*.db"), ("Todos los archivos", "*.*")]
        )
        if not archivo:
            return
        if messagebox.askyesno(
            "Confirmar restauración",
            f"¿Restaurar la base de datos desde:\n\n{os.path.basename(archivo)}\n\n"
            "Esto REEMPLAZARÁ todos los datos actuales."
        ):
            try:
                shutil.copy2(archivo, DB_FILE)
                messagebox.showinfo(
                    "Restauración exitosa",
                    "La base de datos fue restaurada correctamente.\n"
                    "Reinicia la aplicación para ver los datos actualizados."
                )
            except Exception as ex:
                messagebox.showerror("Error al restaurar", str(ex))


# ─────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────────────────────

def main():
    crear_tablas()

    # Pantalla de login
    root_login = tk.Tk()
    login = LoginWindow(root_login)
    root_login.mainloop()

    if not login.autenticado:
        return

    # Aplicación principal
    root = tk.Tk()
    GalaProApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
