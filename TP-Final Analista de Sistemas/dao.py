from typing import Dict, List, Optional
from database import get_db_cursor
from modelos import Articulo, Operario, Recurso, Relevamiento, Usuario, Tarea
from logger import get_logger

logger = get_logger(__name__)

class ArticuloDAO:
    @staticmethod
    def obtener_todos() -> List[Articulo]:
        """Obtiene todos los artículos usando consultas parametrizadas (Regla 6)."""
        query = "SELECT id_articulo, ISNULL(codigo, '') AS codigo, descripcion FROM Articulos"
        articulos: List[Articulo] = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    articulos.append(Articulo(id_articulo=row[0], codigo=row[1], descripcion=row[2]))
        except Exception:
            logger.exception("Falló la obtención de artículos.")
        return articulos

    @staticmethod
    def obtener_por_codigo(codigo: str) -> Optional[Articulo]:
        """
        Obtiene un artículo por su código alfanumérico usando consulta parametrizada (Regla 6).
        
        Args:
            codigo: Código alfanumérico del artículo ingresado por el usuario.
            
        Returns:
            Articulo si existe, None en caso contrario.
        """
        query = "SELECT id_articulo, ISNULL(codigo, '') AS codigo, descripcion FROM Articulos WHERE codigo = ?"
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (codigo,))
                row = cursor.fetchone()
                if row:
                    return Articulo(id_articulo=row[0], codigo=row[1], descripcion=row[2])
        except Exception:
            logger.exception(f"Error al buscar artículo por código: {codigo}")
        return None

    @staticmethod
    def obtener_o_crear(codigo: str, descripcion: str) -> Articulo:
        """
        Obtiene un artículo por código o lo crea con código+descripción de forma transaccional (Regla 6).
        
        Args:
            codigo: Código alfanumérico del artículo (ej. 'CHAPA-123').
            descripcion: Descripción textual del artículo.
            
        Returns:
            Articulo existente o recién creado.
            
        Raises:
            Exception: Si falla la inserción en la BD.
        """
        try:
            art = ArticuloDAO.obtener_por_codigo(codigo)
            if art:
                return art
            
            query = "INSERT INTO Articulos (codigo, descripcion) OUTPUT INSERTED.id_articulo VALUES (?, ?)"
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (codigo, descripcion))
                new_id = cursor.fetchone()[0]
                return Articulo(id_articulo=new_id, codigo=codigo, descripcion=descripcion)
        except Exception:
            logger.exception(f"Error al obtener o crear artículo: código={codigo}, desc={descripcion}")
            raise

class RecursoDAO:
    @staticmethod
    def obtener_por_tipo(tipo: str) -> List[Recurso]:
        """
        Obtiene los recursos filtrados por tipo (MAQUINA o HM) de forma segura (Regla 4 y 6).
        """
        query = "SELECT id_recurso, descripcion, tipo FROM Recursos WHERE tipo = ?"
        recursos = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (tipo,))
                for row in cursor.fetchall():
                    recursos.append(Recurso(id_recurso=str(row[0]), nombre=row[1], tipo=row[2]))
        except Exception:
            logger.exception(f"Error al obtener recursos del tipo {tipo}.")
        return recursos

    @staticmethod
    def obtener_por_descripcion_y_tipo(descripcion: str, tipo: str) -> Optional[Recurso]:
        """
        Obtiene un recurso por su descripción y tipo.
        """
        query = "SELECT id_recurso, descripcion, tipo FROM Recursos WHERE descripcion = ? AND tipo = ?"
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (descripcion, tipo))
                row = cursor.fetchone()
                if row:
                    return Recurso(id_recurso=str(row[0]), nombre=row[1], tipo=row[2])
        except Exception:
            logger.exception("Error al buscar recurso por descripción y tipo.")
        return None

    @staticmethod
    def crear_silencioso(descripcion: str, tipo: str) -> Optional[Recurso]:
        """
        Inserta un nuevo recurso de forma silenciosa si no existe.
        """
        try:
            existing = RecursoDAO.obtener_por_descripcion_y_tipo(descripcion, tipo)
            if existing:
                return existing
                
            query = "INSERT INTO Recursos (descripcion, tipo) OUTPUT INSERTED.id_recurso VALUES (?, ?)"
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (descripcion, tipo))
                row = cursor.fetchone()
                if row:
                    return Recurso(id_recurso=str(row[0]), nombre=descripcion, tipo=tipo)
        except Exception:
            logger.exception(f"Error al crear recurso silenciosamente: {descripcion} ({tipo})")
        return None

    @staticmethod
    def borrar_por_nombre_y_tipo(descripcion: str, tipo: str) -> bool:
        """
        Elimina un recurso por su descripción y tipo de forma transaccional.

        Usa consulta parametrizada (Regla 6) y transacción explícita.
        Si el recurso está referenciado por Relevamientos, la BD rechazará
        la operación por integridad referencial.

        Args:
            descripcion: Nombre/descripción del recurso a eliminar.
            tipo: Tipo del recurso ('MAQUINA' o 'HM').

        Returns:
            True si se eliminó al menos un registro, False en caso contrario.

        Raises:
            No lanza excepciones al exterior; registra en logger (Regla 7).
        """
        query = "DELETE FROM Recursos WHERE descripcion = ? AND tipo = ?"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (descripcion, tipo))
                eliminado = cursor.rowcount > 0
                if eliminado:
                    logger.info(f"Recurso '{descripcion}' ({tipo}) eliminado de la BD.")
                else:
                    logger.warning(f"No se encontró recurso '{descripcion}' ({tipo}) para eliminar.")
                return eliminado
        except Exception:
            logger.exception(f"Error al eliminar recurso '{descripcion}' ({tipo}).")
            return False

