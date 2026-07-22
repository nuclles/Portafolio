import bcrypt
from logger import get_logger
from dao import AuditoriaDAO

logger = get_logger(__name__)

class Seguridad:
    """
    Clase utilitaria para el manejo de la criptografía de contraseñas
    y auditoría de la aplicación.
    """
    
    @staticmethod
    def generar_hash(password_plano: str) -> str:
        """
        Genera un hash seguro utilizando bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_plano.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verificar_password(password_plano: str, password_hash: str) -> bool:
        """
        Verifica una contraseña en texto plano contra su hash almacenado.
        """
        try:
            return bcrypt.checkpw(password_plano.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            logger.exception("Error al verificar hash bcrypt (posible formato inválido).")
            return False

    @staticmethod
    def registrar_auditoria(id_usuario: int, accion: str) -> bool:
        """
        Registra una acción en la tabla LogsAuditoria.
        
        Args:
            id_usuario: ID del usuario que realiza la acción.
            accion: Descripción de la acción realizada.
            
        Returns:
            bool: True si el registro fue exitoso.
        """
        try:
            return AuditoriaDAO.insertar_log(id_usuario, accion)
        except Exception:
            logger.exception("Fallo al registrar auditoría en la capa de seguridad.")
            return False
