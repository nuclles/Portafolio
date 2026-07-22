import logging
import config

def get_logger(name: str) -> logging.Logger:
    """
    Configura y devuelve una instancia de logger centralizada.
    
    Aplica la Regla 7: Reemplaza prints por logging silencioso y robusto.
    
    Args:
        name (str): Nombre del módulo que solicita el logger.
        
    Returns:
        logging.Logger: Instancia del logger configurado.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Console handler (para desarrollo, aunque sin prints sueltos)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger
