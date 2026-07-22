import os
from typing import Final

# Colores originales (UI/UX no modificable)
COLOR_BARRA_SUPERIOR: Final[str] = "#2c3e50"
COLOR_BOTON_ACTIVO: Final[str] = "#1abc9c"
COLOR_BG_INICIO: Final[str] = "#ecf0f1"
COLOR_BG_TAREAS: Final[str] = "#d5dbdb"
COLOR_BG_TABLA_HEAD: Final[str] = "#f0f0f0"
COLOR_BOTON_FINALIZAR: Final[str] = "#2980b9"

# Configuración de ventana
TITULO_APP: Final[str] = "Metodos y Tiempos"
GEOMETRIA: Final[str] = "700x600"
ICONO_PATH: Final[str] = "logo.ico"

# Configuración de Base de Datos
DB_DRIVER: Final[str] = "{ODBC Driver 17 for SQL Server}"
DB_SERVER: Final[str] = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
DB_NAME: Final[str] = os.getenv("DB_NAME", "MetodosTiemposDB")
DB_USER: Final[str] = os.getenv("DB_USER", "sa")
DB_PASSWORD: Final[str] = os.getenv("DB_PASSWORD", "secret")

# Log Configuration
LOG_FILE: Final[str] = "app_metodos_tiempos.log"

# Seguridad
MASTER_PASSWORD: Final[str] = "LongvieAdmin2026"