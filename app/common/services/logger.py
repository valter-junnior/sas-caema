"""
Serviço de logging para o SAS-Caema
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import LOG_CONFIG


class LoggerService:
    """Serviço centralizado de logging"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger principal"""
        # Cria o logger
        self.logger = logging.getLogger('SAS_Caema')
        self.logger.setLevel(getattr(logging, LOG_CONFIG['level']))
        
        # Remove handlers existentes
        self.logger.handlers = []
        
        # Handler para arquivo com rotação
        file_handler = RotatingFileHandler(
            LOG_CONFIG['file'],
            maxBytes=LOG_CONFIG['max_bytes'],
            backupCount=LOG_CONFIG['backup_count'],
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, LOG_CONFIG['level']))
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            LOG_CONFIG['format'],
            datefmt=LOG_CONFIG['date_format']
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adiciona handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self, name: str = None):
        """Retorna um logger"""
        if name:
            return logging.getLogger(f'SAS_Caema.{name}')
        return self.logger
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log de informação"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log de erro"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log crítico"""
        self.logger.critical(message)


# Instância global
logger_service = LoggerService()