class OperarioDAO:
    @staticmethod
    def obtener_todos() -> List[Operario]:
        """
        Obtiene todos los operarios registrados.
        """
        query = "SELECT id_operario, nombre FROM Operarios"
        operarios = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    operarios.append(Operario(id_operario=str(row[0]), nombre=row[1], legajo=""))
        except Exception:
            logger.exception("Error al obtener todos los operarios.")
        return operarios

    @staticmethod
    def obtener_por_nombre(nombre: str) -> Optional[Operario]:
        """
        Obtiene un operario por su nombre.
        """
        query = "SELECT id_operario, nombre FROM Operarios WHERE nombre = ?"
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (nombre,))
                row = cursor.fetchone()
                if row:
                    return Operario(id_operario=str(row[0]), nombre=row[1], legajo="")
        except Exception:
            logger.exception("Error al buscar operario por nombre.")
        return None

    @staticmethod
    def crear_silencioso(nombre: str) -> Optional[Operario]:
        """
        Inserta un nuevo operario de forma silenciosa si no existe.
        """
        try:
            existing = OperarioDAO.obtener_por_nombre(nombre)
            if existing:
                return existing
                
            query = "INSERT INTO Operarios (nombre) OUTPUT INSERTED.id_operario VALUES (?)"
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (nombre,))
                row = cursor.fetchone()
                if row:
                    return Operario(id_operario=str(row[0]), nombre=nombre, legajo="")
        except Exception:
            logger.exception(f"Error al crear operario silenciosamente: {nombre}")
        return None

