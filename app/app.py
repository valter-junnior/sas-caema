"""
Aplicação principal do SAS-Caema
Interface gráfica com PyQt5
"""
import sys
import argparse
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.checkup.services.checkup_service import CheckupService
from common.views.main_window import MainWindow


def run_startup_checkup():
    """Executa checkup em modo silencioso (inicialização)"""
    logger = logger_service.get_logger('Startup')
    logger.info("=== Checkup Automático (Inicialização) ===")
    
    try:
        service = CheckupService()
        result = service.run_full_checkup(auto_fix=True)
        
        issues = result.get('issues_found', 0)
        fixes = result.get('fixes_applied', {})
        
        if issues == 0:
            logger.info("✓ Sistema OK - Nenhum problema encontrado")
        else:
            fixed = sum(1 for success in fixes.values() if success)
            logger.info(f"⚠ {issues} problema(s) - {fixed} corrigido(s)")
            
            # Mostra notificação se houver problemas
            try:
                from winotify import Notification, audio
                
                if fixed == len(fixes):
                    # Todos corrigidos
                    toast = Notification(
                        app_id="SAS-Caema",
                        title="Checkup Concluído",
                        msg=f"✓ {fixed} problema(s) corrigido(s) automaticamente.",
                        duration="short"
                    )
                else:
                    # Alguns problemas persistem
                    toast = Notification(
                        app_id="SAS-Caema",
                        title="Checkup - Atenção",
                        msg=f"{issues} problema(s) detectado(s).\nAbra SAS-Caema para detalhes.",
                        duration="long"
                    )
                
                toast.set_audio(audio.Default, loop=False)
                toast.show()
            except Exception as e:
                logger.error(f"Erro ao mostrar notificação: {e}")
        
        logger.info("=== Checkup Finalizado ===")
        
    except Exception as e:
        logger.error(f"Erro durante checkup: {e}")


def main():
    """Função principal"""
    # Parser de argumentos
    parser = argparse.ArgumentParser(description='SAS-Caema')
    parser.add_argument('--startup', action='store_true',
                       help='Executa em modo startup (checkup silencioso)')
    
    args = parser.parse_args()
    
    # Modo startup: executa checkup e sai
    if args.startup:
        run_startup_checkup()
        sys.exit(0)
    
    # Modo normal: abre GUI
    app = QApplication(sys.argv)
    
    # Define estilo da aplicação
    app.setStyle('Fusion')
    
    # Cria e mostra janela principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
