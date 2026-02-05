"""
Serviço de logging para o SAS-Caema
Com rotação diária e limpeza automática de logs antigos
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import sys
import os
import glob
from datetime import datetime, timedelta

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
        
        # Handler para arquivo com rotação diária
        # Rotaciona à meia-noite e mantém backups
        file_handler = TimedRotatingFileHandler(
            LOG_CONFIG['file'],
            when='midnight',
            interval=1,
            backupCount=LOG_CONFIG.get('backup_days', 7),
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, LOG_CONFIG['level']))
        
        # Adiciona sufixo de data nos arquivos rotacionados
        file_handler.suffix = '%Y-%m-%d'
        
        # Limpa logs antigos (> 7 dias)
        self._cleanup_old_logs()
        
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
    
    def _cleanup_old_logs(self):
        """Remove logs com mais de 7 dias"""
        try:
            log_dir = Path(LOG_CONFIG['file']).parent
            log_pattern = Path(LOG_CONFIG['file']).stem + '*'
            
            # Calcula data limite (7 dias atrás)
            cutoff_date = datetime.now() - timedelta(days=LOG_CONFIG.get('backup_days', 7))
            
            # Busca todos os arquivos de log
            for log_file in log_dir.glob(log_pattern):
                if log_file == Path(LOG_CONFIG['file']):
                    # Não remove o arquivo principal
                    continue
                
                try:
                    # Verifica a data de modificação do arquivo
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    
                    if file_time < cutoff_date:
                        log_file.unlink()
                        self.logger.info(f"Log antigo removido: {log_file.name}")
                        
                except Exception as e:
                    # Se houver erro ao processar um arquivo, continua com os outros
                    pass
                    
        except Exception as e:
            # Se houver erro geral na limpeza, apenas registra mas não falha
            pass
    
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
