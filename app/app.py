"""
Aplicação principal do SAS-Caema
Interface gráfica com PyQt5
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QMessageBox, QProgressDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config import APP_NAME, APP_VERSION, PRIMARY_COLOR, SUCCESS_COLOR, ERROR_COLOR
from common.services.logger import logger_service
from modules.checkup.services.checkup_service import CheckupService


class CheckupThread(QThread):
    """Thread para executar checkup em background"""
    
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, auto_fix=True):
        super().__init__()
        self.auto_fix = auto_fix
        self.checkup_service = CheckupService()
    
    def run(self):
        """Executa o checkup"""
        try:
            self.progress.emit("Iniciando checkup...")
            result = self.checkup_service.run_full_checkup(auto_fix=self.auto_fix)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit({
                'error': str(e),
                'issues_found': 0,
                'fixes_applied': {}
            })


class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.logger = logger_service.get_logger('MainWindow')
        self.checkup_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        title_label = QLabel(APP_NAME)
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {PRIMARY_COLOR}; padding: 20px;")
        main_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Sistema de Automação de Suporte")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666; padding-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # Container de botões
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_container.setLayout(button_layout)
        
        # Botão: Rodar Checkup
        self.btn_checkup = QPushButton("🔍 Rodar Checkup")
        self.btn_checkup.setFont(QFont("Segoe UI", 14))
        self.btn_checkup.setMinimumHeight(60)
        self.btn_checkup.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton:pressed {{
                background-color: #004578;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
            }}
        """)
        self.btn_checkup.clicked.connect(self.run_checkup)
        button_layout.addWidget(self.btn_checkup)
        
        # Botão: Executar Solução (placeholder)
        self.btn_solution = QPushButton("⚙️ Executar Solução")
        self.btn_solution.setFont(QFont("Segoe UI", 14))
        self.btn_solution.setMinimumHeight(60)
        self.btn_solution.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #0E6A0E;
            }}
            QPushButton:pressed {{
                background-color: #0C5A0C;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
            }}
        """)
        self.btn_solution.clicked.connect(self.show_solutions)
        button_layout.addWidget(self.btn_solution)
        
        main_layout.addWidget(button_container)
        
        # Área de log
        log_label = QLabel("Log de Atividades:")
        log_label.setFont(QFont("Segoe UI", 10))
        log_label.setStyleSheet("padding-top: 20px;")
        main_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.log_text)
        
        # Barra de status
        self.statusBar().showMessage("Pronto")
        
        # Log inicial
        self.log("Aplicação iniciada com sucesso")
        self.log(f"Versão: {APP_VERSION}")
    
    def log(self, message: str):
        """Adiciona mensagem ao log"""
        self.log_text.append(f"[{self.get_timestamp()}] {message}")
        self.logger.info(message)
    
    def get_timestamp(self):
        """Retorna timestamp atual"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def run_checkup(self):
        """Executa o checkup em background"""
        self.log("Iniciando checkup do sistema...")
        self.btn_checkup.setEnabled(False)
        self.btn_solution.setEnabled(False)
        self.statusBar().showMessage("Executando checkup...")
        
        # Cria e inicia thread
        self.checkup_thread = CheckupThread(auto_fix=True)
        self.checkup_thread.progress.connect(self.log)
        self.checkup_thread.finished.connect(self.on_checkup_finished)
        self.checkup_thread.start()
    
    def on_checkup_finished(self, result: dict):
        """Callback quando checkup termina"""
        self.btn_checkup.setEnabled(True)
        self.btn_solution.setEnabled(True)
        
        if 'error' in result:
            self.log(f"Erro durante checkup: {result['error']}")
            self.statusBar().showMessage("Erro no checkup")
            QMessageBox.critical(self, "Erro", f"Erro ao executar checkup:\n{result['error']}")
            return
        
        issues = result.get('issues_found', 0)
        fixes = result.get('fixes_applied', {})
        
        self.log(f"\nCheckup concluído!")
        self.log(f"Problemas encontrados: {issues}")
        
        if fixes:
            self.log(f"Correções aplicadas: {len(fixes)}")
            for module, success in fixes.items():
                status = "✓" if success else "✗"
                self.log(f"  {status} {module}")
        
        # Mostra resultados detalhados
        if issues == 0:
            self.statusBar().showMessage("✓ Sistema OK")
            QMessageBox.information(
                self, 
                "Checkup Concluído",
                "✓ Nenhum problema encontrado!\n\nO sistema está funcionando corretamente."
            )
        else:
            self.statusBar().showMessage(f"Checkup concluído - {issues} problema(s)")
            
            fixed_count = sum(1 for success in fixes.values() if success)
            message = f"Checkup concluído!\n\n"
            message += f"Problemas encontrados: {issues}\n"
            message += f"Correções bem-sucedidas: {fixed_count}/{len(fixes)}"
            
            QMessageBox.information(self, "Checkup Concluído", message)
    
    def show_solutions(self):
        """Mostra menu de soluções disponíveis"""
        QMessageBox.information(
            self,
            "Executar Solução",
            "Funcionalidade em desenvolvimento.\n\n"
            "Em breve você poderá executar soluções específicas para problemas conhecidos."
        )
    
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        self.log("Encerrando aplicação...")
        event.accept()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    
    # Define estilo da aplicação
    app.setStyle('Fusion')
    
    # Cria e mostra janela principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
