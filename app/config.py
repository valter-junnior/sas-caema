"""
Arquivo de configuração global do SAS-Caema
"""
import os
import sys
from pathlib import Path

# Diretórios principais
BASE_DIR = Path(__file__).parent.absolute()
ASSETS_DIR = BASE_DIR / "assets"
MODULES_DIR = BASE_DIR / "modules"

# Diretório de logs e apps — ajusta automaticamente para executáveis
if getattr(sys, 'frozen', False):
    # Quando executando como .exe instalado - usa AppData para evitar problemas de permissão
    # Logs em C:\Users\{usuario}\AppData\Local\SAS-Caema\logs\
    appdata_local = os.environ.get('LOCALAPPDATA') or os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local')
    LOGS_DIR = Path(appdata_local) / "SAS-Caema" / "logs"
    APPS_DIR = Path(appdata_local) / "SAS-Caema" / "apps"
else:
    # Quando executando como script Python
    LOGS_DIR = BASE_DIR / "logs"
    APPS_DIR = BASE_DIR / "assets" / "apps"

# Criar diretórios se não existirem
LOGS_DIR.mkdir(parents=True, exist_ok=True)
APPS_DIR.mkdir(parents=True, exist_ok=True)

# Configurações da Aplicação
APP_NAME = "SAS - Caema"
APP_VERSION = "1.0.0"

# Configurações de UI
PRIMARY_COLOR = "#0078D4"  # Azul padrão do Windows
SUCCESS_COLOR = "#107C10"
ERROR_COLOR = "#E81123"

# Configurações de Papel de Parede
WALLPAPER_CONFIG = {
    "text_color": "#FFFFFF",  # Branco (para fundos escuros)
    "text_size": 20,  # Tamanho da fonte aumentado para melhor legibilidade
    "text_position": "top-right",  # top-right, top-left, bottom-right, bottom-left
    "font": "Arial",
    "background_image": ASSETS_DIR / "images" / "wallpaper.jpeg",
    "output_path": ASSETS_DIR / "images" / "wallpaper_generated.png",
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
    "backup_days": 7,  # Número de dias de logs a manter
}

# Configurações do Windows
STARTUP_REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
STARTUP_REGISTRY_VALUE = "SAS_Caema"
