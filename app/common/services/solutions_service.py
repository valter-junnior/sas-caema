"""
Serviço de gerenciamento de soluções de troubleshooting
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service


class SolutionsService:
    """Serviço que gerencia soluções de troubleshooting disponíveis"""
    
    def __init__(self):
        """Inicializa o serviço de soluções"""
        self.logger = logger_service.get_logger('SolutionsService')
        self.solutions = []
        self._load_solutions()
    
    def _load_solutions(self):
        """Carrega as soluções disponíveis"""
        try:
            # Registra módulo de network troubleshoot
            from modules.network_troubleshoot.main import NetworkTroubleshootModule
            
            self.solutions.append({
                'id': 'network_troubleshoot',
                'name': 'Verificação de Cabos de Rede',
                'description': 'Wizard passo-a-passo para diagnóstico de problemas de conectividade',
                'module': NetworkTroubleshootModule,
                'enabled': True,
                'icon': '🔌'
            })
            
            # Adicione mais soluções aqui no futuro
            # Exemplo:
            # self.solutions.append({
            #     'id': 'printer_troubleshoot',
            #     'name': 'Verificação de Impressora',
            #     'description': 'Diagnóstico de problemas com impressoras',
            #     'module': PrinterTroubleshootModule,
            #     'enabled': True,
            #     'icon': '🖨️'
            # })
            
            self.logger.info(f"Carregadas {len(self.solutions)} soluções de troubleshooting")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar soluções: {e}")
    
    def get_available_solutions(self) -> list:
        """
        Retorna lista de soluções disponíveis
        
        Returns:
            Lista de dicionários com informações das soluções
        """
        available = [s for s in self.solutions if s['enabled']]
        self.logger.debug(f"Retornando {len(available)} soluções disponíveis")
        return available
    
    def execute_solution(self, solution_id: str) -> bool:
        """
        Executa uma solução específica
        
        Args:
            solution_id: ID da solução a executar
            
        Returns:
            True se executou com sucesso, False caso contrário
        """
        try:
            # Busca a solução pelo ID
            solution = next((s for s in self.solutions if s['id'] == solution_id), None)
            
            if not solution:
                self.logger.error(f"Solução não encontrada: {solution_id}")
                return False
            
            if not solution['enabled']:
                self.logger.warning(f"Solução desabilitada: {solution_id}")
                return False
            
            self.logger.info(f"Executando solução: {solution['name']}")
            
            # Instancia e executa o módulo
            module = solution['module']()
            result = module.execute()
            
            self.logger.info(f"Solução '{solution['name']}' executada: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao executar solução {solution_id}: {e}")
            import traceback
            traceback.print_exc()
            return False


# Instância global do serviço
solutions_service = SolutionsService()
