import pyodbc
import config
from logger import get_logger

logger = get_logger(__name__)

def run_migration() -> bool:
    """
    Ejecuta la migración de base de datos para agregar las columnas necesarias a SQL Server.
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
        cursor = conn.cursor()
        
        # 1. Add 'tipo' column to Recursos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Recursos' AND column_name = 'tipo'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Recursos ADD tipo NVARCHAR(50) NOT NULL DEFAULT 'MAQUINA'")
            logger.info("Columna 'tipo' agregada a la tabla 'Recursos'.")
            print("Agregada columna 'tipo' a 'Recursos'.")
            
        # 2. Add 'id_hm' column to Relevamientos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Relevamientos' AND column_name = 'id_hm'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Relevamientos ADD id_hm INT NULL CONSTRAINT FK_Rel_HM FOREIGN KEY (id_hm) REFERENCES Recursos(id_recurso)")
            logger.info("Columna 'id_hm' agregada a la tabla 'Relevamientos'.")
            print("Agregada columna 'id_hm' a 'Relevamientos'.")
            
        # 3. Add 'piezas_por_golpe' column to Relevamientos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Relevamientos' AND column_name = 'piezas_por_golpe'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Relevamientos ADD piezas_por_golpe INT NOT NULL DEFAULT 1")
            logger.info("Columna 'piezas_por_golpe' agregada a la tabla 'Relevamientos'.")
            print("Agregada columna 'piezas_por_golpe' a 'Relevamientos'.")
            
        # 4. Add 'articulos_por_golpe' column to Relevamientos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Relevamientos' AND column_name = 'articulos_por_golpe'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Relevamientos ADD articulos_por_golpe INT NOT NULL DEFAULT 1")
            logger.info("Columna 'articulos_por_golpe' agregada a la tabla 'Relevamientos'.")
            print("Agregada columna 'articulos_por_golpe' a 'Relevamientos'.")
            
        # 5. Add 'operarios_maquina' column to Relevamientos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Relevamientos' AND column_name = 'operarios_maquina'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Relevamientos ADD operarios_maquina INT NOT NULL DEFAULT 1")
            logger.info("Columna 'operarios_maquina' agregada a la tabla 'Relevamientos'.")
            print("Agregada columna 'operarios_maquina' a 'Relevamientos'.")
            
        # 6. Add 'id_tarea' column to Relevamientos if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Relevamientos' AND column_name = 'id_tarea'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Relevamientos ADD id_tarea INT NULL CONSTRAINT FK_Rel_Tarea FOREIGN KEY (id_tarea) REFERENCES Tareas(id_tarea)")
            logger.info("Columna 'id_tarea' agregada a la tabla 'Relevamientos'.")
            print("Agregada columna 'id_tarea' a 'Relevamientos'.")
            
        # 7. Add 'elementos_medidos' column to TiemposElemento if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'TiemposElemento' AND column_name = 'elementos_medidos'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE TiemposElemento ADD elementos_medidos INT NOT NULL DEFAULT 1")
            logger.info("Columna 'elementos_medidos' agregada a la tabla 'TiemposElemento'.")
            print("Agregada columna 'elementos_medidos' a 'TiemposElemento'.")
            
        # 8. Add 'lote_frecuencial' column to TiemposElemento if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'TiemposElemento' AND column_name = 'lote_frecuencial'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE TiemposElemento ADD lote_frecuencial FLOAT NOT NULL DEFAULT 1.0")
            logger.info("Columna 'lote_frecuencial' agregada a la tabla 'TiemposElemento'.")
            print("Agregada columna 'lote_frecuencial' a 'TiemposElemento'.")
            
        # 9. Add 'suplemento' column to TiemposElemento if it doesn't exist
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'TiemposElemento' AND column_name = 'suplemento'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE TiemposElemento ADD suplemento FLOAT NOT NULL DEFAULT 0.0")
            logger.info("Columna 'suplemento' agregada a la tabla 'TiemposElemento'.")
            print("Agregada columna 'suplemento' a 'TiemposElemento'.")
            
        # 10. ALTER COLUMN minutos de INT a FLOAT en TiemposElemento (BUG 1: Truncamiento SQL)
        cursor.execute("""
            SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'TiemposElemento' AND COLUMN_NAME = 'minutos'
        """)
        col_type_row = cursor.fetchone()
        if col_type_row and col_type_row[0].lower() != 'float':
            cursor.execute("ALTER TABLE TiemposElemento ALTER COLUMN minutos FLOAT")
            logger.info("Columna 'minutos' de TiemposElemento migrada de INT a FLOAT.")
            print("Migrada columna 'minutos' a FLOAT en 'TiemposElemento'.")

        # 11. ADD columna 'codigo' a Articulos (BUG 2: Desfase de Artículo)
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Articulos' AND column_name = 'codigo'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Articulos ADD codigo NVARCHAR(50) NULL")
            logger.info("Columna 'codigo' agregada a la tabla 'Articulos'.")
            print("Agregada columna 'codigo' a 'Articulos'.")

        conn.commit()
        logger.info("Migración de base de datos completada exitosamente.")
        print("Migración completada exitosamente.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        logger.exception("Error crítico durante la migración de base de datos.")
        print(f"Error de migración: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_migration()
