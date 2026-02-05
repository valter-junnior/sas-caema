"""
Serviço de checkup - executa verificações do sistema
"""
from pathlib import Path
import sys
from typing import List, Dict

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service


class CheckupService:
    """Serviço que executa verificações no sistema"""
    
    def __init__(self):
        """Inicializa o serviço de checkup"""
        self.logger = logger_service.get_logger('CheckupService')
        self.modules = []
        self._load_modules()
    
    def _load_modules(self):
        """Carrega os módulos disponíveis para checkup"""
        try:
            # Importa módulo de wallpaper
            from modules.wallpaper.main import WallpaperModule
            self.modules.append({
                'id': 'wallpaper',
                'name': 'Papel de Parede',
                'module': WallpaperModule,
                'enabled': True
            })
            
            self.logger.info(f"Carregados {len(self.modules)} módulos de checkup")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar módulos: {e}")
    
    def run_checks(self) -> List[Dict]:
        """
        Executa todas as verificações
        
        Returns:
            Lista de resultados das verificações
        """
        results = []
        
        self.logger.info("=== Iniciando Checkup ===")
        
        for module_info in self.modules:
            if not module_info['enabled']:
                continue
            
            try:
                self.logger.info(f"Verificando: {module_info['name']}")
                
                # Instancia o módulo
                module = module_info['module']()
                
                # Executa verificação
                check_result = module.check()
                results.append(check_result)
                
                self.logger.info(f"  Status: {check_result['status']}")
                self.logger.info(f"  {check_result['message']}")
                
            except Exception as e:
                self.logger.error(f"Erro ao verificar {module_info['name']}: {e}")
                results.append({
                    'module': module_info['name'],
                    'status': 'error',
                    'message': str(e)
                })
        
        self.logger.info("=== Checkup Concluído ===")
        return results
    
    def fix_issues(self, results: List[Dict]) -> Dict[str, bool]:
        """
        Corrige problemas detectados
        
        Args:
            results: Resultados do checkup
            
        Returns:
            Dicionário com status de correção de cada módulo
        """
        fixes = {}
        
        self.logger.info("=== Corrigindo Problemas ===")
        
        for result in results:
            module_name = result.get('module', 'unknown')
            status = result.get('status', 'unknown')
            
            if status in ['needs_update', 'error']:
                try:
                    self.logger.info(f"Corrigindo: {module_name}")
                    
                    # Encontra o módulo correspondente
                    module_found = False
                    for module_info in self.modules:
                        if module_info['id'] == module_name:
                            module = module_info['module']()
                            success = module.execute()
                            fixes[module_name] = success
                            module_found = True
                            
                            if success:
                                self.logger.info(f"  ✓ {module_info['name']} corrigido com sucesso")
                            else:
                                self.logger.error(f"  ✗ Falha ao corrigir {module_info['name']}")
                            break
                    
                    if not module_found:
                        self.logger.error(f"  ✗ Módulo '{module_name}' não encontrado")
                        fixes[module_name] = False
                    
                except Exception as e:
                    self.logger.error(f"Erro ao corrigir {module_name}: {e}")
                    fixes[module_name] = False
        
        self.logger.info("=== Correções Concluídas ===")
        return fixes
    
    def run_full_checkup(self, auto_fix: bool = True) -> Dict:
        """
        Executa checkup completo e corrige problemas se solicitado
        
        Args:
            auto_fix: Se True, corrige problemas automaticamente
            
        Returns:
            Dicionário com resultados completos
        """
        # Executa verificações
        check_results = self.run_checks()
        
        # Conta problemas
        issues_count = sum(1 for r in check_results if r['status'] != 'ok')
        
        result = {
            'timestamp': None,
            'checks': check_results,
            'issues_found': issues_count,
            'fixes_applied': {}
        }
        
        # Corrige se solicitado
        if auto_fix and issues_count > 0:
            self.logger.info(f"\n{issues_count} problema(s) encontrado(s). Aplicando correções...")
            fixes = self.fix_issues(check_results)
            result['fixes_applied'] = fixes
        
        return result


if __name__ == "__main__":
    # Teste do serviço
    service = CheckupService()
    result = service.run_full_checkup(auto_fix=True)
    
    print("\n" + "="*50)
    print("RESUMO DO CHECKUP")
    print("="*50)
    print(f"Problemas encontrados: {result['issues_found']}")
    print(f"Correções aplicadas: {len(result['fixes_applied'])}")
    
    if result['fixes_applied']:
        print("\nStatus das correções:")
        for module, success in result['fixes_applied'].items():
            status = "✓" if success else "✗"
            print(f"  {status} {module}")
