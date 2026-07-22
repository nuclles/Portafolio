import tkinter as tk
from tkinter import ttk
import datetime
import os
from tkinter import messagebox
from typing import Any, Dict, List, Tuple, Optional
import config
from logger import get_logger

logger = get_logger(__name__)


def centrar_ventana(toplevel: tk.Toplevel, ancho: int, alto: int) -> None:
    """Centra dinámicamente una ventana Toplevel en la pantalla del usuario.

    Calcula las coordenadas x e y necesarias para posicionar la ventana
    en el centro exacto de la pantalla, basándose en la resolución actual
    del monitor.

    Args:
        toplevel: Instancia de tk.Toplevel a centrar.
        ancho: Ancho deseado de la ventana en píxeles.
        alto: Alto deseado de la ventana en píxeles.
    """
    pantalla_ancho = toplevel.winfo_screenwidth()
    pantalla_alto = toplevel.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    toplevel.geometry(f"{ancho}x{alto}+{x}+{y}")


class PaginaLogin(tk.Frame):
    def __init__(self, parent: tk.Widget, controlador: Any) -> None:
        super().__init__(parent, bg="white")
        self.controlador = controlador
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # --- Logo Longvie: centrado arriba, tamaño grande (subsample 2) ---
        try:
            ruta_longvie = os.path.join(base_dir, "longvie.png")
            self._img_longvie = tk.PhotoImage(file=ruta_longvie).subsample(2, 2)
            tk.Label(self, image=self._img_longvie, bg="white").pack(side="top", pady=(40, 20))
        except Exception:
            logger.warning("No se pudo cargar el logo 'longvie.png'. Verifique que el archivo exista en %s.", base_dir)
        
        # --- Frame central de login (tema oscuro original conservado) ---
        frame_login = tk.Frame(self, bg="#34495e", padx=40, pady=40, bd=2, relief="groove")
        frame_login.pack(expand=True)
        
        # Registrar comandos de validación para los campos de login
        vcmd_user = (self.register(self.validar_usuario), '%P')
        vcmd_pass = (self.register(self.validar_password), '%P')
        
        tk.Label(frame_login, text="Inicie Sesión", font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(pady=(0, 20))
        tk.Label(frame_login, text="Usuario", font=("Arial", 12), bg="#34495e", fg="white", anchor="w").pack(fill="x")
        self.entry_user = tk.Entry(frame_login, font=("Arial", 12),
                                   validate="key", validatecommand=vcmd_user)
        self.entry_user.pack(fill="x", pady=(0, 15))
        self.entry_user.bind("<Return>", lambda e: self.intentar_login())
        
        tk.Label(frame_login, text="Contraseña", font=("Arial", 12), bg="#34495e", fg="white", anchor="w").pack(fill="x")
        self.entry_pass = tk.Entry(frame_login, font=("Arial", 12), show="*",
                                   validate="key", validatecommand=vcmd_pass)
        self.entry_pass.pack(fill="x", pady=(0, 20))
        self.entry_pass.bind("<Return>", lambda e: self.intentar_login())
        tk.Button(frame_login, text="Ingresar", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=self.intentar_login).pack(fill="x", pady=(0, 10))
        tk.Button(frame_login, text="Crear usuario", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=lambda: self.controlador.root.mostrar_frame(PaginaRegistroUsuario)).pack(fill="x")

        # --- Enlace discreto de recuperación de credenciales ---
        tk.Button(
            frame_login, text="¿Olvidó su usuario/contraseña?",
            bg="#34495e", fg="#f1c40f", activeforeground="#f39c12",
            activebackground="#34495e", font=("Arial", 9, "underline"),
            relief="flat", bd=0, cursor="hand2",
            command=self.abrir_modal_recuperacion
        ).pack(pady=(15, 0))
        
        # --- Logo MT: esquina inferior derecha, posicionado con .place() ---
        try:
            ruta_mt = os.path.join(base_dir, "mt.png")
            self._img_mt = tk.PhotoImage(file=ruta_mt).subsample(4, 4)
            tk.Label(self, image=self._img_mt, bg="white").place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
        except Exception:
            logger.warning("No se pudo cargar el logo 'mt.png'. Verifique que el archivo exista en %s.", base_dir)

        # --- Botón "Leer Manual de Usuario" en la esquina inferior izquierda ---
        tk.Button(
            self, text="Leer Manual de Usuario",
            font=("Arial", 9), fg="#2980b9", bg="white",
            bd=0, cursor="hand2", relief="flat",
            command=lambda: self.controlador.root.mostrar_frame(PaginaManual)
        ).place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

    def validar_usuario(self, P: str) -> bool:
        """Valida que el usuario contenga solo caracteres alfanuméricos, máximo 20.

        Permite cadena vacía (campo borrado). Rechaza espacios, signos
        de puntuación y cualquier carácter especial.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor cumple las restricciones, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 20 and P.isalnum()

    def validar_password(self, P: str) -> bool:
        """Valida que la contraseña contenga solo caracteres alfanuméricos, máximo 20.

        Permite cadena vacía (campo borrado). Rechaza caracteres especiales
        como signos de puntuación, símbolos y espacios.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si todos los caracteres son alfanuméricos, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 20 and P.isalnum()

    def intentar_login(self) -> None:
        """Intenta autenticar al usuario con las credenciales ingresadas."""
        if not self.controlador.verificar_credenciales(self.entry_user.get(), self.entry_pass.get()):
            messagebox.showerror("Error", "Credenciales incorrectas.\n\nSi olvidó su usuario o contraseña contacte con el administrador del sistema.")

    def validar_nombre_completo(self, P: str) -> bool:
        """Valida que el nombre contenga solo letras y espacios, máximo 30 caracteres.

        Permite cadena vacía (campo borrado). Rechaza números, signos de
        puntuación y cualquier carácter especial. Los espacios son permitidos
        para nombres compuestos (ej. 'Juan Carlos López').

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor cumple las restricciones, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 30 and all(c.isalpha() or c == " " for c in P)

    def validar_alfanumerico_30(self, P: str) -> bool:
        """Valida que el texto contenga solo caracteres alfanuméricos, máximo 30.

        Permite cadena vacía (campo borrado). Rechaza espacios, signos de
        puntuación y cualquier carácter especial. Diseñado para los campos
        de contraseña y clave maestra del modal de recuperación.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si todos los caracteres son alfanuméricos, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 30 and P.isalnum()

    def abrir_modal_recuperacion(self) -> None:
        """
        Abre una ventana modal para la recuperación/blanqueo de credenciales.

        Presenta un formulario con tres campos: Nombre Completo, Nueva Contraseña
        y Clave Maestra de Autorización. Al confirmar, delega la lógica de
        validación y actualización al método ``controlador.blanquear_credenciales``.

        La ventana es modal (grab_set + transient) para bloquear la interacción
        con la ventana principal hasta que se cierre.
        """
        modal = tk.Toplevel(self)
        modal.title("Recuperación de Credenciales")
        modal.configure(bg="#2c3e50")
        modal.resizable(False, False)
        centrar_ventana(modal, 350, 350)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        # --- Registrar comandos de validación para los campos del modal ---
        vcmd_nombre = (self.register(self.validar_nombre_completo), '%P')
        vcmd_alnum30 = (self.register(self.validar_alfanumerico_30), '%P')

        # --- Título del modal ---
        tk.Label(
            modal, text="Recuperar Usuario / Contraseña",
            font=("Arial", 13, "bold"), bg="#2c3e50", fg="white"
        ).pack(pady=(20, 15))

        # --- Campo: Nombre Completo (letras y espacios, máx 30) ---
        tk.Label(
            modal, text="Su Nombre Completo",
            font=("Arial", 10), bg="#2c3e50", fg="white", anchor="w"
        ).pack(fill="x", padx=30)
        entry_nombre = tk.Entry(
            modal, font=("Arial", 11),
            validate="key", validatecommand=vcmd_nombre
        )
        entry_nombre.pack(fill="x", padx=30, pady=(0, 10))

        # --- Campo: Nueva Contraseña (alfanumérico, máx 30) ---
        tk.Label(
            modal, text="Nueva Contraseña",
            font=("Arial", 10), bg="#2c3e50", fg="white", anchor="w"
        ).pack(fill="x", padx=30)
        entry_nueva_pwd = tk.Entry(
            modal, font=("Arial", 11), show="*",
            validate="key", validatecommand=vcmd_alnum30
        )
        entry_nueva_pwd.pack(fill="x", padx=30, pady=(0, 10))

        # --- Campo: Clave Maestra (alfanumérico, máx 30, resaltado visual) ---
        tk.Label(
            modal, text="Clave Maestra de Autorización",
            font=("Arial", 10, "bold"), bg="#2c3e50", fg="#f1c40f", anchor="w"
        ).pack(fill="x", padx=30)
        entry_clave_maestra = tk.Entry(
            modal, font=("Arial", 11), show="*", bg="#ffeaa7",
            validate="key", validatecommand=vcmd_alnum30
        )
        entry_clave_maestra.pack(fill="x", padx=30, pady=(0, 20))

        def ejecutar_blanqueo() -> None:
            """Extrae los campos del formulario y delega al controlador."""
            nombre: str = entry_nombre.get().strip()
            nueva_pwd: str = entry_nueva_pwd.get().strip()
            clave: str = entry_clave_maestra.get().strip()

            if not nombre or not nueva_pwd or not clave:
                messagebox.showwarning(
                    "Campos Incompletos",
                    "Debe completar todos los campos para continuar.",
                    parent=modal
                )
                return

            exito: bool = self.controlador.blanquear_credenciales(
                nombre, clave, nueva_pwd
            )
            if exito:
                modal.destroy()

        # --- Botón de acción ---
        tk.Button(
            modal, text="Restablecer Credenciales",
            font=("Arial", 10, "bold"), bg="#27ae60", fg="white",
            activebackground="#2ecc71", relief="groove", bd=2, cursor="hand2",
            command=ejecutar_blanqueo
        ).pack(fill="x", padx=30, pady=(0, 10))

        # --- Botón cancelar ---
        tk.Button(
            modal, text="Cancelar",
            font=("Arial", 9), bg="#7f8c8d", fg="white",
            relief="flat", bd=0, cursor="hand2",
            command=modal.destroy
        ).pack(pady=(0, 15))

class PaginaTareas(tk.Frame):
    def __init__(self, parent: tk.Widget, controlador: Any) -> None:
        super().__init__(parent, bg="#ecf0f1")
        self.controlador = controlador
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_inicio = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_inicio, text="Inicio")

        # --- Header: saludo a la izquierda, botón Buscar a la derecha ---
        header_inicio = tk.Frame(self.tab_inicio, bg="white", bd=1, relief="groove")
        header_inicio.pack(side="top", fill="x", padx=10, pady=(10, 5))

        self.lbl_bienvenida = tk.Label(
            header_inicio, text="Bienvenido",
            font=("Arial", 20, "bold"), bg="white", fg="#2c3e50"
        )
        self.lbl_bienvenida.pack(side="left", padx=15, pady=10)

        btn_buscar = tk.Button(
            header_inicio, text="Buscar",
            font=("Arial", 10, "bold"), relief="groove", bd=2,
            bg="#34495e", fg="white", cursor="hand2",
            command=lambda: self.controlador.root.mostrar_frame(PaginaBuscadorHistorico)
        )
        btn_buscar.pack(side="right", padx=15, pady=10)

        # --- Subtítulo ---
        tk.Label(
            self.tab_inicio, text="Últimos trabajos consultados",
            font=("Arial", 11, "bold"), bg="white", fg="#34495e", anchor="w"
        ).pack(side="top", fill="x", padx=15, pady=(5, 2))

        # --- Treeview de trabajos recientes ---
        frame_tree_recientes = tk.Frame(self.tab_inicio, bg="white")
        frame_tree_recientes.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

        cols_recientes = ("ID", "Fecha", "Artículo", "Operación")
        self.tree_recientes = ttk.Treeview(
            frame_tree_recientes, columns=cols_recientes, show="headings", height=10
        )
        for col in cols_recientes:
            self.tree_recientes.heading(col, text=col)
        self.tree_recientes.column("ID", width=60, anchor="center")
        self.tree_recientes.column("Fecha", width=100, anchor="center")
        self.tree_recientes.column("Artículo", width=250, anchor="center")
        self.tree_recientes.column("Operación", width=250, anchor="w")
        self.tree_recientes["displaycolumns"] = ("Fecha", "Artículo", "Operación")

        scroll_recientes = ttk.Scrollbar(
            frame_tree_recientes, orient="vertical",
            command=self.tree_recientes.yview
        )
        self.tree_recientes.configure(yscrollcommand=scroll_recientes.set)
        self.tree_recientes.pack(side="left", fill="both", expand=True)
        scroll_recientes.pack(side="right", fill="y")

        self.tree_recientes.bind("<Double-1>", self.on_double_click_recientes)
        
        self.tab_tareas = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_tareas, text="Tareas")
        
        self.construir_ui_tareas()
        # El bind de <Visibility> se eliminó porque tkraise() no lo dispara fiablemente.
        # En su lugar, main.py llama explícitamente a actualizar_vista()
        
    def actualizar_vista(self) -> None:
        usuario = self.controlador.usuario_actual
        if usuario:
            self.lbl_bienvenida.config(text=f"Bienvenido {usuario.nombre}")
            self.aplicar_tema(usuario.rol)
        self.configurar_rbac()
        self.cargar_datos()
        self._poblar_recientes()

    def aplicar_tema(self, rol: str) -> None:
        """Aplica tematización dinámica de colores según el rol del usuario.

        Define un esquema oscuro para JEFE/GERENTE (#2c3e50 con texto blanco)
        y un esquema claro para METODISTA (#ecf0f1 con texto oscuro). Recorre
        recursivamente todos los widgets hijos usando winfo_children() y aplica
        los colores solo a tk.Frame y tk.Label, ignorando explícitamente
        tk.Button, tk.Entry y todos los widgets ttk para preservar su estilo.

        Args:
            rol: Rol del usuario actual ('JEFE/GERENTE' o 'METODISTA').
        """
        if rol == "JEFE/GERENTE":
            bg_color = "#2c3e50"
            fg_color = "white"
        else:
            bg_color = "#ecf0f1"
            fg_color = "#2c3e50"

        def _aplicar_recursivo(widget: tk.Widget) -> None:
            """Recorre recursivamente los hijos del widget y aplica colores.

            Ignora tk.Button, tk.Entry y cualquier widget de la librería ttk
            para no arruinar botones, campos de texto ni componentes temáticos.

            Args:
                widget: Widget raíz desde el cual iniciar el recorrido.
            """
            for hijo in widget.winfo_children():
                if isinstance(hijo, (tk.Button, tk.Entry)):
                    _aplicar_recursivo(hijo)
                    continue
                if isinstance(hijo, ttk.Widget):
                    _aplicar_recursivo(hijo)
                    continue
                try:
                    hijo.configure(bg=bg_color)
                    if isinstance(hijo, tk.Label):
                        hijo.configure(fg=fg_color)
                except tk.TclError:
                    pass
                _aplicar_recursivo(hijo)

        _aplicar_recursivo(self)

    def _poblar_recientes(self) -> None:
        """Limpia y puebla el Treeview de últimos trabajos consultados.

        Obtiene el resumen completo de relevamientos desde el controlador
        y muestra solo los 10 más recientes (ya vienen ordenados DESC desde el DAO).
        """
        for item in self.tree_recientes.get_children():
            self.tree_recientes.delete(item)
        try:
            resumen = self.controlador.obtener_resumen_relevamientos()
            for fila in resumen[:5]:
                # fila = (ID, Fecha, Artículo_codigo, Operación, Operario)
                self.tree_recientes.insert(
                    "", "end", iid=str(fila[0]),
                    values=(fila[0], fila[1], fila[2], fila[3])
                )
        except Exception:
            logger.exception("Error al poblar la tabla de trabajos recientes.")

    def construir_ui_tareas(self) -> None:
        self.tab_tareas.columnconfigure(0, weight=1)
        self.tab_tareas.rowconfigure(0, weight=1)
        
        columnas = ("Titulo", "Descripcion", "Estado", "Fecha", "Informe")
        self.tree = ttk.Treeview(self.tab_tareas, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tree.column("Estado", anchor="center")
        self.tree.column("Fecha", anchor="center")
        self.tree["displaycolumns"] = ("Titulo", "Descripcion", "Estado", "Fecha")
        
        scroll = ttk.Scrollbar(self.tab_tareas, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns", pady=10)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        self.tooltip_win = None
        self.celda_actual_tooltip = ("", "")
        self.tree.bind("<Motion>", self.manejar_tooltip_tabla)
        self.tree.bind("<Leave>", self.ocultar_tooltip_tabla)
        
        self.panel_botones = tk.Frame(self.tab_tareas, bg="white")
        self.panel_botones.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        # Estilo unificado de oficina para botones de acción
        _btn_style = {"font": ("Arial", 10, "bold"), "relief": "groove", "bd": 2, "cursor": "hand2", "fg": "white", "bg": "#34495e"}

        # Conexión MVC al nuevo modal de creación de tareas
        self.btn_crear = tk.Button(self.panel_botones, text="Cargar nueva tarea", command=self.abrir_modal_nueva_tarea, **_btn_style)
        self.btn_crear.pack(side="left", padx=10)
        
        self.btn_estado = tk.Button(self.panel_botones, text="Cambiar Estado", state="disabled", command=self.cambiar_estado, **_btn_style)
        self.btn_estado.pack(side="left", padx=10)
        
        self.btn_cronometraje = tk.Button(self.panel_botones, text="Realizar Cronometraje", state="disabled", command=self.ejecutar_cronometraje_tarea, **_btn_style)
        
        self.btn_borrar = tk.Button(self.panel_botones, text="Borrar tarea", state="disabled", command=self.accion_borrar_tarea, **_btn_style)
        self.btn_borrar.pack(side="left", padx=10)

    def ocultar_tooltip_tabla(self, event=None) -> None:
        if self.tooltip_win:
            self.tooltip_win.destroy()
            self.tooltip_win = None
            self.celda_actual_tooltip = ("", "")

    def manejar_tooltip_tabla(self, event) -> None:
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        
        if not item:
            self.ocultar_tooltip_tabla()
            return
            
        if col not in ("#1", "#2"):
            self.ocultar_tooltip_tabla()
            return
            
        valores = self.tree.item(item, 'values')
        idx = 0 if col == "#1" else 1
        texto = str(valores[idx])
        
        if not texto:
            self.ocultar_tooltip_tabla()
            return
            
        if (item, col) == self.celda_actual_tooltip:
            return
            
        self.ocultar_tooltip_tabla()
        self.celda_actual_tooltip = (item, col)
        
        self.tooltip_win = tk.Toplevel(self)
        self.tooltip_win.wm_overrideredirect(True)
        self.tooltip_win.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
        
        lbl = tk.Label(self.tooltip_win, text=texto, justify="left", background="#ffffe0", relief="solid", borderwidth=1, wraplength=300)
        lbl.pack()

    def configurar_rbac(self) -> None:
        usuario = self.controlador.usuario_actual
        if not usuario: return
        
        if usuario.rol == "METODISTA":
            self.btn_crear.pack_forget()
            self.btn_borrar.pack_forget()
            self.btn_cronometraje.pack(side="left", padx=10)
        else:
            self.btn_cronometraje.pack_forget()
            self.btn_crear.pack(side="left", padx=10)
            self.btn_borrar.pack(side="left", padx=10)

    def cargar_datos(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for t in self.controlador.obtener_tareas_dashboard():
                self.tree.insert("", "end", iid=str(t.id_tarea), values=(t.titulo, t.descripcion, t.estado, t.fecha, t.informe_url))
        except Exception:
            logger.exception("Error al cargar datos en la tabla.")

    def on_tree_select(self, event: Any) -> None:
        seleccion = self.tree.selection()
        if seleccion:
            self.btn_estado.config(state="normal")
            usuario = self.controlador.usuario_actual
            if usuario and usuario.rol == "JEFE/GERENTE":
                self.btn_borrar.config(state="normal")
            elif usuario and usuario.rol == "METODISTA":
                self.btn_cronometraje.config(state="normal")
        else:
            self.btn_estado.config(state="disabled")
            self.btn_borrar.config(state="disabled")
            if hasattr(self, 'btn_cronometraje'):
                self.btn_cronometraje.config(state="disabled")

    def on_double_click(self, event: Any) -> None:
        seleccion = self.tree.selection()
        if seleccion:
            try:
                id_tarea = int(seleccion[0])
                self.controlador.abrir_relevamiento_desde_tarea(id_tarea)
            except Exception:
                logger.exception("Error al capturar el doble clic en Treeview de tareas.")

    def on_double_click_recientes(self, event: Any) -> None:
        """Captura el doble clic en la tabla de trabajos recientes y abre el relevamiento.

        Extrae el ID del relevamiento desde el iid de la fila seleccionada
        y delega la carga al controlador vía abrir_relevamiento_desde_id.

        Args:
            event: Evento de Tkinter generado por el doble clic.
        """
        seleccion = self.tree_recientes.selection()
        if seleccion:
            try:
                id_rel = int(seleccion[0])
                self.controlador.abrir_relevamiento_desde_id(id_rel)
            except Exception:
                logger.exception("Error al abrir relevamiento desde la tabla de recientes.")

    def ejecutar_cronometraje_tarea(self) -> None:
        seleccion = self.tree.selection()
        if seleccion:
            try:
                id_tarea = int(seleccion[0])
                self.controlador.abrir_relevamiento_desde_tarea(id_tarea)
            except Exception:
                logger.exception("Error al abrir cronometraje desde el botón.")

    def cambiar_estado(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion: return
        try:
            id_tarea = int(seleccion[0])
            tarea_val = self.tree.item(id_tarea, "values")
            estado_actual = tarea_val[2]
            
            usuario = self.controlador.usuario_actual
            if not usuario: return
            
            # Bloqueo de Seguridad para Metodistas
            if usuario.rol == "METODISTA" and estado_actual == "Cerrado":
                messagebox.showwarning("Acceso Denegado", "No tienes permisos para modificar una tarea cerrada.")
                return

            opciones = self.controlador.obtener_opciones_estado()
            
            modal = tk.Toplevel(self)
            modal.title("Cambiar Estado")
            centrar_ventana(modal, 300, 200)
            modal.grab_set()

            tk.Label(modal, text=f"Estado actual: {estado_actual}", font=("Arial", 10)).pack(pady=(15, 5))
            
            tk.Label(modal, text="Nuevo Estado:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
            combo_estado = ttk.Combobox(modal, values=opciones, state="readonly", font=("Arial", 10))
            combo_estado.pack(pady=5)
            if estado_actual in opciones:
                combo_estado.set(estado_actual)
            elif opciones:
                combo_estado.set(opciones[0])

            def guardar():
                nuevo_estado = combo_estado.get()
                if not nuevo_estado:
                    messagebox.showerror("Error", "Debe seleccionar un estado.", parent=modal)
                    return
                
                if nuevo_estado == estado_actual:
                    modal.destroy()
                    return

                if self.controlador.cambiar_estado_tarea(id_tarea, nuevo_estado):
                    self.cargar_datos()
                    self.btn_estado.config(state="disabled")
                    self.btn_borrar.config(state="disabled")
                    if hasattr(self, 'btn_cronometraje'):
                        self.btn_cronometraje.config(state="disabled")
                    modal.destroy()
                else:
                    messagebox.showerror("Error", "Fallo al actualizar el estado.", parent=modal)

            tk.Button(modal, text="Guardar", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=guardar).pack(pady=15)

        except Exception:
            logger.exception("Fallo al cambiar estado.")

    def abrir_modal_nueva_tarea(self) -> None:
        modal = tk.Toplevel(self)
        modal.title("Nueva Tarea")
        centrar_ventana(modal, 400, 380)
        modal.grab_set()
        
        tk.Label(modal, text="Título de la Tarea:", font=("Arial", 10, "bold")).pack(pady=(10,0), anchor="w", padx=20)
        vcmd_titulo = (modal.register(lambda P: len(P) <= 50), '%P')
        entry_titulo = tk.Entry(modal, font=("Arial", 11), validate="key", validatecommand=vcmd_titulo)
        entry_titulo.pack(fill="x", padx=20, pady=5)
        
        tk.Label(modal, text="Descripción:", font=("Arial", 10, "bold")).pack(pady=(10,0), anchor="w", padx=20)
        text_desc = tk.Text(modal, font=("Arial", 10), height=4)
        text_desc.pack(fill="x", padx=20, pady=5)
        
        def limitar_texto_desc(event):
            if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab'):
                return
            if event.char and len(text_desc.get("1.0", "end-1c")) >= 100:
                return "break"
        text_desc.bind("<KeyPress>", limitar_texto_desc)
        
        tk.Label(modal, text="Metodista Asignado:", font=("Arial", 10, "bold")).pack(pady=(10,0), anchor="w", padx=20)
        metodistas = self.controlador.obtener_metodistas()
        nombres = [f"{m.id_usuario} - {m.nombre}" for m in metodistas]
        combo_metodista = ttk.Combobox(modal, values=nombres, state="readonly", font=("Arial", 10))
        combo_metodista.pack(fill="x", padx=20, pady=5)
        if nombres:
            combo_metodista.set(nombres[0])
            
        def guardar():
            tit = entry_titulo.get().strip()
            desc = text_desc.get("1.0", tk.END).strip()
            sel = combo_metodista.get()
            if not tit or not desc or not sel:
                messagebox.showerror("Error", "Todos los campos son requeridos.", parent=modal)
                return
            id_asig = int(sel.split(" - ")[0])
            if self.controlador.crear_tarea(tit, desc, id_asig):
                messagebox.showinfo("Éxito", "Tarea creada correctamente.", parent=modal)
                self.cargar_datos()
                modal.destroy()
            else:
                messagebox.showerror("Error", "Fallo al crear tarea.", parent=modal)
                
        tk.Button(modal, text="Guardar Tarea", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=guardar).pack(pady=20)

    def accion_borrar_tarea(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion: return
        id_tarea = int(seleccion[0])
        if messagebox.askyesno("Confirmar", f"¿Desea borrar permanentemente la tarea ID {id_tarea}?"):
            if self.controlador.borrar_tarea(id_tarea):
                self.cargar_datos()
                self.btn_estado.config(state="disabled")
                self.btn_borrar.config(state="disabled")
                if hasattr(self, 'btn_cronometraje'):
                    self.btn_cronometraje.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se pudo borrar la tarea.")

class PaginaRegistroUsuario(tk.Frame):
    def __init__(self, parent: tk.Widget, controlador: Any) -> None:
        super().__init__(parent, bg="#ecf0f1")
        self.controlador = controlador
        
        frame_form = tk.Frame(self, bg="white", padx=40, pady=40, bd=1, relief="solid")
        frame_form.pack(expand=True)
        
        # Registrar comandos de validación para los campos del formulario
        vcmd_nom = (self.register(self.validar_nombre), '%P')
        vcmd_user = (self.register(self.validar_usuario), '%P')
        vcmd_pass = (self.register(self.validar_password), '%P')
        
        tk.Label(frame_form, text="Registro de Usuarios", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
        
        # Nombre Completo
        tk.Label(frame_form, text="Nombre Completo", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill="x")
        self.entry_nombre = tk.Entry(frame_form, font=("Arial", 12),
                                     validate="key", validatecommand=vcmd_nom)
        self.entry_nombre.pack(fill="x", pady=(0, 10))
        self.entry_nombre.bind("<Return>", lambda e: self.intentar_registro())
        
        # Username
        tk.Label(frame_form, text="Nombre de Usuario (Username)", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill="x")
        self.entry_user = tk.Entry(frame_form, font=("Arial", 12),
                                   validate="key", validatecommand=vcmd_user)
        self.entry_user.pack(fill="x", pady=(0, 10))
        self.entry_user.bind("<Return>", lambda e: self.intentar_registro())
        
        # Rol
        tk.Label(frame_form, text="Rol del Sistema", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill="x")
        self.combo_rol = ttk.Combobox(frame_form, values=["METODISTA", "JEFE/GERENTE"], state="readonly", font=("Arial", 11))
        self.combo_rol.set("METODISTA")
        self.combo_rol.pack(fill="x", pady=(0, 10))
        self.combo_rol.bind("<Return>", lambda e: self.intentar_registro())
        
        # Contraseña
        tk.Label(frame_form, text="Contraseña", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill="x")
        self.entry_pass = tk.Entry(frame_form, font=("Arial", 12), show="*",
                                   validate="key", validatecommand=vcmd_pass)
        self.entry_pass.pack(fill="x", pady=(0, 20))
        self.entry_pass.bind("<Return>", lambda e: self.intentar_registro())
        
        # Botones
        tk.Button(frame_form, text="Crear Usuario", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=self.intentar_registro).pack(fill="x", pady=(0, 10))
        tk.Button(frame_form, text="Volver al Login", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=lambda: self.controlador.root.mostrar_frame(PaginaLogin)).pack(fill="x")

    def validar_nombre(self, P: str) -> bool:
        """Valida que el nombre contenga solo letras y espacios, máximo 30 caracteres.

        Permite cadena vacía (campo borrado). Rechaza dígitos, signos
        y cualquier carácter que no sea alfabético ni espacio.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor cumple las restricciones, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 30 and all(c.isalpha() or c.isspace() for c in P)

    def validar_usuario(self, P: str) -> bool:
        """Valida que el usuario contenga solo caracteres alfanuméricos, máximo 20.

        Permite cadena vacía (campo borrado). Rechaza espacios, signos
        de puntuación y cualquier carácter especial.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor cumple las restricciones, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 20 and P.isalnum()

    def validar_password(self, P: str) -> bool:
        """Valida que la contraseña contenga solo caracteres alfanuméricos, máximo 20.

        Permite cadena vacía (campo borrado). Rechaza caracteres especiales
        como signos de puntuación, símbolos y espacios.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si todos los caracteres son alfanuméricos, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 20 and P.isalnum()

    def intentar_registro(self) -> None:
        nombre = self.entry_nombre.get().strip()
        user = self.entry_user.get().strip()
        rol = self.combo_rol.get().strip()
        pwd = self.entry_pass.get().strip()
        
        if not nombre or not user or not rol or not pwd:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
            
        self.controlador.registrar_nuevo_usuario(nombre, user, rol, pwd)
        
    def limpiar_form(self) -> None:
        self.entry_nombre.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)
        self.combo_rol.set("METODISTA")
        
    def actualizar_vista(self) -> None:
        self.limpiar_form()

class Plantilla(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="white")
        
        self.controlador = controlador
        
        # --- VARIABLES DE CONTROL ---
        self.num_elementos: int = 0
        self.nombres_elementos: List[tk.Entry] = []  
        self.entradas_tabla: List[List[tk.Entry]] = [] 
        self.matriz_bloques: List[List[List[tk.Entry]]] = []  
        self.vars_conteo: List[tk.StringVar] = []     
        
        self.unidades_salida: List[ttk.Combobox] = [] 
        self.unidades_entrada: List[ttk.Combobox] = []
        
        self.max_filas: int = 0 
        self.widgets_resultados_columnas: List[List[tk.Widget]] = [] 
        
        self.guardado_recientemente = False
        self.id_tarea_actual = None
        self.id_relevamiento_actual = None

        self.var_de_pie = tk.BooleanVar()
        self.var_sentado = tk.BooleanVar()
        self.var_maquina = tk.StringVar()
        self.var_hm = tk.StringVar()
        self.var_operario = tk.StringVar()
        self.var_fecha = tk.StringVar(value=datetime.date.today().strftime("%d/%m/%Y"))
        self.var_id_crono = tk.StringVar(value="AUTO-001")

        # Variables para el Footer
        self.var_piezas_golpe = tk.StringVar(value="1")
        self.var_articulos_golpe = tk.StringVar(value="1")
        self.var_operarios_maq = tk.StringVar(value="1")
        self.var_tiempo_estandar_op = tk.StringVar()
        self.var_cadencia_ph = tk.StringVar()
        self.var_cadencia_h1000 = tk.StringVar()
        self.var_estandar_epicor = tk.StringVar()
        self.var_dotacion_epicor = tk.StringVar()

        # Traces para recálculo automático al cambiar variables en el footer
        self.var_piezas_golpe.trace_add("write", lambda *args: self.recalcular_todo())
        self.var_articulos_golpe.trace_add("write", lambda *args: self.recalcular_todo())
        self.var_operarios_maq.trace_add("write", lambda *args: self.recalcular_todo())
        self.var_dotacion_epicor.trace_add("write", lambda *args: self.recalcular_todo())

        # --- DISEÑO DE LA INTERFAZ ---
        btn_container = tk.Frame(self, bg="white")
        btn_container.pack(side="top", fill="x", padx=10)
        
        # Botón Abrir removido (ahora está en el menú global nativo)
        
        tk.Button(btn_container, text="Agregar nueva columna", bg="#34495e", fg="white", 
                  font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=self.ventana_datos_columna).pack(side="right", pady=5)

        self.header_frame = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=1)
        self.header_frame.pack(side="top", fill="x", padx=10, pady=5)
        self.setup_header_widgets()

        # Empaquetamos PRIMERO los elementos inferiores con side="bottom" para anclarlos.
        # Botón Finalizar anclado a la derecha abajo
        tk.Button(self, text="Finalizar", bg="#34495e", fg="white", 
                  font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=self.ventana_finalizar).pack(side="bottom", anchor="e", padx=20, pady=10)

        # Footer Frame anclado abajo (encima del botón)
        self.footer_frame = tk.Frame(self, bg="white")
        self.footer_frame.pack(side="bottom", fill="x", padx=10, pady=(15, 0))
        self.setup_footer_widgets()

        self.middle_frame = tk.Frame(self, bg="white")
        self.middle_frame.pack(side="top", fill="both", expand=True, padx=10)

        # Sincronización Estructural: Grid Maestro para alinear filas
        self.middle_frame.columnconfigure(0, weight=0) # Izquierda fija
        self.middle_frame.columnconfigure(1, weight=1) # Derecha dinámica
        self.middle_frame.rowconfigure(0, weight=1)    # Área Superior (Carga)
        self.middle_frame.rowconfigure(1, weight=0)    # Área Inferior (Resultados)
        self.middle_frame.rowconfigure(2, weight=0)    # Scrollbar Horizontal
        self.setup_left_column_widgets()

        self.setup_scrollable_area()

    def setup_header_widgets(self):
        self.header_frame.columnconfigure(0, weight=0, minsize=150)
        self.header_frame.columnconfigure(1, weight=0, minsize=120)
        self.header_frame.columnconfigure(2, weight=1)

        # Registrar comandos de validación para los campos del header
        vcmd_6 = (self.register(self.validar_max_6), '%P')
        vcmd_100 = (self.register(self.validar_max_100), '%P')

        tk.Label(self.header_frame, text="ARTÍCULO", font=("Arial", 12, "bold"), borderwidth=1, relief="solid").grid(row=0, column=0, rowspan=2, sticky="nsew")
        tk.Label(self.header_frame, text="OPERACIÓN:", font=("Arial", 10), anchor="e", padx=5, borderwidth=1, relief="solid").grid(row=0, column=1, sticky="nsew")
        
        frame_op = tk.Frame(self.header_frame, bg="white")
        frame_op.grid(row=0, column=2, sticky="nsew")
        self.combo_operacion = ttk.Combobox(frame_op, font=("Arial", 10))
        self.combo_operacion.pack(side="left", fill="both", expand=True)
        btn_add_op = tk.Button(
            frame_op,
            text="+",
            font=("Arial", 8, "bold"),
            bg="#2c3e50",
            fg="white",
            bd=1,
            relief="solid",
            width=2,
            command=lambda: self.abrir_modal_crear_recurso("OPERACION")
        )
        btn_add_op.pack(side="right", padx=(2, 0))
        btn_del_op = tk.Button(
            frame_op,
            text="-",
            font=("Arial", 8, "bold"),
            bg="#e74c3c",
            fg="white",
            bd=1,
            relief="solid",
            width=2,
            command=lambda: self.accion_borrar_recurso("OPERACION")
        )
        btn_del_op.pack(side="right", padx=(2, 0))


        tk.Label(self.header_frame, text="DESCRIPCION:", font=("Arial", 10), anchor="e", padx=5, borderwidth=1, relief="solid").grid(row=1, column=1, sticky="nsew")
        
        self.entry_descripcion_articulo = tk.Entry(self.header_frame, borderwidth=1, relief="solid", font=("Arial", 10),
                                                    validate="key", validatecommand=vcmd_100)
        self.entry_descripcion_articulo.grid(row=1, column=2, sticky="nsew")
        
        self.entry_articulo_codigo = tk.Entry(self.header_frame, borderwidth=1, relief="solid", justify="center", bg="#FFF2CC", font=("Arial", 10, "bold"),
                                               validate="key", validatecommand=vcmd_6)
        self.entry_articulo_codigo.grid(row=2, column=0, sticky="nsew")

    def setup_left_column_widgets(self):
        f_top = tk.Frame(self.middle_frame, bg="white")
        f_top.grid(row=0, column=0, sticky="nsew", pady=(10, 0))
        
        tk.Label(f_top, text="DE PIE", width=12, anchor="w", font=("Arial", 9, "bold"), padx=5, borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
        tk.Checkbutton(f_top, variable=self.var_de_pie, bg="white", borderwidth=1, relief="solid", command=lambda: self.exclusividad_postura("pie")).grid(row=0, column=1, sticky="nsew")
        tk.Label(f_top, text="SENTADO", width=12, anchor="w", font=("Arial", 9, "bold"), padx=5, borderwidth=1, relief="solid").grid(row=1, column=0, sticky="nsew")
        tk.Checkbutton(f_top, variable=self.var_sentado, bg="white", borderwidth=1, relief="solid", command=lambda: self.exclusividad_postura("sentado")).grid(row=1, column=1, sticky="nsew")

        labels = [("MÁQUINA", self.var_maquina), ("HM", self.var_hm), ("OPERARIO", self.var_operario), 
                  ("FECHA", self.var_fecha), ("Nº de CRONOMETRAJE", self.var_id_crono)]
        for i, (txt, var) in enumerate(labels):
            font_style = ("Arial", 9, "bold") if txt == "Nº de CRONOMETRAJE" else ("Arial", 9, "bold", "italic")
            tk.Label(f_top, text=txt, font=font_style, anchor="w", padx=5, borderwidth=1, relief="solid").grid(row=2+i, column=0, sticky="nsew")
            if txt == "MÁQUINA":
                frame_maq = tk.Frame(f_top, bg="white")
                frame_maq.grid(row=2+i, column=1, sticky="nsew")
                self.combo_maquina = ttk.Combobox(frame_maq, state="normal", width=10, textvariable=self.var_maquina)
                self.combo_maquina.pack(side="left", fill="both", expand=True)
                btn_add_maq = tk.Button(
                    frame_maq, 
                    text="+", 
                    font=("Arial", 8, "bold"), 
                    bg="#2c3e50", 
                    fg="white", 
                    bd=1, 
                    relief="solid", 
                    width=2, 
                    command=lambda: self.abrir_modal_crear_recurso("MAQUINA")
                )
                btn_add_maq.pack(side="right", padx=(2, 0))
                btn_del_maq = tk.Button(
                    frame_maq,
                    text="-",
                    font=("Arial", 8, "bold"),
                    bg="#e74c3c",
                    fg="white",
                    bd=1,
                    relief="solid",
                    width=2,
                    command=lambda: self.accion_borrar_recurso("MAQUINA")
                )
                btn_del_maq.pack(side="right", padx=(2, 0))
            elif txt == "HM":
                frame_hm = tk.Frame(f_top, bg="white")
                frame_hm.grid(row=2+i, column=1, sticky="nsew")
                self.combo_hm = ttk.Combobox(frame_hm, state="normal", width=10, textvariable=self.var_hm)
                self.combo_hm.pack(side="left", fill="both", expand=True)
                btn_add_hm = tk.Button(
                    frame_hm, 
                    text="+", 
                    font=("Arial", 8, "bold"), 
                    bg="#2c3e50", 
                    fg="white", 
                    bd=1, 
                    relief="solid", 
                    width=2, 
                    command=lambda: self.abrir_modal_crear_recurso("HM")
                )
                btn_add_hm.pack(side="right", padx=(2, 0))
                btn_del_hm = tk.Button(
                    frame_hm,
                    text="-",
                    font=("Arial", 8, "bold"),
                    bg="#e74c3c",
                    fg="white",
                    bd=1,
                    relief="solid",
                    width=2,
                    command=lambda: self.accion_borrar_recurso("HM")
                )
                btn_del_hm.pack(side="right", padx=(2, 0))
            elif txt == "OPERARIO":
                vcmd_op = (self.register(self.validar_letras_30), '%P')
                self.entry_operario = tk.Entry(f_top, textvariable=self.var_operario, borderwidth=1, relief="solid", bg="white", width=15,
                                               validate="key", validatecommand=vcmd_op)
                self.entry_operario.grid(row=2+i, column=1, sticky="nsew")
            else:
                bg_c = "#FFF2CC" if txt == "Nº de CRONOMETRAJE" else "white"
                tk.Entry(f_top, textvariable=var, borderwidth=1, relief="solid", bg=bg_c, width=15).grid(row=2+i, column=1, sticky="nsew")

        # lila_frame anclado EXACTAMENTE en la misma fila base (row=1) que el Área de Resultados
        self.lila_frame = tk.Frame(self.middle_frame, bg="white")
        self.lila_frame.grid(row=1, column=0, sticky="nsew")
        
        titulos_resultados = ["Nº de Observaciones", "Elementos medidos", "Lote frecuencial", "Tiempo MEDIO", 
                              "Desvío estandar", "Nº Obs. Necesarias", "Rango mediciones", "Suplemento", "Tiempo Normal", "Tiempo Estandar"]
        for i, txt in enumerate(titulos_resultados):
            tk.Label(self.lila_frame, text=txt, font=("Arial", 9, "bold"), anchor="w", padx=5, borderwidth=1, relief="solid", bg="white").grid(row=i, column=0, sticky="nsew")
            # Sincronización Pixel-Perfect: forzamos el alto de cada fila de etiqueta a 24px
            self.lila_frame.rowconfigure(i, minsize=24)
        self.lila_frame.columnconfigure(0, weight=1)

    def setup_scrollable_area(self) -> None:
        # Área de Carga (Superior) - Con scroll vertical
        self.canvas = tk.Canvas(self.middle_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=(10, 0))
        
        sb_y = tk.Scrollbar(self.middle_frame, orient="vertical", command=self.canvas.yview)
        sb_y.grid(row=0, column=2, sticky="ns", pady=(10, 0))
        
        self.tabla_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.tabla_frame, anchor="nw")
        
        # Área de Resultados (Inferior) - Sin scroll vertical
        self.canvas_resultados = tk.Canvas(self.middle_frame, bg="white", highlightthickness=0, height=240)
        self.canvas_resultados.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        
        self.tabla_resultados_frame = tk.Frame(self.canvas_resultados, bg="white")
        self.canvas_resultados.create_window((0, 0), window=self.tabla_resultados_frame, anchor="nw")
        
        # Scrollbar Horizontal (Compartida)
        sb_x = tk.Scrollbar(self.middle_frame, orient="horizontal")
        sb_x.grid(row=2, column=1, sticky="ew", padx=(5, 0))
        
        # Sincronización Horizontal
        def scroll_x(*args: Any) -> None:
            self.canvas.xview(*args)
            self.canvas_resultados.xview(*args)
            
        sb_x.config(command=scroll_x)
        self.canvas.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)
        self.canvas_resultados.configure(xscrollcommand=sb_x.set)
        
        self.tabla_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.tabla_resultados_frame.bind("<Configure>", lambda e: self.canvas_resultados.configure(scrollregion=self.canvas_resultados.bbox("all")))

        # Scroll del ratón solo para el Área de Carga superior
        def _on_mousewheel(event: Any) -> None:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def setup_footer_widgets(self):
        font_style = ("Arial", 9, "bold")
        vcmd_piezas = (self.register(self.validar_entrada_numerica), '%P', '10')
        vcmd_articulos = (self.register(self.validar_entrada_numerica), '%P', '10')
        vcmd_operarios = (self.register(self.validar_entrada_numerica), '%P', '2')
        
        tk.Label(self.footer_frame, text="Piezas por golpe", bg="white", font=font_style).grid(row=0, column=0, sticky="e", padx=(0,5), pady=2)
        self.ent_piezas_golpe = tk.Entry(self.footer_frame, textvariable=self.var_piezas_golpe, borderwidth=1, relief="solid", justify="center", bg="#FFF2CC", width=8,
                                         validate="key", validatecommand=vcmd_piezas)
        self.ent_piezas_golpe.grid(row=0, column=1, sticky="w")
        self.ent_piezas_golpe.bind("<KeyRelease>", lambda e: self.recalcular_todo())
        self.ent_piezas_golpe.bind("<FocusOut>", lambda e: self.recalcular_todo())
        tk.Label(self.footer_frame, text="Unidades/golpe", bg="white", font=font_style).grid(row=0, column=2, sticky="w", padx=(5,20))

        tk.Label(self.footer_frame, text="Artículos por golpe", bg="white", font=font_style).grid(row=1, column=0, sticky="e", padx=(0,5), pady=2)
        self.ent_articulos_golpe = tk.Entry(self.footer_frame, textvariable=self.var_articulos_golpe, borderwidth=1, relief="solid", justify="center", bg="#FFF2CC", width=8,
                                            validate="key", validatecommand=vcmd_articulos)
        self.ent_articulos_golpe.grid(row=1, column=1, sticky="w")
        self.ent_articulos_golpe.bind("<KeyRelease>", lambda e: self.recalcular_todo())
        self.ent_articulos_golpe.bind("<FocusOut>", lambda e: self.recalcular_todo())
        tk.Label(self.footer_frame, text="Unidades/golpe", bg="white", font=font_style).grid(row=1, column=2, sticky="w", padx=(5,20))

        tk.Label(self.footer_frame, text="Nº de operarios en máquina", bg="white", font=font_style).grid(row=2, column=0, sticky="e", padx=(0,5), pady=2)
        self.ent_operarios_maq = tk.Entry(self.footer_frame, textvariable=self.var_operarios_maq, borderwidth=1, relief="solid", justify="center", bg="#FFF2CC", width=8,
                                          validate="key", validatecommand=vcmd_operarios)
        self.ent_operarios_maq.grid(row=2, column=1, sticky="w")
        self.ent_operarios_maq.bind("<KeyRelease>", lambda e: self.recalcular_todo())
        self.ent_operarios_maq.bind("<FocusOut>", lambda e: self.recalcular_todo())

        tk.Label(self.footer_frame, text="Tiempo estandar operación", bg="white", font=font_style).grid(row=0, column=3, sticky="e", padx=(20,5), pady=2)
        self.ent_tiempo_estandar_op = tk.Entry(self.footer_frame, textvariable=self.var_tiempo_estandar_op, borderwidth=1, relief="solid", justify="center", bg="#C6EFCE", width=10)
        self.ent_tiempo_estandar_op.grid(row=0, column=4, sticky="w")
        self.ent_tiempo_estandar_op.config(state="readonly")
        tk.Label(self.footer_frame, text="minutos/pieza (de CADA artículo)", bg="white", font=font_style).grid(row=0, column=5, sticky="w", padx=(5,20))

        tk.Label(self.footer_frame, text="Cadencia", bg="white", font=font_style).grid(row=1, column=3, sticky="e", padx=(20,5), pady=2)
        self.ent_cadencia_ph = tk.Entry(self.footer_frame, textvariable=self.var_cadencia_ph, borderwidth=1, relief="solid", justify="center", bg="#C6EFCE", width=10)
        self.ent_cadencia_ph.grid(row=1, column=4, sticky="w")
        self.ent_cadencia_ph.config(state="readonly")
        tk.Label(self.footer_frame, text="piezas/hora (de CADA artículo)", bg="white", font=font_style).grid(row=1, column=5, sticky="w", padx=(5,20))

        tk.Label(self.footer_frame, text="Cadencia", bg="white", font=font_style).grid(row=2, column=3, sticky="e", padx=(20,5), pady=2)
        self.ent_cadencia_h1000 = tk.Entry(self.footer_frame, textvariable=self.var_cadencia_h1000, borderwidth=1, relief="solid", justify="center", bg="#C6EFCE", width=10)
        self.ent_cadencia_h1000.grid(row=2, column=4, sticky="w")
        self.ent_cadencia_h1000.config(state="readonly")
        tk.Label(self.footer_frame, text="horas/1000 piezas", bg="white", font=font_style).grid(row=2, column=5, sticky="w", padx=(5,20))

        epicor_frame = tk.Frame(self.footer_frame, bg="#E7E6E6", borderwidth=1, relief="solid")
        epicor_frame.grid(row=0, column=6, rowspan=3, sticky="nsew", padx=(20, 0))
        epicor_frame.rowconfigure(0, weight=1); epicor_frame.rowconfigure(1, weight=1)
        epicor_frame.rowconfigure(2, weight=1); epicor_frame.rowconfigure(3, weight=1)

        tk.Label(epicor_frame, text="Estandar Epicor", bg="#E7E6E6", font=font_style).grid(row=1, column=0, sticky="e", padx=(15,5))
        self.ent_estandar_epicor = tk.Entry(epicor_frame, textvariable=self.var_estandar_epicor, borderwidth=1, relief="solid", justify="center", bg="#00B0F0", width=10)
        self.ent_estandar_epicor.grid(row=1, column=1, sticky="w")
        self.ent_estandar_epicor.config(state="readonly")
        tk.Label(epicor_frame, text="hh/1000", bg="#E7E6E6", font=font_style).grid(row=1, column=2, sticky="w", padx=(5,15))

        tk.Label(epicor_frame, text="Dotación Epicor", bg="#E7E6E6", font=font_style).grid(row=2, column=0, sticky="e", padx=(15,5))
        self.ent_dotacion_epicor = tk.Entry(epicor_frame, textvariable=self.var_dotacion_epicor, borderwidth=1, relief="solid", justify="center", bg="#00B0F0", width=10)
        self.ent_dotacion_epicor.grid(row=2, column=1, sticky="w")
        self.ent_dotacion_epicor.config(state="readonly")
        tk.Label(epicor_frame, text="operarios", bg="#E7E6E6", font=font_style).grid(row=2, column=2, sticky="w", padx=(5,15))

    def sincronizar_lila(self, n_filas: int) -> None:
        # Ya no es necesario recalcular alturas, los paneles estáticos están anclados abajo.
        pass

    def agregar_elemento_dinamico(self, n_filas):
        self.guardado_recientemente = False 
        
        if n_filas > self.max_filas:
            old_max = self.max_filas
            self.max_filas = n_filas
            self.sincronizar_lila(self.max_filas)
            
            for b in range(self.num_elementos):
                col_base_existente = b * 3
                for f_idx in range(old_max, self.max_filas):
                    if len(self.entradas_tabla) <= f_idx: 
                        self.entradas_tabla.append([])
                    
                    f_w = []
                    for c in range(3):
                        en = tk.Entry(self.tabla_frame, borderwidth=1, relief="solid", width=8, bg="#E7E6E6", justify="center")
                        en.config(state="disabled")
                        en.grid(row=f_idx + 2, column=col_base_existente + c, sticky="nsew")
                        f_w.append(en)
                        self.entradas_tabla[f_idx].append(en)
                    self.matriz_bloques[b].append(f_w)
                
                # Los resultados ahora siempre empiezan desde la fila 0 en tabla_resultados_frame
                r_idx_nuevo = 0
                widgets_columna = self.widgets_resultados_columnas[b]
                for i, widget in enumerate(widgets_columna):
                    widget.grid(row=r_idx_nuevo + i, column=col_base_existente, columnspan=3, sticky="nsew")

        col_base = self.num_elementos * 3
        
        ent_n = tk.Entry(self.tabla_frame, borderwidth=1, relief="solid", justify="center", bg="white", fg="grey")
        ent_n.insert(0, "Nombre Elemento")
        ent_n.grid(row=0, column=col_base, columnspan=3, sticky="nsew", ipady=12) 
        self.nombres_elementos.append(ent_n)
        
        def on_focus_in(event, entry=ent_n):
            if entry.get() == "Nombre Elemento":
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event, entry=ent_n):
            if entry.get() == "":
                entry.insert(0, "Nombre Elemento")
                entry.config(fg="grey")

        ent_n.bind("<FocusIn>", on_focus_in)
        ent_n.bind("<FocusOut>", on_focus_out)
        tk.Label(self.tabla_frame, text="V", font=("Arial", 8, "bold"), bg=config.COLOR_BG_TABLA_HEAD, borderwidth=1, relief="solid").grid(row=1, column=col_base, sticky="nsew")
        
        tk.Label(self.tabla_frame, text="MIN", font=("Arial", 8, "bold"), bg=config.COLOR_BG_TABLA_HEAD, borderwidth=1, relief="solid").grid(row=1, column=col_base+1, sticky="nsew")
        
        combo_entrada = ttk.Combobox(self.tabla_frame, values=["SEG", "MIN"], state="readonly", font=("Arial", 8, "bold"), justify="center", width=6)
        combo_entrada.set("SEG")
        combo_entrada.grid(row=1, column=col_base+2, sticky="nsew")
        combo_entrada.bind("<<ComboboxSelected>>", lambda e: self.recalcular_todo())
        self.unidades_entrada.append(combo_entrada)
        self.unidades_salida.append(combo_entrada)

        bloque = []
        vcmd_v = (self.register(self.validar_entrada_numerica), '%P', '3')
        vcmd_seg = (self.register(self.validar_entrada_numerica), '%P', '5')
        for f in range(self.max_filas):
            if len(self.entradas_tabla) <= f: 
                self.entradas_tabla.append([])
            f_w = []
            for c in range(3):
                is_active = (f < n_filas)
                if c == 1:
                    bg_color = "#E7E6E6"
                else:
                    bg_color = "white" if is_active else "#E7E6E6"
                
                # Aplicar validación numérica solo a columnas V (índice 0) y SEG (índice 2)
                if c in (0, 2):
                    vcmd = vcmd_v if c == 0 else vcmd_seg
                    en = tk.Entry(self.tabla_frame, borderwidth=1, relief="solid", width=8, bg=bg_color, justify="center",
                                  validate="key", validatecommand=vcmd)
                else:
                    en = tk.Entry(self.tabla_frame, borderwidth=1, relief="solid", width=8, bg=bg_color, justify="center")
                
                if is_active:
                    if c == 0:
                        en.bind("<KeyRelease>", lambda e, b=self.num_elementos: self._on_cell_edit(b))
                        en.bind("<Return>", lambda e, b_val=self.num_elementos, r_val=f, c_val=c: self._mover_foco_abajo(e, b_val, r_val, c_val))
                        
                        def on_v_focus_in(event, entry=en):
                            val = entry.get().strip()
                            if val.endswith("%"):
                                entry.delete(0, tk.END)
                                entry.insert(0, val[:-1].strip())
                                
                        def on_v_focus_out(event, entry=en):
                            val = entry.get().strip()
                            if not val:
                                return
                            if val.endswith("%"):
                                val = val[:-1].strip()
                            if val.isdigit() or val.replace(".", "", 1).isdigit():
                                entry.delete(0, tk.END)
                                entry.insert(0, f"{val}%")
                            self.recalcular_todo()
                            
                        en.bind("<FocusIn>", on_v_focus_in)
                        en.bind("<FocusOut>", on_v_focus_out)
                    elif c == 1:
                        en.config(state="readonly")
                    elif c == 2:
                        en.bind("<KeyRelease>", lambda e, b=self.num_elementos: self._on_cell_edit(b))
                        en.bind("<Return>", lambda e, b_val=self.num_elementos, r_val=f, c_val=c: self._mover_foco_abajo(e, b_val, r_val, c_val))
                else:
                    if c == 1:
                        en.config(state="readonly")
                    else:
                        en.config(state="disabled")
                    
                en.grid(row=f + 2, column=col_base + c, sticky="nsew")
                f_w.append(en)
                self.entradas_tabla[f].append(en)
            bloque.append(f_w)
        self.matriz_bloques.append(bloque)

        # Resultados Finales de la Columna van a tabla_resultados_frame (Fila 0)
        r_idx = 0
        var_c = tk.StringVar(value="0"); self.vars_conteo.append(var_c)
        
        lbl_conteo = tk.Label(self.tabla_resultados_frame, textvariable=var_c, font=("Arial", 9), borderwidth=1, relief="solid", bg="white")
        lbl_conteo.grid(row=r_idx, column=col_base, columnspan=3, sticky="nsew")
        self.tabla_resultados_frame.rowconfigure(r_idx, minsize=24)
        
        widgets_bottom = [lbl_conteo]
        
        vcmd_bot_10 = (self.register(self.validar_entrada_numerica), '%P', '10')
        for i in range(1, 10):
            bg_color = "#FFF2CC" if i in [2, 7] else "white" 
            if i in [1, 2, 7]:
                ent_bot = tk.Entry(self.tabla_resultados_frame, borderwidth=1, relief="solid", justify="center", bg=bg_color,
                                   validate="key", validatecommand=vcmd_bot_10)
            else:
                ent_bot = tk.Entry(self.tabla_resultados_frame, borderwidth=1, relief="solid", justify="center", bg=bg_color)
            ent_bot.grid(row=r_idx+i, column=col_base, columnspan=3, sticky="nsew")
            self.tabla_resultados_frame.rowconfigure(r_idx+i, minsize=24)
            
            if i in [1, 2, 7]:
                ent_bot.bind("<KeyRelease>", lambda e: self.recalcular_todo())
                ent_bot.bind("<FocusOut>", lambda e: self.recalcular_todo())
                if i == 1:
                    ent_bot.insert(0, "1")
                elif i == 2:
                    ent_bot.insert(0, "1")
                elif i == 7:
                    ent_bot.insert(0, "0")
            else:
                ent_bot.config(state="disabled")
                
            widgets_bottom.append(ent_bot)
            
        self.widgets_resultados_columnas.append(widgets_bottom)

        # Sincronización Horizontal (Ancho)
        for i in range(3): 
            self.tabla_frame.columnconfigure(col_base+i, weight=0, minsize=75)
            self.tabla_resultados_frame.columnconfigure(col_base+i, weight=0, minsize=75)
        self.num_elementos += 1

    def ventana_datos_columna(self):
        ventana = tk.Toplevel(self)
        ventana.title("Configuración")
        centrar_ventana(ventana, 300, 200)
        ventana.grab_set()
        tk.Label(ventana, text="N° de observaciones:").pack(pady=5)
        ent_f = tk.Entry(ventana); ent_f.insert(0, "10"); ent_f.pack()
        tk.Label(ventana, text="Cantidad de Elementos:").pack(pady=5)
        ent_c = tk.Entry(ventana); ent_c.insert(0, "1"); ent_c.pack()
        def confirmar() -> None:
            try:
                f, c = int(ent_f.get()), int(ent_c.get())
                ventana.destroy()
                for _ in range(c): 
                    self.agregar_elemento_dinamico(f)
            except ValueError:
                logger.warning("Intento de configuración con datos no enteros (EAFP).")
                messagebox.showerror("Error", "Los valores deben ser números enteros.")
            except Exception:
                logger.exception("Fallo inesperado al configurar columnas dinámicas.")
                messagebox.showerror("Error", "Error al procesar la configuración.")
        tk.Button(ventana, text="Generar", bg="#34495e", fg="white", font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2", command=confirmar).pack(pady=15)

    def actualizar_conteo(self, b_idx):
        self.guardado_recientemente = False 
        conteo = sum(1 for fila in self.matriz_bloques[b_idx] if any(c.get().strip() for c in fila))
        self.vars_conteo[b_idx].set(str(conteo))

    def exclusividad_postura(self, s):
        if s == "pie" and self.var_de_pie.get(): self.var_sentado.set(False)
        elif s == "sentado" and self.var_sentado.get(): self.var_de_pie.set(False)

    def ventana_finalizar(self):
        popup = tk.Toplevel(self)
        popup.title("Opciones de Cierre")
        centrar_ventana(popup, 350, 200)
        popup.grab_set()

        tk.Label(popup, text="¿Qué opción desea realizar?", font=("Arial", 11, "bold")).pack(pady=15)

        if not self.guardado_recientemente:
            tk.Button(popup, text="Guardar como PDF", bg="#34495e", fg="white", font=("Arial", 10, "bold"), 
                      relief="groove", bd=2, cursor="hand2", command=lambda: self.accion_guardar(popup)).pack(fill="x", padx=40, pady=5)

        tk.Button(popup, text="Salir sin guardar", bg="#34495e", fg="white", font=("Arial", 10, "bold"), 
                  relief="groove", bd=2, cursor="hand2", command=lambda: self.accion_salir(popup)).pack(fill="x", padx=40, pady=5)

        tk.Button(popup, text="Cancelar", bg="#34495e", fg="white", font=("Arial", 10, "bold"), 
                  relief="groove", bd=2, cursor="hand2", command=popup.destroy).pack(fill="x", padx=40, pady=5)

    def accion_guardar(self, popup):
        popup.destroy()
        exito = self.controlador.guardar_archivo()
        if exito:
            self.guardado_recientemente = True

    def accion_salir(self, popup):
        popup.destroy()
        self.limpiar_datos()
        # Retorna al Dashboard usando el método de Aplicacion
        self.controlador.root.mostrar_frame(PaginaTareas)

    def limpiar_datos(self) -> None:
        self.num_elementos = 0
        self.max_filas = 0
        self.nombres_elementos.clear()
        self.entradas_tabla.clear()
        self.matriz_bloques.clear()
        self.vars_conteo.clear()
        self.unidades_salida.clear()
        self.unidades_entrada.clear()
        self.widgets_resultados_columnas.clear()
        self.id_tarea_actual = None
        self.id_relevamiento_actual = None

        self.var_de_pie.set(False)
        self.var_sentado.set(False)
        self.var_maquina.set("")
        self.var_hm.set("")
        self.var_operario.set("")
        self.var_id_crono.set("AUTO-001")
        
        self.var_piezas_golpe.set("1")
        self.var_articulos_golpe.set("1")
        self.var_operarios_maq.set("1")
        self.var_tiempo_estandar_op.set("")
        self.var_cadencia_ph.set("")
        self.var_cadencia_h1000.set("")
        self.var_estandar_epicor.set("")
        self.var_dotacion_epicor.set("")

        self.guardado_recientemente = False

        for widget in self.tabla_frame.winfo_children():
            widget.destroy()
            
        for widget in self.tabla_resultados_frame.winfo_children():
            widget.destroy()

        for widget in self.header_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

        # El Combobox de operación vive dentro de frame_op (hijo de header_frame),
        # por lo que el bucle anterior no lo alcanza. Limpieza explícita.
        self.combo_operacion.set("")

        self.sincronizar_lila(0)

    def actualizar_vista(self) -> None:
        """
        Inicializa dinámicamente la vista al mostrarse:
        1. Establece la fecha actual.
        2. Obtiene y muestra el correlativo de cronometraje desde la BD.
        3. Carga las listas de Máquinas y HM en los comboboxes.
        """
        import datetime
        self.limpiar_datos()
        
        # 1. Fecha actual
        self.var_fecha.set(datetime.date.today().strftime("%d/%m/%Y"))
        
        # 2. Correlativo de cronometraje
        try:
            next_id = self.controlador.obtener_siguiente_id_relevamiento()
            self.var_id_crono.set(f"AUTO-{next_id:03d}")
        except Exception:
            logger.exception("No se pudo obtener el siguiente correlativo para la vista.")
            self.var_id_crono.set("AUTO-001")
            
        # 3. Poblar Comboboxes
        try:
            self.combo_maquina['values'] = self.controlador.obtener_lista_maquinas()
            self.combo_hm['values'] = self.controlador.obtener_lista_hms()
            self.combo_operacion['values'] = self.controlador.obtener_lista_operaciones()
        except Exception:
            logger.exception("Error al poblar comboboxes de datos maestros en la vista.")

    def validar_entrada_numerica(self, P: str, max_len: str = "") -> bool:
        """
        Valida que el string P sea un float positivo o un estado de transición válido.

        Acepta cadena vacía (borrado), dígitos, un solo punto decimal,
        y el carácter '%' al final (para valoraciones). Rechaza letras,
        signos negativos y caracteres especiales.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor es válido, False para rechazar la pulsación.
        """
        if P == "":
            return True
        
        P_clean = P.replace("%", "")
        if max_len and max_len.isdigit():
            if len(P_clean) > int(max_len):
                return False

        # Permitir '%' solo al final (para valoraciones tipo "100%")
        if P.endswith("%"):
            P = P[:-1]
        if P == "":
            return True
        # Permitir un solo punto decimal y solo dígitos
        if P == ".":
            return True
        try:
            val = float(P)
            return val >= 0.0
        except ValueError:
            return False

    def validar_letras_30(self, P: str) -> bool:
        """Valida que el texto contenga solo letras y espacios, con máximo 30 caracteres.

        Permite cadena vacía (campo borrado). Rechaza dígitos, signos
        y cualquier carácter que no sea alfabético ni espacio.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si el valor cumple las restricciones, False en caso contrario.
        """
        if P == "":
            return True
        return len(P) <= 30 and all(c.isalpha() or c.isspace() for c in P)

    def validar_max_6(self, P: str) -> bool:
        """Valida que el texto no exceda 6 caracteres de cualquier tipo.

        Permite cadena vacía (campo borrado). Acepta letras, dígitos
        y caracteres especiales siempre que la longitud no supere 6.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si la longitud es válida, False en caso contrario.
        """
        return len(P) <= 6

    def validar_max_100(self, P: str) -> bool:
        """Valida que el texto no exceda 100 caracteres de cualquier tipo.

        Permite cadena vacía (campo borrado). Acepta letras, dígitos
        y caracteres especiales siempre que la longitud no supere 100.

        Args:
            P: String actual del widget Entry tras la edición propuesta.

        Returns:
            True si la longitud es válida, False en caso contrario.
        """
        return len(P) <= 100

    def accion_borrar_recurso(self, tipo: str) -> None:
        """
        Elimina el recurso actualmente seleccionado en el Combobox correspondiente.

        Lee el valor actual del Combobox de MAQUINA, HM u OPERACION,
        pide confirmación al usuario, delega la eliminación al controlador
        y recarga la lista.

        Args:
            tipo: Tipo de recurso ('MAQUINA', 'HM' u 'OPERACION').
        """
        if tipo == "MAQUINA":
            combo = self.combo_maquina
            var = self.var_maquina
            tipo_legible = "Máquina"
        elif tipo == "OPERACION":
            combo = self.combo_operacion
            var = None
            tipo_legible = "Operación"
        else:
            combo = self.combo_hm
            var = self.var_hm
            tipo_legible = "Herramienta/Matriz"
        nombre = combo.get().strip()


        if not nombre:
            messagebox.showwarning(
                "Sin selección",
                f"Seleccione una {tipo_legible} del desplegable antes de intentar eliminar."
            )
            return

        confirmado = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar la {tipo_legible} '{nombre}'?\n\n"
            f"Si está asociada a relevamientos existentes, la operación será rechazada por la base de datos."
        )
        if not confirmado:
            return

        exito = self.controlador.borrar_recurso(nombre, tipo)
        if exito:
            messagebox.showinfo("Éxito", f"{tipo_legible} '{nombre}' eliminada correctamente.")
            if var is not None:
                var.set("")
            else:
                combo.set("")
            if tipo == "MAQUINA":
                self.combo_maquina['values'] = self.controlador.obtener_lista_maquinas()
            elif tipo == "OPERACION":
                self.combo_operacion['values'] = self.controlador.obtener_lista_operaciones()
            else:
                self.combo_hm['values'] = self.controlador.obtener_lista_hms()
        else:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar '{nombre}'.\n"
                f"Puede estar asociada a relevamientos existentes."
            )

    def abrir_modal_crear_recurso(self, tipo: str) -> None:
        """
        Abre una pequeña ventana modal (Toplevel) para ingresar una nueva Máquina o HM.
        
        Args:
            tipo (str): El tipo de recurso a crear ('MAQUINA' o 'HM').
        """
        modal = tk.Toplevel(self)
        titulos_tipo = {"MAQUINA": "Máquina", "HM": "Herramienta/Matriz", "OPERACION": "Operación"}
        titulo_legible = titulos_tipo.get(tipo, tipo)
        modal.title(f"Nueva {titulo_legible}")
        centrar_ventana(modal, 350, 150)
        modal.resizable(False, False)
        modal.grab_set()  # Hacerlo modal

        # Centrar el modal sobre la ventana principal
        modal.transient(self)
        
        # Etiqueta
        tk.Label(
            modal, 
            text=f"Ingrese el nombre de la nueva {titulo_legible}:", 
            font=("Arial", 10, "bold")
        ).pack(pady=(15, 5))

        # Campo de entrada
        entry_nombre = tk.Entry(modal, font=("Arial", 11), width=30)
        entry_nombre.pack(pady=5)
        entry_nombre.focus_set()

        def guardar() -> None:
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error de Validación", "El nombre no puede estar vacío.", parent=modal)
                return
            
            # Llamar al controlador para insertar en la BD
            exito = self.controlador.crear_recurso(nombre, tipo)
            if exito:
                messagebox.showinfo("Éxito", f"'{nombre}' guardado correctamente.", parent=modal)
                
                # Recargar las opciones en el combobox correspondiente y dejar seleccionado el nuevo elemento
                if tipo == "MAQUINA":
                    self.combo_maquina['values'] = self.controlador.obtener_lista_maquinas()
                    self.var_maquina.set(nombre)
                elif tipo == "HM":
                    self.combo_hm['values'] = self.controlador.obtener_lista_hms()
                    self.var_hm.set(nombre)
                elif tipo == "OPERACION":
                    self.combo_operacion['values'] = self.controlador.obtener_lista_operaciones()
                    self.combo_operacion.set(nombre)
                
                modal.destroy()
            else:
                messagebox.showerror("Error", f"No se pudo registrar '{nombre}' en la base de datos.", parent=modal)

        # Botón Guardar
        btn_guardar = tk.Button(
            modal, 
            text="Guardar", 
            bg="#34495e", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            relief="groove", bd=2, cursor="hand2",
            command=guardar
        )
        btn_guardar.pack(pady=15)

        # Bind Enter key to save
        entry_nombre.bind("<Return>", lambda e: guardar())

    def _on_cell_edit(self, b_idx: int) -> None:
        """Helper para actualizar conteo y disparar recálculos."""
        self.actualizar_conteo(b_idx)
        self.recalcular_todo()

    def recalcular_todo(self, event: Any = None) -> None:
        """
        Motor de cálculo en tiempo real refactorizado:
        Normaliza a MINUTOS, extrae variables limpias, calcula estadísticas industriales
        y actualiza la visualización de resultados y variables del footer.
        """
        import math
        import statistics

        def set_readonly_val(entry: tk.Entry, val: str) -> None:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, val)
            entry.config(state="readonly")

        t_estandar_total = 0.0

        for b_idx in range(self.num_elementos):
            # Obtener el combobox del encabezado para este elemento
            unit = "SEG"
            try:
                unit = self.unidades_entrada[b_idx].get().strip()
            except Exception:
                pass

            # Paso 1: Normalización a MINUTOS
            for row_idx, fila in enumerate(self.matriz_bloques[b_idx]):
                if row_idx >= self.max_filas:
                    continue
                val_raw_str = fila[2].get().strip()
                if not val_raw_str:
                    set_readonly_val(fila[1], "")
                    continue

                try:
                    val_raw = float(val_raw_str)
                    if unit == "SEG":
                        val_min = val_raw / 60.0
                    else:
                        val_min = val_raw
                    set_readonly_val(fila[1], f"{val_min:.4f}")
                except ValueError:
                    set_readonly_val(fila[1], "")

            # Paso 2: Extracción de variables limpias
            minutos = []
            valoraciones = []
            
            for row_idx, fila in enumerate(self.matriz_bloques[b_idx]):
                if row_idx >= self.max_filas:
                    continue
                min_str = fila[1].get().strip()
                v_str = fila[0].get().strip()
                
                if min_str and v_str:
                    try:
                        m_val = float(min_str)
                        clean_v = v_str
                        if clean_v.endswith("%"):
                            clean_v = clean_v[:-1].strip()
                        v_val = float(clean_v) / 100.0
                        
                        minutos.append(m_val)
                        valoraciones.append(v_val)
                    except ValueError:
                        pass

            widgets = self.widgets_resultados_columnas[b_idx]
            n = len(minutos)

            if n == 0:
                set_readonly_val(widgets[3], "0.0000")  # Tiempo MEDIO
                set_readonly_val(widgets[4], "0.0000")  # Desvío estandar
                set_readonly_val(widgets[5], "0.00")    # Obs. Necesarias
                set_readonly_val(widgets[6], "MIN: 0.00 | MAX: 0.00") # Rango
                set_readonly_val(widgets[8], "0.0000")  # Tiempo Normal
                set_readonly_val(widgets[9], "0.0000")  # Tiempo Estandar
                continue

            # Paso 3: Fórmulas Estadísticas
            # Inputs manuales
            try:
                elem_val = float(widgets[1].get().strip() or 1.0)
            except ValueError:
                elem_val = 1.0

            try:
                lote_str = widgets[2].get().strip()
                lote_val = float(lote_str) if lote_str else None
            except ValueError:
                lote_val = None

            try:
                sup_str = widgets[7].get().strip()
                if sup_str.endswith("%"):
                    suplemento = float(sup_str[:-1].strip()) / 100.0
                else:
                    val_sup = float(sup_str)
                    if val_sup >= 1.0:
                        suplemento = val_sup / 100.0
                    else:
                        suplemento = val_sup
            except ValueError:
                suplemento = 0.0

            # Divisor: div = lote_frecuencial o elementos_medidos
            div = lote_val if lote_val is not None else elem_val
            if div <= 0:
                div = 1.0

            # Tiempo Medio: sum(minutos) / (n * div)
            sum_min = sum(minutos)
            medio = sum_min / (n * div)
            set_readonly_val(widgets[3], f"{medio:.4f}")

            # Desvío Estándar: statistics.stdev(minutos) (si n>=2, sino 0)
            std_dev = 0.0
            if n >= 2:
                try:
                    std_dev = statistics.stdev(minutos)
                except Exception:
                    std_dev = 0.0
            set_readonly_val(widgets[4], f"{std_dev:.4f}")

            # Rango Mediciones: max(minutos) - min(minutos)
            rango = max(minutos) - min(minutos)
            set_readonly_val(widgets[6], f"{rango:.4f}")

            # Nº Obs. Necesarias
            sum_sq_min = sum(m**2 for m in minutos)
            obs_nec = 0.0
            if sum_min > 0:
                radicand = max(0.0, n * sum_sq_min - (sum_min ** 2))
                obs_nec = ((40.0 * math.sqrt(radicand)) / sum_min) ** 2
            set_readonly_val(widgets[5], f"{obs_nec:.2f}")

            # Tiempo Normal: sum(m * v for m, v in zip(minutos, valoraciones)) / (n * div)
            t_normal = sum(m * v for m, v in zip(minutos, valoraciones)) / (n * div)
            set_readonly_val(widgets[8], f"{t_normal:.4f}")

            # Tiempo Estándar: Tiempo Normal * (1 + suplemento)
            t_estandar = t_normal * (1.0 + suplemento)
            set_readonly_val(widgets[9], f"{t_estandar:.4f}")
            t_estandar_total += t_estandar

        # Paso 4: Actualización de Variables Globales del Footer en Cascada
        def set_readonly_entry_val(entry: tk.Entry, val: float) -> None:
            val_str = f"{val:.3f}" if val > 0.0 else "0.000"
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, val_str)
            entry.config(state="readonly")

        try:
            p_golpe = float(self.var_piezas_golpe.get().strip() or 1.0)
        except ValueError:
            p_golpe = 1.0

        try:
            a_golpe = float(self.var_articulos_golpe.get().strip() or 1.0)
        except ValueError:
            a_golpe = 1.0

        # NUEVO: Extraemos el número de operarios
        try:
            o_maq = float(self.var_operarios_maq.get().strip() or 1.0)
        except ValueError:
            o_maq = 1.0

        # Invocar la lógica de totalización en el Controlador
        metricas = self.controlador.calcular_metricas_globales(t_estandar_total, p_golpe, a_golpe)

        # Actualizar los widgets globales de forma segura
        set_readonly_entry_val(self.ent_tiempo_estandar_op, metricas["te_operacion"])
        set_readonly_entry_val(self.ent_cadencia_ph, metricas["cadencia_ph"])
        set_readonly_entry_val(self.ent_cadencia_h1000, metricas["cadencia_h1000"])
        set_readonly_entry_val(self.ent_estandar_epicor, metricas["estandar_epicor"])
        
        # FIX: La dotación es exactamente igual al número de operarios
        set_readonly_entry_val(self.ent_dotacion_epicor, o_maq)
    def ventana_finalizar(self) -> None:
        """Muestra popup con opciones de cierre, incluyendo persistencia en BD."""
        popup = tk.Toplevel(self)
        popup.title("Opciones de Cierre")
        centrar_ventana(popup, 350, 250)
        popup.grab_set()

        tk.Label(popup, text="¿Qué opción desea realizar?", font=("Arial", 11, "bold")).pack(pady=15)

        tk.Button(popup, text="Guardar en Base de Datos", bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), 
                  command=lambda: self.accion_guardar_bd(popup)).pack(fill="x", padx=40, pady=5)

        if not self.guardado_recientemente:
            tk.Button(popup, text="Guardar como PDF", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                      command=lambda: self.accion_guardar(popup)).pack(fill="x", padx=40, pady=5)

        tk.Button(popup, text="Salir sin guardar", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), 
                  command=lambda: self.accion_salir(popup)).pack(fill="x", padx=40, pady=5)

        tk.Button(popup, text="Cancelar", bg="gray", fg="white", font=("Arial", 10, "bold"), 
                  command=popup.destroy).pack(fill="x", padx=40, pady=5)

    def accion_guardar_bd(self, popup: tk.Toplevel) -> None:
        """Acción de guardar los datos del relevamiento en la BD."""
        popup.destroy()
        exito = self.guardar_en_bd()
        if exito:
            messagebox.showinfo("Éxito", "Relevamiento guardado exitosamente en la Base de Datos.")
            self.guardado_recientemente = True

    def guardar_en_bd(self) -> bool:
        """
        Valida, sanitiza e inserta/actualiza el cronometraje en la BD.
        Cumple estrictamente con la seguridad y casteo seguro (Regla 0 y Regla 7).
        """
        from tkinter import messagebox
        try:
            # 1. Recolección e intercepción de nulos (Strings)
            def str_or_none(val: str) -> Optional[str]:
                cleaned = val.strip()
                return cleaned if cleaned and cleaned.lower() != "none" else None

            art_codigo = str_or_none(self.entry_articulo_codigo.get())
            art_desc = str_or_none(self.entry_descripcion_articulo.get())
            operacion = str_or_none(self.combo_operacion.get())
            maquina = str_or_none(self.var_maquina.get())
            hm = str_or_none(self.var_hm.get())
            operario = str_or_none(self.var_operario.get())
            fecha_str = str_or_none(self.var_fecha.get())
            id_tarea_val = str_or_none(str(self.id_tarea_actual))
            
            if not art_codigo:
                messagebox.showwarning("Error de Validación", "El código de Artículo es obligatorio.")
                return False
            if not operacion:
                messagebox.showwarning("Error de Validación", "La Operación es obligatoria.")
                return False
                
            from dao import ArticuloDAO
            import datetime as dt
            from modelos import Relevamiento, TiemposElemento, Recurso, Operario
            
            # Obtener o crear artículo enviando codigo y descripcion como campos independientes
            articulo_obj = ArticuloDAO.obtener_o_crear(art_codigo, art_desc or art_codigo)
            
            # Delegamos la creación o búsqueda de recursos al DAO. Enviamos objetos de transporte.
            maquina_obj = Recurso(id_recurso="0", nombre=maquina, tipo="MAQUINA") if maquina else None
            hm_obj = Recurso(id_recurso="0", nombre=hm, tipo="HM") if hm else None
            operario_obj = Operario(id_operario="0", nombre=operario, legajo="") if operario else None
            
            try:
                fecha_obj = dt.datetime.strptime(fecha_str, "%d/%m/%Y").date() if fecha_str else dt.date.today()
            except ValueError:
                fecha_obj = dt.date.today()
                
            postura = "pie" if self.var_de_pie.get() else "sentado" if self.var_sentado.get() else "pie"
            
            # 2. Casteo Seguro de métricas globales (Regla de Nulos y Casteo)
            def safe_int_parse(val: str, field_name: str) -> int:
                val = val.strip()
                if not val or val.lower() == "none":
                    return 1
                try:
                    return int(float(val))
                except ValueError:
                    raise ValueError(f"El campo '{field_name}' debe ser un número entero. Valor ingresado: '{val}'")

            try:
                p_golpe = safe_int_parse(self.var_piezas_golpe.get(), "Piezas/Golpe")
                a_golpe = safe_int_parse(self.var_articulos_golpe.get(), "Artículos/Golpe")
                o_maq = safe_int_parse(self.var_operarios_maq.get(), "Operarios/Maq")
            except ValueError as ve:
                messagebox.showwarning("Error de Tipos", str(ve))
                return False
                
            relevamiento = Relevamiento(
                id_relevamiento=self.id_relevamiento_actual,
                id_tarea=int(id_tarea_val) if id_tarea_val else None,
                articulo=articulo_obj,
                operacion=operacion,
                recurso=maquina_obj,
                hm=hm_obj,
                operario=operario_obj,
                fecha=fecha_obj,
                postura=postura,
                piezas_por_golpe=p_golpe,
                articulos_por_golpe=a_golpe,
                operarios_maquina=o_maq,
                tiempos=[]
            )
            
            # 3. Recolectar y sanitizar tiempos de la grilla
            for b_idx in range(self.num_elementos):
                raw_nombre = str_or_none(self.nombres_elementos[b_idx].get())
                if not raw_nombre or raw_nombre.strip() == "Nombre Elemento":
                    nombre_el = f"Elemento {b_idx + 1}"
                else:
                    nombre_el = raw_nombre
                    
                for row_idx, fila in enumerate(self.matriz_bloques[b_idx]):
                    if row_idx >= self.max_filas:
                       continue
                       
                    val_v_str = str_or_none(fila[0].get())
                    val_min_str = str_or_none(fila[1].get())
                    val_raw_str = str_or_none(fila[2].get())
                    
                    if val_v_str or val_min_str or val_raw_str:
                        try:
                            # Valoración
                            v = 100.0
                            if val_v_str:
                                if val_v_str.endswith("%"):
                                    val_v_str = val_v_str[:-1].strip()
                                v = float(val_v_str)
                                
                            # Minutos y Segundos (Regla de extracción segura)
                            m = 0.0
                            if val_raw_str:
                                unit = "SEG"
                                try:
                                    unit = self.unidades_entrada[b_idx].get().strip()
                                except Exception:
                                    pass
                                raw_val = float(val_raw_str)
                                m = raw_val / 60.0 if unit == "SEG" else raw_val
                            elif val_min_str:
                                m = float(val_min_str)
                            
                            s = m * 60.0
                            
                            # Métricas inferiores
                            el_med_str = str_or_none(self.widgets_resultados_columnas[b_idx][1].get())
                            el_medidos = int(float(el_med_str)) if el_med_str else 1
                                
                            lote_str = str_or_none(self.widgets_resultados_columnas[b_idx][2].get())
                            lote_freq = float(lote_str) if lote_str else 1.0
                                
                            suple_str = str_or_none(self.widgets_resultados_columnas[b_idx][7].get())
                            suple = 0.0
                            if suple_str:
                                if suple_str.endswith("%"):
                                    suple_str = suple_str[:-1].strip()
                                suple = float(suple_str)
                                if suple > 1.0:
                                    suple = suple / 100.0
                            
                            relevamiento.tiempos.append(TiemposElemento(
                                elemento=nombre_el,
                                valoracion=v,
                                minutos=m,
                                segundos=s,
                                elementos_medidos=el_medidos,
                                lote_frecuencial=lote_freq,
                                suplemento=suple
                            ))
                        except ValueError as e:
                            messagebox.showwarning("Datos Inválidos en Grilla", f"Se encontró texto donde iba un número en la columna {b_idx + 1}, fila {row_idx + 1}.\nRevise los valores ingresados.")
                            return False
                            
            exito = self.controlador.guardar_relevamiento_bd(relevamiento)
            if exito:
                self.id_relevamiento_actual = relevamiento.id_relevamiento
                self.var_id_crono.set(f"AUTO-{relevamiento.id_relevamiento:03d}")
            return exito
        except Exception as e:
            logger.exception("Error en la fase de recolección de vista.")
            messagebox.showerror("Error Inesperado", f"Detalle técnico:\n{str(e)}")
            return False
    def cargar_datos_nuevos(self, id_tarea: int) -> None:
        """
        Limpia la vista y la vincula a una tarea nueva.
        """
        self.limpiar_datos()
        self.id_tarea_actual = id_tarea
        self.id_relevamiento_actual = None
        self.var_id_crono.set("AUTO-NUEVO")

    def cargar_datos(self, relevamiento: Any, id_tarea: int) -> None:
        """
        Carga toda la información de un relevamiento (cabecera + detalle)
        e inicializa el grid de tiempos de manera dinámica.
        """
        try:
            self.limpiar_datos()
            self.id_tarea_actual = id_tarea
            self.id_relevamiento_actual = relevamiento.id_relevamiento
            
            # Setear cabecera con sanitización de nulos - mapeo correcto codigo/descripcion
            if relevamiento.articulo:
                self.entry_articulo_codigo.delete(0, tk.END)
                art_codigo = str(relevamiento.articulo.codigo) if relevamiento.articulo.codigo else ""
                self.entry_articulo_codigo.insert(0, art_codigo)
                self.entry_descripcion_articulo.delete(0, tk.END)
                art_desc = str(relevamiento.articulo.descripcion) if relevamiento.articulo.descripcion else ""
                self.entry_descripcion_articulo.insert(0, art_desc)
                
            op_val = str(relevamiento.operacion) if relevamiento.operacion is not None else ""
            self.combo_operacion.set(op_val)
            
            if relevamiento.recurso:
                maq_val = str(relevamiento.recurso.nombre) if relevamiento.recurso.nombre is not None else ""
                self.var_maquina.set(maq_val)
            if relevamiento.hm:
                hm_val = str(relevamiento.hm.nombre) if relevamiento.hm.nombre is not None else ""
                self.var_hm.set(hm_val)
            if relevamiento.operario:
                op_nombre = str(relevamiento.operario.nombre) if relevamiento.operario.nombre is not None else ""
                self.var_operario.set(op_nombre)
                
            # Formatear fecha
            from datetime import date
            if relevamiento.fecha is not None:
                if isinstance(relevamiento.fecha, date):
                    self.var_fecha.set(relevamiento.fecha.strftime("%d/%m/%Y"))
                else:
                    self.var_fecha.set(str(relevamiento.fecha))
            else:
                self.var_fecha.set("")
                
            # Nº de Cronometraje: si es borrador nuevo (sin ID), obtener el siguiente correlativo de la BD
            # Nº de Cronometraje: Lógica de "Borrador Nuevo" o "Cargar Existente"
            if relevamiento.id_relevamiento is None:
                self.id_relevamiento_actual = None
                
                if hasattr(relevamiento, 'numero_importado') and relevamiento.numero_importado:
                    self.var_id_crono.set(relevamiento.numero_importado)
                else:
                    try:
                        next_id = self.controlador.obtener_siguiente_id_relevamiento()
                        self.var_id_crono.set(f"AUTO-{next_id:03d}")
                    except Exception:
                        self.var_id_crono.set("AUTO-NUEVO")
            else:
                self.id_relevamiento_actual = relevamiento.id_relevamiento
                self.var_id_crono.set(f"AUTO-{self.id_relevamiento_actual:03d}")
            
            # Postura
            postura_val = str(relevamiento.postura).lower() if relevamiento.postura is not None else "pie"
            if postura_val == "pie":
                self.var_de_pie.set(True)
                self.var_sentado.set(False)
            else:
                self.var_de_pie.set(False)
                self.var_sentado.set(True)
                
            # Footer
            piezas = str(relevamiento.piezas_por_golpe) if relevamiento.piezas_por_golpe is not None else "1"
            arts = str(relevamiento.articulos_por_golpe) if relevamiento.articulos_por_golpe is not None else "1"
            ops = str(relevamiento.operarios_maquina) if relevamiento.operarios_maquina is not None else "1"
            
            self.var_piezas_golpe.set(piezas)
            self.var_articulos_golpe.set(arts)
            self.var_operarios_maq.set(ops)
            
            # Reconstruir detalle de grilla
            from collections import OrderedDict
            tiempos_por_elemento = OrderedDict()
            if relevamiento.tiempos:
                for t in relevamiento.tiempos:
                    el_nombre = str(t.elemento) if t.elemento is not None else "Elemento"
                    if el_nombre not in tiempos_por_elemento:
                        tiempos_por_elemento[el_nombre] = []
                    tiempos_por_elemento[el_nombre].append(t)
                
            if not tiempos_por_elemento:
                return
                
            # Obtener el número máximo de observaciones para inicializar la grilla
            max_obs = max(len(t_list) for t_list in tiempos_por_elemento.values())
            if max_obs < 10:
                max_obs = 10  # Mantener mínimo de 10 filas para estética
                
            # Agregar columnas dinámicas
            for elem_nombre, t_list in tiempos_por_elemento.items():
                self.agregar_elemento_dinamico(max_obs)
                col_idx = self.num_elementos - 1
                
                # Poner nombre del elemento
                self.nombres_elementos[col_idx].delete(0, tk.END)
                self.nombres_elementos[col_idx].insert(0, elem_nombre)
                self.nombres_elementos[col_idx].config(fg="black")
                
                # Poner observaciones
                for row_idx, t in enumerate(t_list):
                    fila_widgets = self.matriz_bloques[col_idx][row_idx]
                    
                    # Valoración sanitizada
                    val_v = ""
                    if t.valoracion is not None:
                        val_v = f"{t.valoracion:.0f}%" if t.valoracion.is_integer() else f"{t.valoracion}%"
                        
                    fila_widgets[0].delete(0, tk.END)
                    fila_widgets[0].insert(0, val_v)
                    
                    # Minutos -> celda MIN (readonly, index 1)
                    val_m = ""
                    if t.minutos is not None and t.minutos > 0.0:
                        val_m = f"{t.minutos:.4f}"
                        
                    fila_widgets[1].config(state="normal")
                    fila_widgets[1].delete(0, tk.END)
                    fila_widgets[1].insert(0, val_m)
                    fila_widgets[1].config(state="readonly")
                    
                    # Segundos -> celda RAW (editable, index 2) para recuperar el número original
                    val_s = ""
                    if t.segundos is not None and t.segundos > 0.0:
                        val_s = f"{t.segundos:.2f}"
                    
                    fila_widgets[2].delete(0, tk.END)
                    fila_widgets[2].insert(0, val_s)
                
                # Poner métricas inferiores de la columna
                first_t = t_list[0]
                
                # Elementos medidos
                self.widgets_resultados_columnas[col_idx][1].config(state="normal")
                self.widgets_resultados_columnas[col_idx][1].delete(0, tk.END)
                el_med = str(first_t.elementos_medidos) if first_t.elementos_medidos is not None else "1"
                self.widgets_resultados_columnas[col_idx][1].insert(0, el_med)
                
                # Lote frecuencial
                self.widgets_resultados_columnas[col_idx][2].config(state="normal")
                self.widgets_resultados_columnas[col_idx][2].delete(0, tk.END)
                lote_f = str(first_t.lote_frecuencial) if first_t.lote_frecuencial is not None else "1.0"
                self.widgets_resultados_columnas[col_idx][2].insert(0, lote_f)
                
                # Suplemento
                self.widgets_resultados_columnas[col_idx][7].config(state="normal")
                self.widgets_resultados_columnas[col_idx][7].delete(0, tk.END)
                suple_str = ""
                if first_t.suplemento is not None:
                    suple_val = first_t.suplemento
                    if suple_val <= 1.0 and suple_val > 0.0:
                        suple_val = suple_val * 100
                    suple_str = f"{suple_val:.0f}" if suple_val.is_integer() else f"{suple_val}"
                self.widgets_resultados_columnas[col_idx][7].insert(0, suple_str)
                
            # Actualizar conteo de filas cargadas para cada columna
            for b_idx in range(self.num_elementos):
                self.actualizar_conteo(b_idx)
                
            # Ejecutar el motor de cálculo en tiempo real
            self.recalcular_todo()
            self.guardado_recientemente = True
            
        except Exception as e:
            logger.exception("Error poblando la interfaz")
            from tkinter import messagebox
            messagebox.showerror("Error al Cargar", f"Falló el renderizado de la interfaz:\n{str(e)}")

    def obtener_datos_limpios(self) -> Dict[str, Any]:
        """
        Extrae la totalidad de los datos de la planilla para generar un PDF tipo 'snapshot'.

        Retorna un diccionario integral con tres secciones:
        - 'cabecera': datos de artículo, operación, máquina, operario, etc.
        - 'elementos': lista de diccionarios, cada uno con nombre, observaciones y resultados.
        - 'footer': métricas globales (piezas/golpe, TE operación, cadencias, Epicor).

        Returns:
            Dict[str, Any]: Diccionario con toda la información visible en la UI.
        """
        # --- CABECERA COMPLETA ---
        cabecera: Dict[str, str] = {
            "articulo_codigo": self.entry_articulo_codigo.get().strip() or "S/C",
            "articulo_descripcion": self.entry_descripcion_articulo.get().strip() or "Sin Descripción",
            "operacion": self.combo_operacion.get().strip() or "S/O",
            "maquina": self.var_maquina.get().strip() or "S/M",
            "herramienta": self.var_hm.get().strip() or "S/H",
            "operario": self.var_operario.get().strip() or "S/OP",
            "fecha": self.var_fecha.get().strip() or "S/F",
            "postura": "Pie" if self.var_de_pie.get() else "Sentado" if self.var_sentado.get() else "N/A",
            "id_crono": self.var_id_crono.get().strip() or "N/A",
        }

        # --- ELEMENTOS (Observaciones + Resultados Estadísticos) ---
        elementos: List[Dict[str, Any]] = []
        for b_idx in range(self.num_elementos):
            nombre = self.nombres_elementos[b_idx].get().strip()
            if nombre == "Nombre Elemento" or not nombre:
                nombre = f"Elemento {b_idx + 1}"

            # Observaciones: V, MIN, RAW de cada fila activa
            observaciones: List[Dict[str, str]] = []
            for row_idx, fila in enumerate(self.matriz_bloques[b_idx]):
                if row_idx >= self.max_filas:
                    continue
                v_str = fila[0].get().strip()
                min_str = fila[1].get().strip()
                raw_str = fila[2].get().strip()

                if v_str or min_str or raw_str:
                    observaciones.append({
                        "valoracion": v_str or "-",
                        "min": min_str or "-",
                        "raw": raw_str or "-",
                    })

            # Resultados: los 10 widgets de widgets_resultados_columnas
            widgets = self.widgets_resultados_columnas[b_idx]
            # Mapeo posicional: [0]=Nº Obs(Label), [1]=Elem Med, [2]=Lote Frec,
            # [3]=T.MEDIO, [4]=Desvío, [5]=Obs Nec, [6]=Rango,
            # [7]=Suplemento, [8]=T.Normal, [9]=T.Estándar
            def _extraer_valor_widget(widget: Any) -> str:
                """Extrae texto de un widget tk (Entry o Label con StringVar)."""
                try:
                    if isinstance(widget, tk.Label):
                        # Labels usan cget('text') o textvariable
                        var = widget.cget("textvariable")
                        if var:
                            return widget.getvar(var)
                        return widget.cget("text")
                    # Entry (normal o readonly)
                    return widget.get().strip()
                except Exception:
                    return ""

            resultados: Dict[str, str] = {
                "n_observaciones": _extraer_valor_widget(widgets[0]),
                "elementos_medidos": _extraer_valor_widget(widgets[1]),
                "lote_frecuencial": _extraer_valor_widget(widgets[2]),
                "tiempo_medio": _extraer_valor_widget(widgets[3]),
                "desvio_estandar": _extraer_valor_widget(widgets[4]),
                "obs_necesarias": _extraer_valor_widget(widgets[5]),
                "rango": _extraer_valor_widget(widgets[6]),
                "suplemento": _extraer_valor_widget(widgets[7]),
                "tiempo_normal": _extraer_valor_widget(widgets[8]),
                "tiempo_estandar": _extraer_valor_widget(widgets[9]),
            }

            elementos.append({
                "nombre": nombre,
                "observaciones": observaciones,
                "resultados": resultados,
            })

        # --- FOOTER COMPLETO (Métricas Globales + Epicor) ---
        footer: Dict[str, str] = {
            "piezas_por_golpe": self.var_piezas_golpe.get().strip() or "1",
            "articulos_por_golpe": self.var_articulos_golpe.get().strip() or "1",
            "operarios_maquina": self.var_operarios_maq.get().strip() or "1",
            "te_operacion": self.var_tiempo_estandar_op.get().strip() or "0.000",
            "cadencia_ph": self.var_cadencia_ph.get().strip() or "0.000",
            "cadencia_h1000": self.var_cadencia_h1000.get().strip() or "0.000",
            "estandar_epicor": self.var_estandar_epicor.get().strip() or "0.000",
            "dotacion_epicor": self.var_dotacion_epicor.get().strip() or "0.000",
        }

        return {
            "cabecera": cabecera,
            "elementos": elementos,
            "footer": footer,
        }

    def _mover_foco_abajo(self, event, b_idx: int, row_idx: int, c_idx: int) -> None:
        if row_idx + 1 < self.max_filas:
            siguiente = self.matriz_bloques[b_idx][row_idx + 1][c_idx]
            if siguiente.cget("state") == "normal":
                siguiente.focus_set()


class PaginaBuscadorHistorico(tk.Frame):
    """
    Vista del Buscador Histórico de relevamientos con filtros tipo Excel.

    Permite a los responsables de planta buscar cronometrajes pasados
    haciendo clic en los encabezados de columna para activar Comboboxes
    flotantes con valores únicos extraídos de los datos actuales.

    El ID de la base de datos se oculta del usuario; se usa internamente
    como iid del Treeview. El Código del Artículo es el identificador visual.

    Attributes:
        controlador: Instancia del controlador MVC principal.
        tree: Treeview con los resultados de la búsqueda.
        filtros_activos: Diccionario con los filtros aplicados actualmente.
        _combo_flotante: Referencia al Combobox flotante activo (o None).
        _nombres_originales: Nombres base de cada columna (sin íconos de filtro).
    """

    # Mapeo: nombre columna visible -> clave de filtro en el DAO
    _COL_A_FILTRO: Dict[str, str] = {
        "Artículo": "articulo",
        "Operación": "operacion",
        "Máquina": "maquina",
        "HM": "hm",
        "Operario": "operario",
    }

    # Columnas que NO permiten filtrado por clic en header
    _COLUMNAS_SIN_FILTRO: tuple = ("Fecha",)

    def __init__(self, parent: tk.Widget, controlador: Any) -> None:
        """
        Inicializa la vista del Buscador Histórico.

        Args:
            parent: Widget padre (contenedor de frames de la aplicación).
            controlador: Instancia del Controlador MVC.
        """
        super().__init__(parent, bg="#ecf0f1")
        self.controlador = controlador

        # Estado interno de filtros activos
        self.filtros_activos: Dict[str, str] = {}
        self._combo_flotante: Optional[ttk.Combobox] = None

        # Nombres base de cada columna (sin ícono de filtro)
        self._nombres_originales: Dict[str, str] = {}

        # ═══════════════════════════════════════════════════════════════
        # PANEL SUPERIOR — Título
        # ═══════════════════════════════════════════════════════════════
        panel_titulo = tk.Frame(self, bg="#2c3e50")
        panel_titulo.pack(side="top", fill="x")
        tk.Label(
            panel_titulo, text="Buscador Histórico de Relevamientos",
            font=("Arial", 14, "bold"), bg="#2c3e50", fg="white"
        ).pack(pady=10)

        # Barra de instrucción sutil
        barra_instruccion = tk.Frame(self, bg="#dfe6e9")
        barra_instruccion.pack(side="top", fill="x", padx=15, pady=(5, 0))
        tk.Label(
            barra_instruccion,
            text="💡 Haga clic en los encabezados de columna para filtrar",
            font=("Arial", 9, "italic"), bg="#dfe6e9", fg="#636e72"
        ).pack(side="left", padx=10, pady=4)

        # Indicador de resultados (lado derecho de la barra de instrucción)
        self.var_resultado_info = tk.StringVar(value="")
        tk.Label(
            barra_instruccion, textvariable=self.var_resultado_info,
            font=("Arial", 9, "bold"), bg="#dfe6e9", fg="#2c3e50"
        ).pack(side="right", padx=10, pady=4)

        # ═══════════════════════════════════════════════════════════════
        # PANEL CENTRAL — Treeview con resultados
        # ═══════════════════════════════════════════════════════════════
        self.panel_grilla = tk.Frame(self, bg="white")
        self.panel_grilla.pack(side="top", fill="both", expand=True, padx=15, pady=5)

        # Todas las columnas internas (ID oculta)
        todas_columnas: tuple = ("ID", "Fecha", "Artículo", "Operación", "Máquina", "HM", "Operario")
        # Columnas visibles para el usuario (sin ID)
        columnas_visibles: tuple = ("Fecha", "Artículo", "Operación", "Máquina", "HM", "Operario")

        self.tree = ttk.Treeview(
            self.panel_grilla, columns=todas_columnas, show="headings",
            selectmode="browse", displaycolumns=columnas_visibles
        )

        # Configuración de columnas
        anchos: Dict[str, int] = {
            "ID": 0, "Fecha": 110, "Artículo": 160,
            "Operación": 160, "Máquina": 160, "HM": 130, "Operario": 160,
        }
        for col in todas_columnas:
            self.tree.heading(col, text=col, anchor="center")
            ancho = anchos.get(col, 120)
            anchor = "center" if col == "Fecha" else "w"
            self.tree.column(col, width=ancho, anchor=anchor, minwidth=50)
            # Guardar nombres originales para restaurar tras limpiar filtros
            self._nombres_originales[col] = col

        # Columna ID con ancho 0 (oculta vía displaycolumns, refuerzo visual)
        self.tree.column("ID", width=0, stretch=False, minwidth=0)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.panel_grilla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.panel_grilla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.panel_grilla.columnconfigure(0, weight=1)
        self.panel_grilla.rowconfigure(0, weight=1)

        # Eventos
        self.tree.bind("<Double-1>", self._on_doble_clic)
        self.tree.bind("<Button-1>", self._on_header_click)

        # ═══════════════════════════════════════════════════════════════
        # PANEL INFERIOR — Botones de acción
        # ═══════════════════════════════════════════════════════════════
        panel_inferior = tk.Frame(self, bg="#ecf0f1")
        panel_inferior.pack(side="bottom", fill="x", padx=15, pady=10)

        tk.Button(
            panel_inferior, text="📂 Cargar Relevamiento", bg="#34495e", fg="white",
            font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2",
            command=self._cargar_seleccionado
        ).pack(side="right", padx=5)

        self.btn_limpiar = tk.Button(
            panel_inferior, text="🧹 Limpiar Filtros", bg="#34495e", fg="white",
            font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2",
            command=self._limpiar_filtros
        )
        self.btn_limpiar.pack(side="right", padx=5)

        # Botón "Borrar Planilla" — RBAC: solo visible para JEFE/GERENTE
        self.btn_borrar = tk.Button(
            panel_inferior, text="🗑 Borrar Planilla", bg="#34495e", fg="white",
            font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2",
            command=self._borrar_seleccionado
        )

        tk.Button(
            panel_inferior, text="↩ Volver al Home", bg="#34495e", fg="white",
            font=("Arial", 10, "bold"), relief="groove", bd=2, cursor="hand2",
            command=lambda: self.controlador.root.mostrar_frame(PaginaTareas)
        ).pack(side="left", padx=5)

    # ═══════════════════════════════════════════════════════════════════
    # FILTROS TIPO EXCEL — Combobox Flotante sobre Encabezados
    # ═══════════════════════════════════════════════════════════════════

    def _on_header_click(self, event: Any) -> None:
        """
        Intercepta clics en la zona de encabezados del Treeview.

        Usa identify_region para verificar que el clic fue en 'heading'.
        Usa identify_column para determinar qué columna fue clickeada.
        Si la columna admite filtrado, despliega un Combobox flotante
        con los valores únicos actuales de esa columna.

        Args:
            event: Evento de Tkinter con coordenadas x, y del clic.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region != "heading":
            return

        # Destruir Combobox flotante previo si existe
        self._destruir_combo_flotante()

        # Obtener el índice de columna clickeada (formato "#N")
        col_id_raw: str = self.tree.identify_column(event.x)
        try:
            # col_id_raw es "#1", "#2", etc. — índice 1-based sobre displaycolumns
            col_display_idx: int = int(col_id_raw.replace("#", "")) - 1
        except ValueError:
            return

        # Mapear índice de displaycolumns al nombre real de la columna
        displaycolumns = self.tree.cget("displaycolumns")
        if isinstance(displaycolumns, str):
            displaycolumns = self.tree.configure("displaycolumns")[4]
            if isinstance(displaycolumns, str):
                displaycolumns = displaycolumns.split()

        if col_display_idx < 0 or col_display_idx >= len(displaycolumns):
            return

        col_name: str = displaycolumns[col_display_idx]

        # No filtrar columnas excluidas
        if col_name in self._COLUMNAS_SIN_FILTRO:
            return

        # No filtrar columnas sin mapeo
        if col_name not in self._COL_A_FILTRO:
            return

        # Extraer valores únicos de la columna desde los datos actuales del Treeview
        valores_unicos: List[str] = sorted({
            str(self.tree.set(child, col_name))
            for child in self.tree.get_children()
            if self.tree.set(child, col_name).strip()
        })

        # Agregar opción vacía al inicio para "sin filtro"
        opciones: List[str] = ["(Todos)"] + valores_unicos

        # ─── Geometría: posicionar Combobox sobre el encabezado ───
        tree_x: int = self.tree.winfo_x()
        tree_y: int = self.tree.winfo_y()

        # Calcular x offset iterando sobre las columnas anteriores visibles
        x_offset: int = 0
        for i in range(col_display_idx):
            prev_col = displaycolumns[i]
            col_width = self.tree.column(prev_col, "width")
            x_offset += col_width

        col_width: int = self.tree.column(col_name, "width")
        header_height: int = 26  # Altura típica del heading en ttk.Treeview

        combo_x: int = tree_x + x_offset
        combo_y: int = tree_y
        combo_w: int = col_width

        # Crear Combobox flotante dentro del panel_grilla
        self._combo_flotante = ttk.Combobox(
            self.panel_grilla, values=opciones, font=("Arial", 9),
            state="normal"  # Permite tipeo libre + selección
        )
        self._combo_flotante.place(x=combo_x, y=combo_y, width=combo_w, height=header_height)

        # Inyectar filtro actual si existe
        clave_filtro: str = self._COL_A_FILTRO[col_name]
        filtro_actual: str = self.filtros_activos.get(clave_filtro, "")
        if filtro_actual:
            self._combo_flotante.set(filtro_actual)
        else:
            self._combo_flotante.set("")

        self._combo_flotante.focus_set()
        self._combo_flotante.event_generate("<Button-1>")

        # ─── Bindings del Combobox flotante ───
        def aplicar_filtro(e: Any = None) -> None:
            """Aplica el valor seleccionado/escrito como filtro y refresca."""
            if self._combo_flotante is None:
                return
            valor: str = self._combo_flotante.get().strip()
            self._destruir_combo_flotante()

            if valor == "(Todos)" or valor == "":
                # Remover filtro para esta columna
                self.filtros_activos.pop(clave_filtro, None)
                self.tree.heading(col_name, text=self._nombres_originales[col_name])
            else:
                # Aplicar filtro
                self.filtros_activos[clave_filtro] = valor
                self.tree.heading(col_name, text=f"🔍 {self._nombres_originales[col_name]}")

            self._ejecutar_busqueda()

        def cancelar(e: Any = None) -> None:
            """Destruye el Combobox sin aplicar cambios."""
            self._destruir_combo_flotante()

        self._combo_flotante.bind("<Return>", aplicar_filtro)
        self._combo_flotante.bind("<<ComboboxSelected>>", aplicar_filtro)
        self._combo_flotante.bind("<Escape>", cancelar)
        self._combo_flotante.bind("<FocusOut>", cancelar)

    def _destruir_combo_flotante(self) -> None:
        """
        Destruye el Combobox flotante activo si existe.
        Manejo seguro para evitar errores si ya fue destruido.
        """
        if self._combo_flotante is not None:
            try:
                self._combo_flotante.destroy()
            except tk.TclError:
                pass
            self._combo_flotante = None

    # ═══════════════════════════════════════════════════════════════════
    # Lógica de Búsqueda y Población de Datos
    # ═══════════════════════════════════════════════════════════════════

    def _construir_filtros(self) -> Dict[str, str]:
        """
        Construye el diccionario de filtros a partir de self.filtros_activos.

        Returns:
            Diccionario con las claves de filtro y sus valores actuales.
        """
        return dict(self.filtros_activos)

    def _ejecutar_busqueda(self) -> None:
        """
        Ejecuta la búsqueda histórica delegando al controlador y puebla la grilla.
        """
        filtros: Dict[str, str] = self._construir_filtros()
        try:
            resultados: List[tuple] = self.controlador.buscar_relevamientos_historicos(filtros)
            self._poblar_grilla(resultados)
            # Actualizar indicador de resultados
            n: int = len(resultados)
            n_filtros: int = len(self.filtros_activos)
            texto: str = f"{n} resultado{'s' if n != 1 else ''}"
            if n_filtros > 0:
                texto += f" | {n_filtros} filtro{'s' if n_filtros != 1 else ''} activo{'s' if n_filtros != 1 else ''}"
            self.var_resultado_info.set(texto)
        except Exception:
            logger.exception("Error al ejecutar búsqueda histórica desde la vista.")
            messagebox.showerror(
                "Error de Búsqueda",
                "Ocurrió un error al buscar los relevamientos históricos.\nRevise el log del sistema."
            )

    def _poblar_grilla(self, resultados: List[tuple]) -> None:
        """
        Limpia y vuelve a cargar el Treeview con los resultados provistos.

        El id_relevamiento (índice 0) se almacena como iid para uso interno
        pero no es visible al usuario gracias a displaycolumns.

        Args:
            resultados: Lista de tuplas
                (id_relevamiento, fecha, codigo_articulo, operacion, maquina, hm, operario).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for fila in resultados:
            # iid = id_relevamiento (índice 0), values incluye TODAS las columnas
            self.tree.insert(
                "", "end", iid=str(fila[0]),
                values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])
            )

    def _limpiar_filtros(self) -> None:
        """
        Limpia todos los filtros activos, restaura los encabezados originales
        y recarga la grilla sin filtros.
        """
        self.filtros_activos.clear()
        self._destruir_combo_flotante()

        # Restaurar textos originales de todos los encabezados
        for col_name, nombre_original in self._nombres_originales.items():
            self.tree.heading(col_name, text=nombre_original)

        self.var_resultado_info.set("")
        self._ejecutar_busqueda()

    # ═══════════════════════════════════════════════════════════════════
    # Acciones de Selección y Carga
    # ═══════════════════════════════════════════════════════════════════

    def _cargar_seleccionado(self) -> None:
        """
        Captura el ID del relevamiento seleccionado en la grilla (almacenado
        como iid) y lo abre en la vista Plantilla mediante el controlador.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Sin selección",
                "Debe seleccionar un relevamiento de la grilla para cargarlo."
            )
            return
        try:
            id_rel: int = int(seleccion[0])
            self.controlador.abrir_relevamiento_desde_id(id_rel)
        except ValueError:
            logger.exception("El ID seleccionado no es un entero válido.")
            messagebox.showerror("Error", "El ID seleccionado no es válido.")
        except Exception:
            logger.exception("Error al intentar cargar el relevamiento seleccionado.")
            messagebox.showerror(
                "Error",
                "No se pudo cargar el relevamiento seleccionado.\nRevise el log del sistema."
            )

    def _borrar_seleccionado(self) -> None:
        """
        Elimina físicamente el relevamiento seleccionado de la base de datos.

        Extrae el ID del Treeview (almacenado como iid), pide confirmación,
        delega al controlador y recarga la grilla tras la eliminación.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Sin selección",
                "Debe seleccionar un relevamiento de la grilla para eliminarlo."
            )
            return
        try:
            id_rel: int = int(seleccion[0])
        except ValueError:
            logger.exception("El ID seleccionado no es un entero válido para borrado.")
            messagebox.showerror("Error", "El ID seleccionado no es válido.")
            return

        confirmado = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar PERMANENTEMENTE el relevamiento ID {id_rel}?\n\n"
            f"Esta acción no se puede deshacer."
        )
        if not confirmado:
            return

        exito = self.controlador.borrar_relevamiento(id_rel)
        if exito:
            messagebox.showinfo("Éxito", f"Relevamiento {id_rel} eliminado correctamente.")
            self._ejecutar_busqueda()
        else:
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el relevamiento {id_rel}.\nRevise el log del sistema."
            )

    def _on_doble_clic(self, event: Any) -> None:
        """
        Manejador del evento <Double-1> sobre la grilla.
        Ejecuta la misma acción que el botón 'Cargar Relevamiento'.
        Solo actúa si el doble clic fue en la zona de celdas (no en heading).

        Args:
            event: Evento de Tkinter con coordenadas del clic.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            return  # Evitar conflicto con _on_header_click
        self._cargar_seleccionado()

    # ═══════════════════════════════════════════════════════════════════
    # Método Público (Interfaz MVC)
    # ═══════════════════════════════════════════════════════════════════

    def actualizar_vista(self) -> None:
        """
        Limpia la UI completa: resetea filtros activos, restaura encabezados
        originales y carga todos los registros por defecto (filtros vacíos).
        Se invoca automáticamente al mostrar el frame vía mostrar_frame().
        """
        self.filtros_activos.clear()
        self._destruir_combo_flotante()

        for col_name, nombre_original in self._nombres_originales.items():
            self.tree.heading(col_name, text=nombre_original)

        self.var_resultado_info.set("")
        self._ejecutar_busqueda()

        # RBAC: Mostrar u ocultar el botón "Borrar Planilla" según el rol
        usuario = self.controlador.usuario_actual
        if usuario and usuario.rol == "JEFE/GERENTE":
            self.btn_borrar.pack(side="right", padx=5, before=self.btn_limpiar)
        else:
            self.btn_borrar.pack_forget()


class PaginaManual(tk.Frame):
    """
    Pantalla integrada de solo lectura con el Manual de Usuario completo.

    Se renderiza como un tk.Frame dentro del contenedor principal de la
    aplicación (no como Toplevel), permitiendo navegación estándar vía
    mostrar_frame(). El contenido se inyecta en un tk.Text con tags de
    estilo y se bloquea con state='disabled'.

    El botón "Volver" evalúa dinámicamente si el usuario está autenticado:
    si no hay sesión activa, regresa a PaginaLogin; si hay sesión,
    regresa a PaginaTareas.

    Attributes:
        controlador: Referencia al Controlador MVC.
        texto: Widget tk.Text de solo lectura con el contenido del manual.
    """

    def __init__(self, parent: tk.Widget, controlador: Any) -> None:
        """
        Inicializa el frame del Manual de Usuario.

        Configura el fondo blanco, crea el título, el widget tk.Text
        con scrollbar vertical, inyecta todo el contenido formateado
        y lo bloquea en modo solo lectura.

        Args:
            parent: Widget contenedor padre (self.contenedor de Aplicacion).
            controlador: Instancia del Controlador MVC.
        """
        super().__init__(parent, bg="white")
        self.controlador = controlador

        # --- Título superior ---
        tk.Label(
            self, text="Manual de Usuario — Métodos y Tiempos",
            font=("Arial", 16, "bold"), bg="white", fg="#2c3e50"
        ).pack(side="top", pady=(15, 5))

        # --- Botón Volver (parte inferior) ---
        tk.Button(
            self, text="Volver",
            font=("Arial", 10, "bold"), bg="#34495e", fg="white",
            relief="groove", bd=2, cursor="hand2",
            command=self._volver
        ).pack(side="bottom", pady=(5, 15))

        # --- Contenedor de Text + Scrollbar ---
        frame_contenido = tk.Frame(self, bg="white")
        frame_contenido.pack(fill="both", expand=True, padx=15, pady=(5, 5))

        scrollbar = tk.Scrollbar(frame_contenido, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.texto = tk.Text(
            frame_contenido,
            wrap="word",
            font=("Arial", 10),
            bg="white",
            fg="#2c3e50",
            padx=15,
            pady=15,
            spacing1=2,
            spacing3=2,
            yscrollcommand=scrollbar.set,
        )
        self.texto.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.texto.yview)

        # --- Tags de estilo ---
        self.texto.tag_configure("titulo", font=("Arial", 16, "bold"), foreground="#2c3e50", spacing1=10, spacing3=6)
        self.texto.tag_configure("subtitulo", font=("Arial", 13, "bold"), foreground="#34495e", spacing1=8, spacing3=4)
        self.texto.tag_configure("seccion", font=("Arial", 11, "bold"), foreground="#2980b9", spacing1=6, spacing3=3)
        self.texto.tag_configure("negrita", font=("Arial", 10, "bold"))
        self.texto.tag_configure("normal", font=("Arial", 10))
        self.texto.tag_configure("item", font=("Arial", 10), lmargin1=30, lmargin2=45)
        self.texto.tag_configure("separador", font=("Arial", 6), foreground="#bdc3c7")
        self.texto.tag_configure("nota", font=("Arial", 9, "italic"), foreground="#7f8c8d", lmargin1=20, lmargin2=20)
        self.texto.tag_configure("tabla_head", font=("Arial", 10, "bold"), foreground="#2c3e50", background="#ecf0f1")
        self.texto.tag_configure("tabla_row", font=("Consolas", 9), lmargin1=15, lmargin2=15)

        # --- Inyectar contenido ---
        self._insertar_contenido()
        
        self.texto.config(state="normal")
        self.texto.insert(tk.END, """
--------------------------------------------------
6. RECUPERACIÓN DE USUARIO Y CONTRASEÑA
--------------------------------------------------
En caso de olvidar sus credenciales de acceso, el sistema permite generar una nueva contraseña de forma segura.

Pasos para restablecer sus datos:
1. En la pantalla principal de Inicio de Sesión (Login), haga clic en el enlace inferior que dice "¿Olvidó su usuario/contraseña?".
2. Se abrirá una ventana de seguridad. Complete los siguientes campos:
   - Su Nombre Completo: Ingrese su nombre tal cual fue registrado en el sistema.
   - Nueva Contraseña: Cree su nueva clave (solo letras y números, máximo 30 caracteres).
   - Clave Maestra de Autorización: Ingrese la clave de seguridad provista por la Gerencia.
3. Haga clic en el botón "Restablecer Credenciales".
4. Si los datos son correctos, el sistema le mostrará un mensaje de éxito recordándole cuál es su Nombre de Usuario y confirmando el cambio de contraseña.
""")
        self.texto.config(state="disabled")

    def _volver(self) -> None:
        """
        Navega de vuelta a la pantalla correspondiente según el estado de sesión.

        Si no hay usuario autenticado (acceso desde Login), regresa a
        PaginaLogin. Si hay sesión activa, regresa a PaginaTareas.
        """
        if self.controlador.usuario_actual is None:
            self.controlador.root.mostrar_frame(PaginaLogin)
        else:
            self.controlador.root.mostrar_frame(PaginaTareas)

    def _ins(self, contenido: str, tag: str = "normal") -> None:
        """
        Helper interno para insertar una línea con tag en el widget Text.

        Args:
            contenido: Texto a insertar.
            tag: Nombre del tag de estilo a aplicar.
        """
        self.texto.insert("end", contenido + "\n", tag)

    def _sep(self) -> None:
        """Inserta una línea separadora horizontal decorativa."""
        self.texto.insert("end", "\u2501" * 80 + "\n", "separador")

    def _insertar_contenido(self) -> None:
        """
        Inyecta el contenido completo del Manual de Usuario en el widget Text.

        Utiliza los helpers _ins y _sep para insertar secciones con formato.
        El contenido cubre: Introducción, Dashboard, Cronometraje, Buscador
        Histórico, Copia de Seguridad (Backup), Barra de Menú y Glosario
        de Términos.
        """
        ins = self._ins
        sep = self._sep

        ins("MANUAL DE USUARIO \u2014 MÉTODOS Y TIEMPOS", "titulo")
        ins("Versión Beta 0.15  \u00b7  Junio 2026", "nota")
        ins("Audiencia: Metodistas \u00b7 Jefes/Gerentes de Planta", "nota")
        sep()

        # --- SECCION 1 ---
        ins("1. INTRODUCCIÓN Y ACCESO AL SISTEMA", "subtitulo")
        sep()

        ins("1.1 ¿Qué es Métodos y Tiempos?", "seccion")
        ins("Métodos y Tiempos es un software de escritorio diseñado para la gestión integral "
            "de estudios de cronometraje industrial. Permite a los equipos de Ingeniería de Métodos:")
        ins("  \u2022  Crear y gestionar plantillas de cronometraje con múltiples elementos.", "item")
        ins("  \u2022  Registrar tiempos, valoraciones y suplementos de forma dinámica.", "item")
        ins("  \u2022  Calcular automáticamente métricas industriales (Tiempo Estándar, Cadencia, Epicor).", "item")
        ins("  \u2022  Persistir los relevamientos en base de datos centralizada (SQL Server).", "item")
        ins("  \u2022  Exportar informes en formato PDF.", "item")
        ins("  \u2022  Buscar y consultar el historial de todos los estudios realizados.", "item")
        ins("")

        ins("1.2 Roles del Sistema", "seccion")
        ins("El sistema implementa Control de Acceso Basado en Roles (RBAC) con dos perfiles:")
        ins("")
        ins("  METODISTA                              JEFE/GERENTE", "tabla_head")
        ins("  Ver Dashboard: Solo tareas asignadas   Ver Dashboard: Todas las tareas", "tabla_row")
        ins("  Realizar cronometrajes: SI             Realizar cronometrajes: NO", "tabla_row")
        ins("  Crear nuevas tareas: NO                Crear nuevas tareas: SI", "tabla_row")
        ins("  Borrar tareas: NO                      Borrar tareas: SI", "tabla_row")
        ins("  Cambiar estado a Cerrado: NO           Cambiar estado a Cerrado: SI", "tabla_row")
        ins("  Borrar planillas historicas: NO         Borrar planillas historicas: SI", "tabla_row")
        ins("  Buscar relevamientos: SI               Buscar relevamientos: SI", "tabla_row")
        ins("")

        ins("1.3 Pantalla de Inicio de Sesión (Login)", "seccion")
        ins("Al abrir la aplicación se presenta la pantalla de Inicio de Sesión. "
            "Esta pantalla bloquea el acceso a todas las funcionalidades hasta autenticarse.")
        ins("")
        ins("Campos del formulario:", "negrita")
        ins("  \u2022  Usuario: Ingrese su nombre de usuario registrado.", "item")
        ins("  \u2022  Contraseña: Los caracteres se muestran ocultos por seguridad.", "item")
        ins("")
        ins("Botones disponibles:", "negrita")
        ins("  \u2022  Ingresar: Valida credenciales. Si son correctas, redirige al Dashboard.", "item")
        ins("  \u2022  Crear usuario: Redirige a la pantalla de Registro.", "item")
        ins("")
        ins("Cada inicio y cierre de sesión queda registrado en el sistema de auditoría.", "nota")
        ins("")

        ins("1.4 Registro de Nuevos Usuarios", "seccion")
        ins("La pantalla de Registro permite dar de alta nuevas cuentas con los campos:")
        ins("  \u2022  Nombre Completo: Nombre real del usuario.", "item")
        ins("  \u2022  Nombre de Usuario (Username): Identificador único para el login.", "item")
        ins("  \u2022  Rol del Sistema: METODISTA o JEFE/GERENTE.", "item")
        ins("  \u2022  Contraseña: Clave de acceso personal (se almacena cifrada).", "item")
        ins("")
        ins("Si se selecciona JEFE/GERENTE, el sistema solicitará una Contraseña Maestra "
            "de autorización para prevenir escalada de privilegios.", "nota")
        ins("")

        ins("1.5 Cerrar Sesión", "seccion")
        ins("Desde el menú superior: Archivo \u2192 Cerrar Sesión. "
            "Limpia la sesión activa y devuelve a la pantalla de Login.")
        sep()

        # --- SECCION 2 ---
        ins("2. PANEL PRINCIPAL (DASHBOARD)", "subtitulo")
        sep()

        ins("2.1 Pestaña Inicio", "seccion")
        ins("Funciona como página de bienvenida y acceso rápido:")
        ins("  \u2022  Saludo personalizado: Muestra 'Bienvenido [Nombre]' según la sesión.", "item")
        ins("  \u2022  Botón Buscar: Acceso directo al Buscador Histórico.", "item")
        ins("  \u2022  Últimos trabajos consultados: Tabla con los 5 relevamientos más recientes.", "item")
        ins("  \u2022  Doble clic en cualquier fila abre el relevamiento en el Módulo de Cronometraje.", "item")
        ins("")

        ins("2.2 Pestaña Tareas", "seccion")
        ins("Centro de gestión de solicitudes de cronometraje. Muestra una tabla con las tareas "
            "disponibles según el rol del usuario.")
        ins("")
        ins("Columnas: Título, Descripción, Estado, Fecha, Informe.", "negrita")
        ins("")
        ins("Botones para JEFE/GERENTE:", "negrita")
        ins("  \u2022  Cargar nueva tarea: Formulario modal (Título, Descripción, Metodista asignado).", "item")
        ins("  \u2022  Cambiar Estado: Permite asignar cualquier estado, incluyendo Cerrado.", "item")
        ins("  \u2022  Borrar tarea: Elimina permanentemente la tarea (previa confirmación).", "item")
        ins("")
        ins("Botones para METODISTA:", "negrita")
        ins("  \u2022  Realizar Cronometraje: Abre el módulo vinculado a la tarea seleccionada.", "item")
        ins("  \u2022  Cambiar Estado: Permite modificar, excepto asignar Cerrado.", "item")
        ins("")
        ins("Los Metodistas solo ven sus tareas asignadas. Los Jefes/Gerentes ven todas.", "nota")
        sep()

        # --- SECCION 3 ---
        ins("3. MÓDULO DE CRONOMETRAJE", "subtitulo")
        sep()

        ins("3.1 Acceso", "seccion")
        ins("Se accede de tres formas:")
        ins("  \u2022  Menú Archivo \u2192 Nueva plantilla (plantilla vacía).", "item")
        ins("  \u2022  Menú Archivo \u2192 Importar desde Excel... (carga automática).", "item")
        ins("  \u2022  Desde el Dashboard (vinculada a una tarea o trabajos recientes).", "item")
        ins("")

        ins("3.2 Cabecera del Artículo", "seccion")
        ins("  \u2022  ARTÍCULO (código): Campo obligatorio, resaltado en amarillo.", "item")
        ins("  \u2022  OPERACIÓN: Nombre o código de la operación. Obligatorio.", "item")
        ins("  \u2022  DESCRIPCIÓN: Descripción detallada del artículo.", "item")
        ins("")

        ins("3.3 Panel Lateral (Datos del Estudio)", "seccion")
        ins("  \u2022  DE PIE / SENTADO: Casillas mutuamente excluyentes (postura del operario).", "item")
        ins("  \u2022  MÁQUINA: Desplegable + botones [+] para agregar y [-] para eliminar.", "item")
        ins("  \u2022  HM (Herramienta/Matriz): Desplegable + botones [+] y [-].", "item")
        ins("  \u2022  OPERARIO: Campo de texto libre.", "item")
        ins("  \u2022  FECHA: Se establece automáticamente con la fecha actual.", "item")
        ins("  \u2022  Nº de CRONOMETRAJE: Identificador correlativo automático (AUTO-XXX).", "item")
        ins("")

        ins("3.4 Creación de Plantilla", "seccion")
        ins("Botón 'Agregar nueva columna' (esquina superior derecha):", "negrita")
        ins("Abre un formulario modal con:")
        ins("  \u2022  Nº de observaciones: Cantidad de filas por elemento (predeterminado: 10).", "item")
        ins("  \u2022  Cantidad de Elementos: Elementos a agregar simultáneamente (predeterminado: 1).", "item")
        ins("Al presionar 'Generar', se crean las columnas dinámicas en la zona central.", "item")
        ins("")

        ins("3.5 Grilla de Tiempos", "seccion")
        ins("Cada elemento genera un bloque de tres columnas:")
        ins("  \u2022  V (Valoración): Factor de ritmo en %. Editable. Se agrega '%' al salir.", "item")
        ins("  \u2022  MIN (Minutos): Conversión automática. Solo lectura.", "item")
        ins("  \u2022  SEG/MIN (Tiempo bruto): Tiempo cronometrado. Editable. Solo acepta números.", "item")
        ins("")
        ins("El selector SEG/MIN en el encabezado define la unidad de entrada.", "negrita")
        ins("")

        ins("3.6 Resultados Estadísticos (por elemento)", "seccion")
        ins("Se calculan automáticamente en tiempo real:")
        ins("  \u2022  Nº de Observaciones: Conteo automático de filas con datos.", "item")
        ins("  \u2022  Elementos medidos: Editable (predeterminado: 1).", "item")
        ins("  \u2022  Lote frecuencial: Factor de frecuencia. Editable (predeterminado: 1).", "item")
        ins("  \u2022  Tiempo MEDIO: Suma(min) / (n x divisor).", "item")
        ins("  \u2022  Desvío estándar: Dispersión estadística (requiere 2+ datos).", "item")
        ins("  \u2022  Nº Obs. Necesarias: Cantidad estadísticamente necesaria.", "item")
        ins("  \u2022  Rango mediciones: Valor máximo menos mínimo.", "item")
        ins("  \u2022  Suplemento: Porcentaje por fatiga/necesidades. Editable.", "item")
        ins("  \u2022  Tiempo Normal: Suma(min x V) / (n x divisor).", "item")
        ins("  \u2022  Tiempo Estándar: Tiempo Normal x (1 + Suplemento).", "item")
        ins("")

        ins("3.7 Footer: Métricas Globales", "seccion")
        ins("Campos editables (fondo amarillo):", "negrita")
        ins("  \u2022  Piezas por golpe: Piezas producidas por ciclo.", "item")
        ins("  \u2022  Artículos por golpe: Artículos diferentes por ciclo.", "item")
        ins("  \u2022  Nº de operarios en máquina.", "item")
        ins("")
        ins("Campos de resultado (fondo verde, solo lectura):", "negrita")
        ins("  \u2022  Tiempo estándar operación = Suma(TE) / Piezas por golpe  [min/pieza].", "item")
        ins("  \u2022  Cadencia = 60 / TE Operación  [piezas/hora].", "item")
        ins("  \u2022  Cadencia = 1000 / Cadencia piezas/hora  [horas/1000 piezas].", "item")
        ins("")
        ins("Bloque Epicor (fondo azul, solo lectura):", "negrita")
        ins("  \u2022  Estándar Epicor = Cadencia horas/1000  [hh/1000].", "item")
        ins("  \u2022  Dotación Epicor = Nº de operarios en máquina.", "item")
        ins("")

        ins("3.8 Importación desde Excel", "seccion")
        ins("Menú Archivo \u2192 Importar desde Excel...", "negrita")
        ins("El sistema lee automáticamente: cabecera (artículo, operación, máquina, operario, "
            "fecha), grilla de tiempos (valoraciones, minutos, segundos) y parámetros (suplementos, "
            "lote frecuencial, piezas/golpe). Los datos se cargan como borrador nuevo.")
        ins("")

        ins("3.9 Finalización", "seccion")
        ins("Botón 'Finalizar' (esquina inferior derecha). Opciones:", "negrita")
        ins("  \u2022  Guardar en Base de Datos: Persiste el cronometraje completo en SQL Server.", "item")
        ins("  \u2022  Guardar como PDF: Genera informe PDF (nombre sugerido = código artículo).", "item")
        ins("  \u2022  Salir sin guardar: Limpia la plantilla y vuelve al Dashboard.", "item")
        ins("  \u2022  Cancelar: Cierra el diálogo sin acción.", "item")
        ins("")
        ins("'Salir sin guardar' es irreversible. Asegúrese de guardar antes.", "nota")
        sep()

        # --- SECCION 4 ---
        ins("4. BUSCADOR HISTÓRICO", "subtitulo")
        sep()

        ins("4.1 Acceso", "seccion")
        ins("  \u2022  Botón 'Buscar' en la pestaña Inicio del Dashboard.", "item")
        ins("")

        ins("4.2 Estructura", "seccion")
        ins("Título: 'Buscador Histórico de Relevamientos'.", "negrita")
        ins("Tabla con columnas: Fecha, Artículo, Operación, Máquina, HM, Operario.")
        ins("Indicador de resultados en la esquina derecha.")
        ins("")

        ins("4.3 Filtros Flotantes (tipo Excel)", "seccion")
        ins("  1.  Haga clic en el encabezado de una columna filtrable.", "item")
        ins("  2.  Aparece un desplegable flotante con valores únicos disponibles.", "item")
        ins("  3.  Seleccione un valor o escriba directamente para buscar.", "item")
        ins("  4.  Presione Enter o seleccione para aplicar.", "item")
        ins("  5.  El encabezado filtrado se marca con un icono de búsqueda.", "item")
        ins("  6.  Seleccione '(Todos)' para remover el filtro de esa columna.", "item")
        ins("  7.  Puede combinar filtros en múltiples columnas (operación AND).", "item")
        ins("")
        ins("La columna Fecha no admite filtrado por clic.", "nota")
        ins("")

        ins("4.4 Botones de Acción", "seccion")
        ins("  \u2022  Volver al Home: Regresa al Dashboard.", "item")
        ins("  \u2022  Limpiar Filtros: Remueve todos los filtros y recarga.", "item")
        ins("  \u2022  Cargar Relevamiento: Abre el registro seleccionado en el Cronometraje.", "item")
        ins("  \u2022  Borrar Planilla (solo JEFE/GERENTE): Eliminación permanente.", "item")
        ins("")
        ins("Doble clic en una fila equivale a presionar 'Cargar Relevamiento'.", "negrita")
        ins("")
        ins("La eliminación de planillas es permanente e irreversible.", "nota")
        sep()

        # --- MENU SUPERIOR ---
        ins("BARRA DE MENÚ SUPERIOR", "subtitulo")
        sep()
        ins("Se habilita tras iniciar sesión. Menú Archivo:", "negrita")
        ins("  \u2022  Nueva plantilla: Abre plantilla de cronometraje vacía.", "item")
        ins("  \u2022  Importar desde Excel...: Diálogo de selección de archivo.", "item")
        ins("  \u2022  Volver al Home: Regresa al Dashboard.", "item")
        ins("  \u2022  Cerrar Sesión: Cierra sesión y vuelve al Login.", "item")
        ins("")
        ins("Menú Herramientas:", "negrita")
        ins("  \u2022  Generar Backup de Base de Datos: Crea una copia de seguridad.", "item")
        ins("")
        ins("Botón directo 'Manual de Usuario':", "negrita")
        ins("  \u2022  Ubicado en la barra superior, al lado de Herramientas. Abre esta pantalla.", "item")
        sep()

        # --- SECCION 5: BACKUP ---
        ins("5. COPIA DE SEGURIDAD (BACKUP) DE LA BASE DE DATOS", "subtitulo")
        sep()
        ins("El sistema permite generar copias de seguridad de toda la información "
            "almacenada para prevenir pérdidas de datos.")
        ins("")
        ins("Pasos para generar un Backup:", "negrita")
        ins("  1.  En la barra superior de la pantalla principal, haz clic en el menú 'Herramientas'.", "item")
        ins("  2.  Selecciona la opción 'Generar Backup de Base de Datos'.", "item")
        ins("  3.  En la ventana emergente, selecciona la carpeta donde deseas guardar el archivo.", "item")
        ins("       (Nota: Debe ser una ubicación válida en el equipo servidor).", "nota")
        ins("  4.  Haz clic en 'Seleccionar Carpeta'.", "item")
        ins("  5.  El sistema procesará la solicitud y mostrará un cartel de Éxito indicando "
            "la ruta donde se guardó el archivo (.bak).", "item")
        ins("")
        ins("IMPORTANTE SOBRE LA RESTAURACIÓN:", "negrita")
        ins("La restauración de un backup implica sobreescribir el motor de datos y matar "
            "conexiones activas. En caso de emergencia, debe contactar al departamento de "
            "Sistemas (Administrador de Base de Datos) para realizar la restauración "
            "directamente en el servidor.", "nota")
        sep()

        # --- GLOSARIO ---
        ins("GLOSARIO DE TÉRMINOS", "subtitulo")
        sep()
        ins("  \u2022  Relevamiento: Estudio completo de cronometraje.", "item")
        ins("  \u2022  Elemento: Parte medible de una operación.", "item")
        ins("  \u2022  Valoración (V): Factor de ajuste según ritmo del operario (100% = normal).", "item")
        ins("  \u2022  Suplemento: Porcentaje adicional por fatiga y necesidades personales.", "item")
        ins("  \u2022  Tiempo Normal: Tiempo observado ajustado por valoración.", "item")
        ins("  \u2022  Tiempo Estándar: Tiempo Normal + suplementos. Referencia final.", "item")
        ins("  \u2022  Cadencia: Velocidad de producción (piezas/hora o horas/1000).", "item")
        ins("  \u2022  Lote frecuencial: Cada cuántos ciclos se realiza un elemento.", "item")
        ins("  \u2022  Epicor: Sistema ERP. Estándar y Dotación son datos de carga.", "item")
        ins("  \u2022  RBAC: Control de Acceso Basado en Roles.", "item")
        ins("  \u2022  Tarea: Solicitud de trabajo asignada a un Metodista.", "item")
        ins("")
        ins("Version Beta 0.15  -  Junio 2026  -  Ingenieria de Software", "nota")
