"""
Módulo principal do Checkup
Executado na inicialização do sistema
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from modules.checkup.services.checkup_service import CheckupService
from common.services.logger import logger_service
from config import CHECKUP_CONFIG


class CheckupModule:
    """Classe principal do módulo de checkup"""
    
    def __init__(self, silent_mode: bool = False):
        """
        Inicializa o módulo
        
        Args:
            silent_mode: Se True, executa sem mostrar janelas (para startup)
        """
        self.silent_mode = silent_mode
        self.logger = logger_service.get_logger('CheckupModule')
        self.service = CheckupService()
    
    def run(self):
        """Executa o checkup"""
        try:
            if self.silent_mode:
                self.logger.info("Executando checkup em modo silencioso (startup)")
            else:
                self.logger.info("Executando checkup")
            
            # Executa checkup completo com auto-fix
            result = self.service.run_full_checkup(
                auto_fix=CHECKUP_CONFIG.get('auto_run_on_startup', True)
            )
            
            issues = result.get('issues_found', 0)
            
            if issues == 0:
                self.logger.info("Checkup concluído - sistema OK")
                if not self.silent_mode:
                    self._show_success_notification()
            else:
                fixes = result.get('fixes_applied', {})
                fixed_count = sum(1 for success in fixes.values() if success)
                
                self.logger.warning(f"Checkup concluído - {issues} problema(s), {fixed_count} corrigido(s)")
                
                # Se houver problemas não resolvidos, mostrar notificação
                if fixed_count < len(fixes):
                    self._show_warning_notification(issues, fixed_count)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao executar checkup: {e}")
            if not self.silent_mode:
                self._show_error_notification(str(e))
            return None
    
    def _show_success_notification(self):
        """Mostra notificação de sucesso"""
        try:
            from winotify import Notification, audio
            
            toast = Notification(
                app_id="SAS-Caema",
                title="Checkup Concluído",
                msg="Sistema verificado com sucesso! Tudo está funcionando corretamente.",
                duration="short"
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            
        except Exception as e:
            self.logger.error(f"Erro ao mostrar notificação: {e}")
    
    def _show_warning_notification(self, issues: int, fixed: int):
        """Mostra notificação de aviso"""
        try:
            from winotify import Notification, audio
            
            toast = Notification(
                app_id="SAS-Caema",
                title="Checkup - Atenção Necessária",
                msg=f"{issues} problema(s) detectado(s). {fixed} corrigido(s) automaticamente.\n"
                    f"Abra o SAS-Caema para mais detalhes.",
                duration="long"
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            
        except Exception as e:
            self.logger.error(f"Erro ao mostrar notificação: {e}")
    
    def _show_error_notification(self, error_msg: str):
        """Mostra notificação de erro"""
        try:
            from winotify import Notification, audio
            
            toast = Notification(
                app_id="SAS-Caema",
                title="Erro no Checkup",
                msg=f"Ocorreu um erro durante o checkup: {error_msg}",
                duration="long"
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
            
        except Exception as e:
            self.logger.error(f"Erro ao mostrar notificação: {e}")


def main():
    """Função principal para execução standalone"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Módulo de Checkup SAS-Caema')
    parser.add_argument('--silent', action='store_true', 
                       help='Executa em modo silencioso (para startup)')
    
    args = parser.parse_args()
    
    module = CheckupModule(silent_mode=args.silent)
    result = module.run()
    
    if result and result.get('issues_found', 0) == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
