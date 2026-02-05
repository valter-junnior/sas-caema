"""
Gerenciador de inicialização automática no Windows
"""
import sys
import winreg
from pathlib import Path

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import STARTUP_REGISTRY_KEY, STARTUP_REGISTRY_VALUE
from common.services.logger import logger_service


class StartupManager:
    """Gerencia a inicialização automática no Windows"""
    
    @staticmethod
    def is_enabled() -> bool:
        """Verifica se está configurado para iniciar com Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, STARTUP_REGISTRY_VALUE)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def enable() -> bool:
        """Ativa inicialização com Windows"""
        try:
            # Caminho do executável atual
            if getattr(sys, 'frozen', False):
                # Rodando como .exe
                exe_path = sys.executable
            else:
                # Rodando como script - usa pythonw para não abrir console
                exe_path = f'"{sys.executable}" "{Path(__file__).parent.parent.absolute() / "app.py"}"'
            
            # Adiciona argumento --startup para modo silencioso
            command = f'"{exe_path}" --startup'
            
            # Abre registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Define valor
            winreg.SetValueEx(
                key,
                STARTUP_REGISTRY_VALUE,
                0,
                winreg.REG_SZ,
                command
            )
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            logger_service.error(f"Erro ao ativar startup: {e}")
            return False
    
    @staticmethod
    def disable() -> bool:
        """Desativa inicialização com Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.DeleteValue(key, STARTUP_REGISTRY_VALUE)
            winreg.CloseKey(key)
            return True
            
        except FileNotFoundError:
            return True  # Já não estava configurado
        except Exception as e:
            logger_service.error(f"Erro ao desativar startup: {e}")
            return False
