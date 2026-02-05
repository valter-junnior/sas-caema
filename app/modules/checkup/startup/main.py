"""
Modo Startup - Checkup com feedback visual na inicialização do Windows
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.checkup.services.checkup_service import CheckupService
from modules.checkup.startup.startup_feedback import StartupFeedbackWindow


class StartupCheckupThread(QThread):
    """Thread para executar checkup com feedback de progresso"""
    
    checking_module = pyqtSignal(str, int)  # nome_modulo, progresso
    fixing_module = pyqtSignal(str, int)    # nome_modulo, progresso
    finished_success = pyqtSignal(str)      # mensagem
    finished_partial = pyqtSignal(int, int) # corrigidos, total
    finished_error = pyqtSignal(str)        # erro
    
    def __init__(self):
        super().__init__()
        self.checkup_service = CheckupService()
        self.logger = logger_service.get_logger('StartupCheckup')
    
    def run(self):
        """Executa o checkup com feedback de progresso"""
        try:
            self.logger.info("=== Checkup Automático (Inicialização) ===")
            
            # Fase 1: Verificação (0-50%)
            self.checking_module.emit("Carregando módulos...", 10)
            
            # Carrega módulos
            modules = self.checkup_service.modules
            total_modules = len(modules)
            
            if total_modules == 0:
                self.finished_error.emit("Nenhum módulo disponível")
                return
            
            # Executa verificações
            checks_results = []
            for idx, module_info in enumerate(modules):
                module_name = module_info['name']
                progress = 10 + int((idx / total_modules) * 40)
                
                self.checking_module.emit(module_name, progress)
                self.logger.info(f"Verificando: {module_name}")
                
                try:
                    module = module_info['module']()
                    check_result = module.check()
                    checks_results.append(check_result)
                    
                    self.logger.info(f"  Status: {check_result['status']}")
                except Exception as e:
                    self.logger.error(f"Erro ao verificar {module_name}: {e}")
                    checks_results.append({
                        'module': module_info['id'],
                        'status': 'error',
                        'message': str(e)
                    })
            
            # Analisa resultados
            issues_found = sum(1 for r in checks_results if r['status'] != 'ok')
            
            if issues_found == 0:
                self.logger.info("Sistema OK - Nenhum problema encontrado")
                self.finished_success.emit("Sistema verificado com sucesso!")
                return
            
            # Fase 2: Correção (50-100%)
            self.logger.info(f"Encontrados {issues_found} problema(s). Aplicando correções...")
            
            fixes_applied = {}
            fixed_count = 0
            
            for idx, result in enumerate(checks_results):
                if result['status'] not in ['needs_update', 'error']:
                    continue
                
                module_id = result.get('module', 'unknown')
                
                # Encontra o módulo
                module_info = next((m for m in modules if m['id'] == module_id), None)
                if not module_info:
                    continue
                
                module_name = module_info['name']
                progress = 50 + int((idx / issues_found) * 50)
                
                self.fixing_module.emit(module_name, progress)
                self.logger.info(f"Corrigindo: {module_name}")
                
                try:
                    module = module_info['module']()
                    success = module.execute()
                    fixes_applied[module_id] = success
                    
                    if success:
                        fixed_count += 1
                        self.logger.info(f"  ✓ {module_name} corrigido com sucesso")
                    else:
                        self.logger.error(f"  ✗ Falha ao corrigir {module_name}")
                        
                except Exception as e:
                    self.logger.error(f"  ✗ Erro ao corrigir {module_name}: {e}")
                    fixes_applied[module_id] = False
            
            # Resultado final
            if fixed_count == issues_found:
                self.logger.info(f"✓ Todos os {fixed_count} problema(s) foram corrigidos")
                self.finished_success.emit(f"{fixed_count} problema(s) corrigido(s)!")
            else:
                self.logger.info(f"⚠ {fixed_count} de {issues_found} problema(s) corrigidos")
                self.finished_partial.emit(fixed_count, issues_found)
            
            self.logger.info("=== Checkup Finalizado ===")
            
        except Exception as e:
            self.logger.error(f"Erro crítico durante checkup: {e}")
            self.finished_error.emit(f"Erro: {str(e)}")


def main():
    """Função principal do modo startup"""
    # Cria aplicação Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Cria janela de feedback
    feedback_window = StartupFeedbackWindow()
    
    # Cria thread de checkup
    checkup_thread = StartupCheckupThread()
    
    # Conecta sinais
    checkup_thread.checking_module.connect(feedback_window.show_checking)
    checkup_thread.fixing_module.connect(feedback_window.show_fixing)
    checkup_thread.finished_success.connect(feedback_window.show_success)
    checkup_thread.finished_partial.connect(feedback_window.show_partial_success)
    checkup_thread.finished_error.connect(feedback_window.show_error)
    
    # Quando a janela fechar, encerra a aplicação
    feedback_window.closed.connect(app.quit)
    
    # Mostra janela e inicia checkup
    feedback_window.show()
    checkup_thread.start()
    
    # Executa aplicação
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
