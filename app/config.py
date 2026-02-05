"""
Arquivo de configuração global do SAS-Caema
"""
import os
from pathlib import Path

# Diretórios principais
BASE_DIR = Path(__file__).parent.absolute()
ASSETS_DIR = BASE_DIR / "assets"
MODULES_DIR = BASE_DIR / "modules"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretório de logs se não existir
LOGS_DIR.mkdir(exist_ok=True)

# Configurações da Aplicação
APP_NAME = "SAS - Caema"
APP_VERSION = "1.0.0"

# Configurações de UI
UI_THEME = "light"  # light ou dark
PRIMARY_COLOR = "#0078D4"  # Azul padrão do Windows
SECONDARY_COLOR = "#005A9E"
SUCCESS_COLOR = "#107C10"
WARNING_COLOR = "#FF8C00"
ERROR_COLOR = "#E81123"

# Configurações de Papel de Parede
WALLPAPER_CONFIG = {
    "text_color": "#FFFFFF",  # Branco (para fundos escuros)
    "text_size": 14,
    "text_position": "top-right",  # top-right, top-left, bottom-right, bottom-left
    "font": "Arial",
    "background_image": ASSETS_DIR / "wallpaper_base.png",
    "output_path": ASSETS_DIR / "wallpaper_generated.png",
    "padding": 20,  # Pixels de padding do texto nas bordas
}

# Configurações de Checkup
CHECKUP_CONFIG = {
    "auto_run_on_startup": True,
    "notification_duration": 5000,  # milissegundos
    "retry_on_error": True,
    "max_retries": 3,
}

# Configurações de Logs
LOG_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "file": LOGS_DIR / "sas_caema.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5,
}

# Configurações do Windows
STARTUP_REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
STARTUP_REGISTRY_VALUE = "SAS_Caema"
