"""
Thread para executar checkup em background
"""
import sys
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from modules.checkup.services.checkup_service import CheckupService


class CheckupThread(QThread):
    """Thread para executar checkup em background"""
    
    finished = pyqtSignal(dict)
    
    def __init__(self, auto_fix=True):
        super().__init__()
        self.auto_fix = auto_fix
        self.checkup_service = CheckupService()
    
    def run(self):
        """Executa o checkup"""
        try:
            result = self.checkup_service.run_full_checkup(auto_fix=self.auto_fix)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit({
                'error': str(e),
                'issues_found': 0,
                'fixes_applied': {}
            })