class RelevamientoDAO:
    @staticmethod
    def obtener_siguiente_id() -> int:
        """
        Obtiene el siguiente ID correlativo para el relevamiento.
        """
        query = "SELECT ISNULL(MAX(id_relevamiento), 0) + 1 FROM Relevamientos"
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    return int(row[0])
        except Exception:
            logger.exception("Error al obtener el siguiente ID de relevamiento.")
        return 1

    @staticmethod
    def guardar(relevamiento: 'Relevamiento') -> bool:
        """
        Guarda un relevamiento y sus tiempos asociados en una sola transacción estricta.
        Soporta inserción (INSERT) o actualización (UPDATE) si ya existe.
        Cumple la Regla 6 (Transacciones explícitas) y la creación dinámica de entidades.
        """
        query_insert = """
            INSERT INTO Relevamientos 
            (id_articulo, operacion, id_recurso, id_hm, id_operario, fecha, postura, piezas_por_golpe, articulos_por_golpe, operarios_maquina, id_tarea)
            OUTPUT INSERTED.id_relevamiento
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        query_update = """
            UPDATE Relevamientos SET
                id_articulo = ?, operacion = ?, id_recurso = ?, id_hm = ?, id_operario = ?,
                fecha = ?, postura = ?, piezas_por_golpe = ?, articulos_por_golpe = ?, operarios_maquina = ?, id_tarea = ?
            WHERE id_relevamiento = ?
        """
        query_delete_tiempos = """
            DELETE FROM TiemposElemento WHERE id_relevamiento = ?
        """
        query_tiempo = """
            INSERT INTO TiemposElemento (id_relevamiento, elemento, valoracion, minutos, segundos, elementos_medidos, lote_frecuencial, suplemento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        from database import get_db_connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                art_id = relevamiento.articulo.id_articulo if relevamiento.articulo else None
                
                # --- Gestión dinámica de Entidades Maestras ---
                # Máquina
                rec_id = None
                maq_nombre = None
                if isinstance(relevamiento.recurso, str):
                    maq_nombre = relevamiento.recurso.strip()
                elif relevamiento.recurso and hasattr(relevamiento.recurso, 'nombre'):
                    maq_nombre = relevamiento.recurso.nombre.strip() if relevamiento.recurso.nombre else None
                
                if maq_nombre:
                    cursor.execute("SELECT id_recurso FROM Recursos WHERE descripcion = ? AND tipo = 'MAQUINA'", (maq_nombre,))
                    row_maq = cursor.fetchone()
                    if row_maq:
                        rec_id = row_maq[0]
                    else:
                        cursor.execute("INSERT INTO Recursos (descripcion, tipo) OUTPUT INSERTED.id_recurso VALUES (?, 'MAQUINA')", (maq_nombre,))
                        rec_id = cursor.fetchone()[0]

                # HM (Herramienta/Matriz)
                hm_id = None
                hm_nombre = None
                if isinstance(relevamiento.hm, str):
                    hm_nombre = relevamiento.hm.strip()
                elif relevamiento.hm and hasattr(relevamiento.hm, 'nombre'):
                    hm_nombre = relevamiento.hm.nombre.strip() if relevamiento.hm.nombre else None
                
                if hm_nombre:
                    cursor.execute("SELECT id_recurso FROM Recursos WHERE descripcion = ? AND tipo = 'HM'", (hm_nombre,))
                    row_hm = cursor.fetchone()
                    if row_hm:
                        hm_id = row_hm[0]
                    else:
                        cursor.execute("INSERT INTO Recursos (descripcion, tipo) OUTPUT INSERTED.id_recurso VALUES (?, 'HM')", (hm_nombre,))
                        hm_id = cursor.fetchone()[0]

                # Operario
                op_id = None
                op_nombre = None
                if isinstance(relevamiento.operario, str):
                    op_nombre = relevamiento.operario.strip()
                elif relevamiento.operario and hasattr(relevamiento.operario, 'nombre'):
                    op_nombre = relevamiento.operario.nombre.strip() if relevamiento.operario.nombre else None
                
                if op_nombre:
                    cursor.execute("SELECT id_operario FROM Operarios WHERE nombre = ?", (op_nombre,))
                    row_op = cursor.fetchone()
                    if row_op:
                        op_id = row_op[0]
                    else:
                        cursor.execute("INSERT INTO Operarios (nombre) OUTPUT INSERTED.id_operario VALUES (?)", (op_nombre,))
                        op_id = cursor.fetchone()[0]
                
                # --- Preparación de la cabecera ---
                from datetime import date
                fecha_str = relevamiento.fecha
                if isinstance(fecha_str, date):
                    fecha_str = fecha_str.strftime("%d/%m/%Y")
                
                # Sanitización estricta de Foreign Key id_tarea
                id_tarea_db = relevamiento.id_tarea
                if not id_tarea_db or str(id_tarea_db).strip() == "" or str(id_tarea_db) == "0" or str(id_tarea_db).lower() == "none":
                    id_tarea_db = None
                else:
                    id_tarea_db = int(id_tarea_db)
                    
                id_rel = relevamiento.id_relevamiento
                
                if id_rel is not None:
                    # UPDATE cabecera
                    cursor.execute(query_update, (
                        art_id, relevamiento.operacion, rec_id, hm_id, op_id, 
                        fecha_str, relevamiento.postura,
                        relevamiento.piezas_por_golpe, relevamiento.articulos_por_golpe,
                        relevamiento.operarios_maquina, id_tarea_db,
                        id_rel
                    ))
                else:
                    # INSERT cabecera
                    cursor.execute(query_insert, (
                        art_id, relevamiento.operacion, rec_id, hm_id, op_id, 
                        fecha_str, relevamiento.postura,
                        relevamiento.piezas_por_golpe, relevamiento.articulos_por_golpe,
                        relevamiento.operarios_maquina, id_tarea_db
                    ))
                    id_rel = cursor.fetchone()[0]
                    relevamiento.id_relevamiento = id_rel
                
                if not relevamiento.tiempos:
                    raise ValueError("La lista de tiempos está vacía. Abortando guardado para prevenir pérdida de datos (Regla 0).")
                
                # DELETE tiempos anteriores antes del bulk insert
                cursor.execute(query_delete_tiempos, (id_rel,))
                
                # INSERT tiempos nuevos
                for t in relevamiento.tiempos:
                    cursor.execute(query_tiempo, (
                        id_rel, t.elemento, t.valoracion, t.minutos, t.segundos,
                        t.elementos_medidos, t.lote_frecuencial, t.suplemento
                    ))
                
                conn.commit()
                logger.info(f"Relevamiento {id_rel} guardado exitosamente en BD (Cabecera + Detalle).")
                return True
            except Exception as e:
                conn.rollback()
                logger.exception("Error crítico en transacción de guardado. Se ejecutó rollback.")
                raise e
            finally:
                cursor.close()

    @staticmethod
    def obtener_por_id(id_relevamiento: int) -> Optional['Relevamiento']:
        """
        Obtiene un relevamiento por su ID directamente, sin manejo silencioso de errores (Regla 0 y Regla 7).
        """
        from modelos import Relevamiento, Articulo, Recurso, Operario, TiemposElemento
        from database import get_db_cursor
        
        query_cabecera = """
            SELECT 
                r.id_relevamiento, r.operacion, r.fecha, r.postura, 
                r.piezas_por_golpe, r.articulos_por_golpe, r.operarios_maquina, r.id_tarea,
                ISNULL(a.codigo, '') AS articulo_codigo,
                ISNULL(a.descripcion, '') AS articulo_desc,
                m.descripcion AS maquina_desc, m.tipo AS maquina_tipo,
                h.descripcion AS hm_desc, h.tipo AS hm_tipo,
                o.nombre AS operario_nombre
            FROM Relevamientos r
            LEFT JOIN Articulos a ON r.id_articulo = a.id_articulo
            LEFT JOIN Recursos m ON r.id_recurso = m.id_recurso
            LEFT JOIN Recursos h ON r.id_hm = h.id_recurso
            LEFT JOIN Operarios o ON r.id_operario = o.id_operario
            WHERE r.id_relevamiento = ?
        """
        with get_db_cursor() as cursor:
            cursor.execute(query_cabecera, (id_relevamiento,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Mapeo inmune a desfases utilizando nombres de columnas (Regla 0)
            columns = [column[0] for column in cursor.description]
            result_dict = dict(zip(columns, row))
                
            id_rel = result_dict.get('id_relevamiento')
            operacion = result_dict.get('operacion')
            fecha_str = result_dict.get('fecha')
            postura = result_dict.get('postura')
            piezas = result_dict.get('piezas_por_golpe')
            articulos_g = result_dict.get('articulos_por_golpe')
            operarios_m = result_dict.get('operarios_maquina')
            id_tarea = result_dict.get('id_tarea')
            
            art_codigo = result_dict.get('articulo_codigo')
            art_desc = result_dict.get('articulo_desc')
            maq_desc = result_dict.get('maquina_desc')
            maq_tipo = result_dict.get('maquina_tipo')
            hm_desc = result_dict.get('hm_desc')
            hm_tipo = result_dict.get('hm_tipo')
            op_nombre = result_dict.get('operario_nombre')

            articulo_obj = None
            if art_codigo or art_desc:
                articulo_obj = Articulo(
                    id_articulo="0", 
                    codigo=art_codigo or "", 
                    descripcion=art_desc or ""
                )

            maquina_obj = None
            if maq_desc is not None:
                maquina_obj = Recurso(id_recurso="0", nombre=maq_desc, tipo=maq_tipo)

            hm_obj = None
            if hm_desc is not None:
                hm_obj = Recurso(id_recurso="0", nombre=hm_desc, tipo=hm_tipo)

            operario_obj = None
            if op_nombre is not None:
                operario_obj = Operario(id_operario="0", nombre=op_nombre, legajo="")

            query_tiempos = "SELECT elemento, valoracion, minutos, segundos, elementos_medidos, lote_frecuencial, suplemento FROM TiemposElemento WHERE id_relevamiento = ? ORDER BY id_tiempo ASC"
            cursor.execute(query_tiempos, (id_rel,))
            tiempos_db = cursor.fetchall()
            
            tiempos = []
            for t_row in tiempos_db:
                tiempos.append(TiemposElemento(
                    elemento=t_row[0],
                    valoracion=float(t_row[1]),
                    minutos=float(t_row[2]),
                    segundos=float(t_row[3]),
                    elementos_medidos=int(t_row[4]),
                    lote_frecuencial=float(t_row[5]),
                    suplemento=float(t_row[6])
                ))
            
            from datetime import datetime, date
            parsed_date = date.today()
            if fecha_str:
                if isinstance(fecha_str, str):
                    if "-" in fecha_str:
                        parsed_date = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                    else:
                        parsed_date = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                else:
                    parsed_date = fecha_str

            return Relevamiento(
                id_relevamiento=id_rel,
                id_tarea=id_tarea,
                articulo=articulo_obj,
                operacion=operacion,
                recurso=maquina_obj,
                hm=hm_obj,
                operario=operario_obj,
                fecha=parsed_date,
                postura=postura if postura else "pie",
                piezas_por_golpe=int(piezas) if piezas else 1,
                articulos_por_golpe=int(articulos_g) if articulos_g else 1,
                operarios_maquina=int(operarios_m) if operarios_m else 1,
                tiempos=tiempos
            )

    @staticmethod
    def obtener_por_tarea(id_tarea: int) -> Optional[Relevamiento]:
        """
        Obtiene un relevamiento asociado a una tarea.
        """
        query = "SELECT id_relevamiento FROM Relevamientos WHERE id_tarea = ?"
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (id_tarea,))
                row = cursor.fetchone()
                if row:
                    return RelevamientoDAO.obtener_por_id(int(row[0]))
        except Exception:
            logger.exception(f"Error al obtener relevamiento por tarea: {id_tarea}")
        return None
    @staticmethod
    def obtener_todos_resumen() -> List[tuple]:
        """
        Devuelve un resumen de todos los relevamientos para listarlos en la interfaz.
        Retorna lista de tuplas: (ID, Fecha, Artículo, Operación, Operario)
        """
        query = """
            SELECT 
                r.id_relevamiento, 
                r.fecha, 
                ISNULL(a.codigo, 'S/C') AS articulo_codigo, 
                r.operacion, 
                ISNULL(o.nombre, 'S/O') AS operario_nombre
            FROM Relevamientos r
            LEFT JOIN Articulos a ON r.id_articulo = a.id_articulo
            LEFT JOIN Operarios o ON r.id_operario = o.id_operario
            ORDER BY r.id_relevamiento DESC
        """
        resumen = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    resumen.append((row[0], row[1], row[2], row[3], row[4]))
        except Exception:
            logger.exception("Error al obtener resumen de relevamientos.")
        return resumen

    @staticmethod
    def buscar_historico(filtros: Dict[str, str]) -> List[tuple]:
        """
        Busca relevamientos históricos aplicando filtros dinámicos combinados.

        Construye una consulta SQL con LEFT JOINs a Articulos, Recursos (máquina y HM)
        y Operarios. Agrega cláusulas WHERE parametrizadas según los filtros provistos,
        utilizando LIKE para búsqueda parcial (Regla 6: consultas parametrizadas estrictas).

        Args:
            filtros: Diccionario con claves opcionales:
                - 'articulo': Filtra por código del artículo.
                - 'operario': Filtra por nombre del operario.
                - 'maquina': Filtra por descripción de la máquina.
                - 'hm': Filtra por descripción de la herramienta/matriz.
                - 'operacion': Filtra por nombre de la operación.

        Returns:
            Lista de tuplas con formato:
            (id_relevamiento, fecha, codigo_articulo, operacion, maquina, hm, operario).
            El id_relevamiento se usa internamente como iid del Treeview pero NO se
            muestra al usuario. El código del artículo actúa como identificador visual.
            Retorna lista vacía si ocurre un error.

        Raises:
            No lanza excepciones al exterior; los errores se registran
            en el logger (Regla 7).
        """
        query_base = """
            SELECT
                r.id_relevamiento,
                r.fecha,
                ISNULL(a.codigo, 'S/C') AS codigo_articulo,
                ISNULL(r.operacion, '') AS operacion,
                ISNULL(m.descripcion, 'S/M') AS maquina_desc,
                ISNULL(h.descripcion, 'S/HM') AS hm_desc,
                ISNULL(o.nombre, 'S/O') AS operario_nombre
            FROM Relevamientos r
            LEFT JOIN Articulos a ON r.id_articulo = a.id_articulo
            LEFT JOIN Recursos m ON r.id_recurso = m.id_recurso
            LEFT JOIN Recursos h ON r.id_hm = h.id_recurso
            LEFT JOIN Operarios o ON r.id_operario = o.id_operario
        """

        condiciones: List[str] = []
        parametros: List[str] = []

        # Mapeo filtro -> columna SQL para construcción dinámica segura
        mapa_filtros: Dict[str, str] = {
            "articulo": "a.codigo",
            "operario": "o.nombre",
            "maquina": "m.descripcion",
            "hm": "h.descripcion",
            "operacion": "r.operacion",
        }

        for clave, columna in mapa_filtros.items():
            valor = filtros.get(clave, "").strip()
            if valor:
                condiciones.append(f"{columna} LIKE ?")
                parametros.append(f"%{valor}%")

        if condiciones:
            query_base += " WHERE " + " AND ".join(condiciones)

        query_base += " ORDER BY r.id_relevamiento DESC"

        resultados: List[tuple] = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query_base, tuple(parametros))
                for row in cursor.fetchall():
                    resultados.append(
                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    )
        except Exception:
            logger.exception("Error al ejecutar búsqueda histórica de relevamientos.")
        return resultados

    @staticmethod
    def borrar_por_id(id_relevamiento: int) -> bool:
        """
        Elimina un relevamiento y sus tiempos asociados en una sola transacción.

        Primero borra los TiemposElemento hijos y luego la cabecera del
        relevamiento, garantizando integridad referencial (Regla 6).

        Args:
            id_relevamiento: ID del relevamiento a eliminar.

        Returns:
            True si la cabecera fue eliminada exitosamente, False en caso contrario.

        Raises:
            No lanza excepciones al exterior; registra en logger (Regla 7).
        """
        from database import get_db_connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "DELETE FROM TiemposElemento WHERE id_relevamiento = ?",
                    (id_relevamiento,)
                )
                cursor.execute(
                    "DELETE FROM Relevamientos WHERE id_relevamiento = ?",
                    (id_relevamiento,)
                )
                eliminado = cursor.rowcount > 0
                conn.commit()
                if eliminado:
                    logger.info(f"Relevamiento {id_relevamiento} eliminado (cabecera + tiempos).")
                else:
                    logger.warning(f"No se encontró relevamiento {id_relevamiento} para eliminar.")
                return eliminado
            except Exception:
                conn.rollback()
                logger.exception(f"Error transaccional al eliminar relevamiento {id_relevamiento}. Rollback ejecutado.")
                return False
            finally:
                cursor.close()


