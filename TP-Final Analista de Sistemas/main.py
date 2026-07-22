import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Dict, Type, Any
import gestor_pdf
import vistas
import config
from logger import get_logger
from controlador import Controlador

logger = get_logger(__name__)

class Aplicacion(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.controlador = Controlador(self)
        
        self.title(config.TITULO_APP)
        # 1. Aplicamos minsize para evitar el colapso responsivo
        self.minsize(width=900, height=650)
        
        try:
            self.iconbitmap(config.ICONO_PATH)
        except Exception:
            logger.warning("No se pudo cargar el icono de la aplicación.")
        self.geometry(config.GEOMETRIA)


        # BARRA DE MENÚ NATIVA (nace oculta hasta el login exitoso)
        self.barra_menus = tk.Menu(self)
        self.menu_archivo = tk.Menu(self.barra_menus, tearoff=0)
        self.menu_archivo.add_command(label="Nueva plantilla", command=self.nueva_plantilla)
        self.menu_archivo.add_command(label="Importar desde Excel...", command=self._abrir_filedialog_excel)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Volver al Home", command=lambda: self.mostrar_frame(vistas.PaginaTareas))
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Cerrar Sesión", command=self.controlador.cerrar_sesion)
        
        self.barra_menus.add_cascade(label="Archivo", menu=self.menu_archivo)

        # Menú "Herramientas" — Backup BD
        self.menu_herramientas = tk.Menu(self.barra_menus, tearoff=0)
        self.menu_herramientas.add_command(label="Generar Backup de Base de Datos", command=self.controlador.crear_backup_bd)
        self.barra_menus.add_cascade(label="Herramientas", menu=self.menu_herramientas)

        # Botón directo "Manual de Usuario" en la barra superior
        self.barra_menus.add_command(label="Manual de Usuario", command=lambda: self.mostrar_frame(vistas.PaginaManual))
        
        # CONTENEDOR
        self.contenedor = tk.Frame(self, bg="white")
        self.contenedor.pack(side="top", fill="both", expand=True)

        self.contenedor.columnconfigure(0, weight=1) # Permite que la columna 0 crezca
        self.contenedor.rowconfigure(0, weight=1)    # Permite que la fila 0 crezca

        self.frames: Dict[Type[tk.Frame], tk.Frame] = {}
        for Pagina in (vistas.PaginaLogin, vistas.PaginaTareas, vistas.PaginaRegistroUsuario, vistas.Plantilla, vistas.PaginaBuscadorHistorico, vistas.PaginaManual):
            frame = Pagina(self.contenedor, self.controlador)
            self.frames[Pagina] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(vistas.PaginaLogin)

    # FUNCIONES DE NAVEGACIÓN
    def mostrar_frame(self, nombre_clase: Type[tk.Frame]) -> None:
        frame = self.frames[nombre_clase]
        frame.tkraise()
        # Forzar actualización de la vista al mostrarla (Corrige Bug de RBAC en Tkinter)
        if hasattr(frame, "actualizar_vista"):
            frame.actualizar_vista()

    def nueva_plantilla(self) -> None:
        self.controlador.nueva_plantilla()

    def abrir_archivo(self) -> None:
        self.controlador.abrir_archivo()

    def guardar_archivo(self) -> bool:
        return self.controlador.guardar_archivo()

    def _abrir_filedialog_excel(self) -> None:
        """Abre un diálogo para seleccionar un archivo Excel e invoca la importación."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=(("Archivos Excel", "*.xlsx *.xlsm"), ("Todos los archivos", "*.*"))
        )
        if ruta:
            self.controlador.importar_desde_excel(ruta)

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()