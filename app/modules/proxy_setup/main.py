"""
Módulo principal do Proxy Setup
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service


class ProxySetupModule:
    """Classe principal do módulo de configuração de proxy"""

    def __init__(self):
        self.logger = logger_service.get_logger('ProxySetup')

    def execute(self) -> bool:
        """
        Executa o wizard de configuração de proxy

        Returns:
            True se o wizard foi concluído com sucesso, False caso contrário
        """
        try:
            self.logger.info("Iniciando wizard de configuração de proxy...")

            from modules.proxy_setup.views.wizard_window import ProxyWizardWindow

            wizard = ProxyWizardWindow()
            result = wizard.exec_()

            self.logger.info(f"Wizard de proxy concluído com resultado: {result}")
            return result == 1  # QDialog.Accepted

        except Exception as e:
            self.logger.error(f"Erro ao executar wizard de proxy: {e}")
            import traceback
            traceback.print_exc()
            return False

    def check(self) -> dict:
        """
        Verifica status atual do proxy configurado

        Returns:
            Dicionário com status da verificação
        """
        try:
            from modules.proxy_setup.services.proxy_service import ProxyService

            service = ProxyService()
            current = service.get_current_proxy()
            from modules.proxy_setup import config

            expected = config.PROXY_SERVER
            is_set = current == expected

            return {
                'module': 'Proxy Setup',
                'status': 'ok' if is_set else 'warning',
                'message': f'Proxy configurado: {current}' if is_set else f'Proxy não configurado (atual: {current or "nenhum"})',
            }

        except Exception as e:
            self.logger.error(f"Erro ao verificar proxy: {e}")
            return {
                'module': 'Proxy Setup',
                'status': 'error',
                'message': str(e),
            }
