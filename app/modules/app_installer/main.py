"""
Módulo principal do Instalador de Aplicativos.
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service


class AppInstallerModule:
    """Abre o dialog de instalação de aplicativos."""

    def __init__(self):
        self.logger = logger_service.get_logger('AppInstaller')

    def execute(self, parent=None):
        try:
            self.logger.info("Abrindo instalador de aplicativos...")
            from modules.app_installer.views.apps_dialog import AppsDialog
            dialog = AppsDialog(parent)
            dialog.exec_()
        except Exception as e:
            self.logger.error(f"Erro ao abrir instalador: {e}")
            import traceback
            traceback.print_exc()