class UsuarioDAO:
    @staticmethod
    def obtener_por_username(username: str) -> Optional[Usuario]:
        """Obtiene un usuario (con su rol) mediante consulta parametrizada."""
        query = """
            SELECT u.id_usuario, u.username, u.password_hash, r.nombre AS rol, u.nombre
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            WHERE u.username = ?
        """
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (username,))
                row = cursor.fetchone()
                if row:
                    # En modelos.py: id_usuario, username, password_hash, rol, nombre
                    from modelos import Usuario # Import local para evitar circularidad si la hubiera
                    return Usuario(id_usuario=row[0], username=row[1], password_hash=row[2], rol=row[3], nombre=row[4])
                return None
        except Exception:
            logger.exception("Fallo al obtener usuario por username.")
            return None

    @staticmethod
    def crear_usuario(username: str, password_hash: str, rol: str, nombre: str) -> bool:
        """Crea un nuevo usuario asignando el id_rol correspondiente."""
        query = """
            INSERT INTO Usuarios (username, password_hash, id_rol, nombre)
            VALUES (?, ?, (SELECT id_rol FROM Roles WHERE nombre = ?), ?)
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (username, password_hash, rol, nombre))
                return True
        except Exception:
            logger.exception(f"Fallo al crear el usuario: {username}")
            return False

    @staticmethod
    def obtener_metodistas() -> List['Usuario']:
        """Obtiene la lista de usuarios con rol METODISTA."""
        query = """
            SELECT u.id_usuario, u.username, u.password_hash, r.nombre AS rol, u.nombre
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            WHERE r.nombre = 'METODISTA'
        """
        metodistas = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                from modelos import Usuario
                for row in cursor.fetchall():
                    metodistas.append(Usuario(id_usuario=row[0], username=row[1], password_hash=row[2], rol=row[3], nombre=row[4]))
        except Exception:
            logger.exception("Fallo al obtener la lista de metodistas.")
        return metodistas

    @staticmethod
    def obtener_por_nombre_completo(nombre: str) -> Optional[Usuario]:
        """
        Obtiene un usuario buscando por su nombre completo (campo 'nombre').

        Realiza un INNER JOIN con Roles para recuperar el nombre del rol
        asociado, idéntico al patrón de obtener_por_username.
        Utiliza consulta parametrizada (Regla 6).

        Args:
            nombre: Nombre completo del usuario a buscar (coincidencia exacta).

        Returns:
            Instancia de Usuario si se encuentra, None en caso contrario.

        Raises:
            No lanza excepciones al exterior; registra en logger (Regla 7).
        """
        query = """
            SELECT u.id_usuario, u.username, u.password_hash, r.nombre AS rol, u.nombre
            FROM Usuarios u
            INNER JOIN Roles r ON u.id_rol = r.id_rol
            WHERE u.nombre = ?
        """
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (nombre,))
                row = cursor.fetchone()
                if row:
                    from modelos import Usuario
                    return Usuario(
                        id_usuario=row[0],
                        username=row[1],
                        password_hash=row[2],
                        rol=row[3],
                        nombre=row[4],
                    )
                return None
        except Exception:
            logger.exception("Fallo al obtener usuario por nombre completo.")
            return None

    @staticmethod
    def actualizar_password(id_usuario: int, nuevo_hash: str) -> bool:
        """
        Actualiza el hash de contraseña de un usuario existente.

        Ejecuta un UPDATE parametrizado con commit explícito (Regla 6).
        Destinado al flujo de blanqueo/recuperación de contraseña.

        Args:
            id_usuario: ID del usuario cuya contraseña se actualiza.
            nuevo_hash: Nuevo hash bcrypt de la contraseña.

        Returns:
            True si la actualización afectó al menos una fila, False en caso contrario.

        Raises:
            No lanza excepciones al exterior; registra en logger (Regla 7).
        """
        query = "UPDATE Usuarios SET password_hash = ? WHERE id_usuario = ?"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (nuevo_hash, id_usuario))
                actualizado: bool = cursor.rowcount > 0
                if actualizado:
                    logger.info(f"Contraseña actualizada para id_usuario={id_usuario}.")
                else:
                    logger.warning(f"No se encontró id_usuario={id_usuario} para actualizar contraseña.")
                return actualizado
        except Exception:
            logger.exception(f"Fallo al actualizar contraseña para id_usuario={id_usuario}.")
            return False

class TareaDAO:
    @staticmethod
    def obtener_todas() -> List['Tarea']:
        """Obtiene todas las tareas/solicitudes de la BD."""
        # Se asume que id_usuario_asignado ya existe en BD tras el ALTER TABLE
        query = "SELECT id_tarea, titulo, descripcion, estado, fecha, informe_url, id_usuario_asignado FROM Tareas"
        tareas = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                from modelos import Tarea
                for row in cursor.fetchall():
                    # Para prevenir crash si la columna aún no existe, capturamos el índice seguro
                    try:
                        id_asig = row[6]
                    except IndexError:
                        id_asig = None
                        
                    tareas.append(Tarea(
                        id_tarea=row[0], titulo=row[1], descripcion=row[2],
                        estado=row[3], fecha=str(row[4]), informe_url=row[5] or "",
                        id_usuario_asignado=id_asig
                    ))
        except Exception:
            logger.exception("Fallo al obtener tareas.")
        return tareas

    @staticmethod
    def obtener_tareas_por_usuario(id_usuario: int) -> List['Tarea']:
        """Obtiene solo las tareas asignadas a un metodista."""
        query = "SELECT id_tarea, titulo, descripcion, estado, fecha, informe_url, id_usuario_asignado FROM Tareas WHERE id_usuario_asignado = ?"
        tareas = []
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (id_usuario,))
                from modelos import Tarea
                for row in cursor.fetchall():
                    tareas.append(Tarea(
                        id_tarea=row[0], titulo=row[1], descripcion=row[2],
                        estado=row[3], fecha=str(row[4]), informe_url=row[5] or "",
                        id_usuario_asignado=row[6]
                    ))
        except Exception:
            logger.exception("Fallo al obtener tareas por usuario.")
        return tareas

    @staticmethod
    def crear_tarea(titulo: str, descripcion: str, id_usuario_asignado: int) -> bool:
        """Crea una nueva solicitud de relevamiento (Tarea) en estado Pendiente."""
        query = """
            INSERT INTO Tareas (titulo, descripcion, id_usuario_asignado, estado)
            VALUES (?, ?, ?, 'Pendiente')
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (titulo, descripcion, id_usuario_asignado))
                return True
        except Exception:
            logger.exception("Fallo al crear la tarea.")
            return False

    @staticmethod
    def borrar_tarea(id_tarea: int) -> bool:
        """Elimina una tarea permanentemente de la BD."""
        query = "DELETE FROM Tareas WHERE id_tarea = ?"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (id_tarea,))
                return cursor.rowcount > 0
        except Exception:
            logger.exception("Fallo al borrar la tarea.")
            return False

    @staticmethod
    def actualizar_estado(id_tarea: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una tarea."""
        query = "UPDATE Tareas SET estado = ? WHERE id_tarea = ?"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (nuevo_estado, id_tarea))
                return cursor.rowcount > 0
        except Exception:
            logger.exception("Fallo al actualizar el estado de la tarea.")
            return False

class AuditoriaDAO:
    @staticmethod
    def insertar_log(id_usuario: Optional[int], accion: str) -> bool:
        """Inserta un registro en LogsAuditoria de manera transaccional."""
        query = "INSERT INTO LogsAuditoria (id_usuario, accion) VALUES (?, ?)"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (id_usuario, accion))
                return True
        except Exception:
            logger.exception("Error crítico al guardar log de auditoría.")
            return False
    @staticmethod
    def actualizar_estado(id_tarea: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una tarea."""
        query = "UPDATE Tareas SET estado = ? WHERE id_tarea = ?"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (nuevo_estado, id_tarea))
                return cursor.rowcount > 0
        except Exception:
            logger.exception("Fallo al actualizar el estado de la tarea.")
            return False

class AuditoriaDAO:
    @staticmethod
    def insertar_log(id_usuario: Optional[int], accion: str) -> bool:
        """Inserta un registro en LogsAuditoria de manera transaccional."""
        query = "INSERT INTO LogsAuditoria (id_usuario, accion) VALUES (?, ?)"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (id_usuario, accion))
                return True
        except Exception:
            logger.exception("Error crítico al guardar log de auditoría.")
            return False
