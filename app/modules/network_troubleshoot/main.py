"""
Módulo principal do Network Troubleshoot
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service


class NetworkTroubleshootModule:
    """Classe principal do módulo de troubleshooting de rede"""
    
    def __init__(self):
        """Inicializa o módulo"""
        self.logger = logger_service.get_logger('NetworkTroubleshoot')
    
    def execute(self) -> bool:
        """
        Executa o wizard de troubleshooting de rede
        
        Returns:
            True se o wizard foi completado, False caso contrário
        """
        try:
            self.logger.info("Iniciando wizard de troubleshooting de rede...")
            
            # Importa a janela do wizard
            from modules.network_troubleshoot.views.wizard_window import WizardWindow
            
            # Cria e exibe o wizard
            wizard = WizardWindow()
            result = wizard.exec_()
            
            self.logger.info(f"Wizard concluído com resultado: {result}")
            return result == 1  # QDialog.Accepted
            
        except Exception as e:
            self.logger.error(f"Erro ao executar wizard: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def check(self) -> dict:
        """
        Verifica status atual da conectividade
        Este método não é usado neste módulo (é opcional)
        
        Returns:
            Dicionário com status da verificação
        """
        try:
            from modules.network_troubleshoot.services.network_checker import NetworkChecker
            
            checker = NetworkChecker()
            is_connected = checker.check_internet_connectivity()
            
            return {
                'module': 'Network Troubleshoot',
                'status': 'ok' if is_connected else 'error',
                'message': 'Conectividade OK' if is_connected else 'Sem conectividade'
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar conectividade: {e}")
            return {
                'module': 'Network Troubleshoot',
                'status': 'error',
                'message': str(e)
            }
