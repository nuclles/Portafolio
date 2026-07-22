# pyrefly: ignore [missing-import]
import pyodbc
from typing import Iterator, Any, Optional
from contextlib import contextmanager
import config
from logger import get_logger

logger = get_logger(__name__)

class DatabaseConnectionError(Exception):
    """Excepción personalizada para errores de conexión a la base de datos."""
    pass

@contextmanager
def get_db_connection() -> Iterator[pyodbc.Connection]:
    """
    Context Manager (Regla 3) para manejar de forma segura la conexión a SQL Server.
    Garantiza que la conexión se cierre al salir del bloque.
    
    Yields:
        pyodbc.Connection: Objeto de conexión a la base de datos.
        
    Raises:
        DatabaseConnectionError: Si falla la conexión a la base de datos (Regla 7).
    """
    conn_str = (
        f"DRIVER={config.DB_DRIVER};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"Trusted_Connection=yes;"
    )
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        logger.info("Conexión a base de datos establecida exitosamente.")
        yield conn
    except pyodbc.Error as e:
        logger.exception("Error crítico al conectar a SQL Server.")
        raise DatabaseConnectionError(f"No se pudo conectar a la base de datos: {e}")
    finally:
        if conn is not None:
            conn.close()
            logger.debug("Conexión a la base de datos cerrada.")

@contextmanager
def get_db_cursor(commit: bool = False) -> Iterator[pyodbc.Cursor]:
    """
    Context Manager (Regla 3 y 6) para manejar un cursor de SQL Server,
    con soporte para transacciones seguras (commit/rollback).
    
    Args:
        commit (bool): Indica si se debe ejecutar commit() al finalizar sin errores.
        
    Yields:
        pyodbc.Cursor: Cursor activo para ejecutar consultas.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
                logger.info("Transacción confirmada (commit).")
        except Exception as e:
            conn.rollback()
            logger.exception("Error en transacción SQL. Se ejecutó rollback().")
            raise
        finally:
            cursor.close()
            logger.debug("Cursor de base de datos cerrado.")


def ejecutar_backup(ruta_destino: str) -> bool:
    """
    Ejecuta un backup nativo de SQL Server (BACKUP DATABASE) a la ruta indicada.

    Utiliza una conexión independiente con autocommit=True, ya que el comando
    BACKUP DATABASE de SQL Server no puede ejecutarse dentro de un bloque
    de transacción explícito. Esta conexión se abre y cierra exclusivamente
    para esta operación administrativa.

    Args:
        ruta_destino (str): Ruta absoluta del archivo .bak de destino en el
            servidor de SQL Server. Ejemplo: ``'C:\\Backups\\mi_db.bak'``.

    Returns:
        bool: ``True`` si el backup se completó exitosamente,
              ``False`` si ocurrió cualquier error durante la operación.

    Raises:
        No levanta excepciones. Todos los errores se capturan, registran
        en el logger y la función retorna ``False``.

    Note:
        El comando BACKUP DATABASE es una instrucción DDL administrativa que
        no soporta consultas parametrizadas via ``cursor.execute(sql, params)``.
        La interpolación directa de ``config.DB_NAME`` y ``ruta_destino`` en
        el string SQL es una excepción técnica justificada a la Regla 6.
    """
    conn_str: str = (
        f"DRIVER={config.DB_DRIVER};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"Trusted_Connection=yes;"
    )
    conn: Optional[pyodbc.Connection] = None
    cursor: Optional[pyodbc.Cursor] = None
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        logger.info(
            "Conexión con autocommit establecida para backup de '%s'.",
            config.DB_NAME,
        )

        sql_backup: str = (
            f"BACKUP DATABASE [{config.DB_NAME}] "
            f"TO DISK = '{ruta_destino}' "
            f"WITH FORMAT, "
            f"MEDIANAME = 'SQLServerBackups', "
            f"NAME = 'Full Backup'"
        )
        cursor.execute(sql_backup)

        # BACKUP DATABASE puede devolver múltiples result sets informativos.
        # Consumirlos evita que la conexión quede en estado inconsistente.
        while cursor.nextset():
            pass

        logger.info(
            "Backup de la base de datos '%s' completado exitosamente en: %s",
            config.DB_NAME,
            ruta_destino,
        )
        return True

    except pyodbc.Error as db_err:
        logger.exception(
            "Error de SQL Server al ejecutar backup de '%s': %s",
            config.DB_NAME,
            db_err,
        )
        return False

    except OSError as os_err:
        logger.exception(
            "Error de sistema operativo durante el backup (posible ruta inválida '%s'): %s",
            ruta_destino,
            os_err,
        )
        return False

    except Exception as unexpected_err:
        logger.exception(
            "Error inesperado durante el backup de '%s': %s",
            config.DB_NAME,
            unexpected_err,
        )
        return False

    finally:
        if cursor is not None:
            cursor.close()
            logger.debug("Cursor de backup cerrado.")
        if conn is not None:
            conn.close()
            logger.debug("Conexión de backup cerrada.")
