"""
Janela principal da aplicação
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QAction, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import APP_NAME, APP_VERSION, PRIMARY_COLOR, SUCCESS_COLOR
from common.services.logger import logger_service
from common.services.solutions_service import solutions_service
from modules.checkup.threads.checkup_thread import CheckupThread
from common.views.dialogs import ResultDialogs
from common.views.solutions_dialog import SolutionsDialog


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
        
        # Cria menu
        self.create_menu()
        
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
        subtitle_label.setStyleSheet("color: #666666; padding-bottom: 40px;")
        main_layout.addWidget(subtitle_label)
        
        # Container de botões em duas colunas
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_container.setLayout(button_layout)
        
        # Botão: Rodar Checkup
        self.btn_checkup = QPushButton("Rodar Checkup")
        self.btn_checkup.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_checkup.setMinimumHeight(120)
        self.btn_checkup.setMinimumWidth(250)
        self.btn_checkup.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton:pressed {{
                background-color: #004578;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
        """)
        self.btn_checkup.clicked.connect(self.run_checkup)
        button_layout.addWidget(self.btn_checkup)
        
        # Botão: Executar Solução (placeholder)
        self.btn_solution = QPushButton("Executar Solução")
        self.btn_solution.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_solution.setMinimumHeight(120)
        self.btn_solution.setMinimumWidth(250)
        self.btn_solution.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #0E6A0E;
            }}
            QPushButton:pressed {{
                background-color: #0C5A0C;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
        """)
        self.btn_solution.clicked.connect(self.show_solutions)
        button_layout.addWidget(self.btn_solution)
        
        main_layout.addWidget(button_container)
        
        # Adiciona espaçamento flexível
        main_layout.addStretch()
        
        # Barra de status
        self.statusBar().showMessage("Pronto")
        
        # Log no arquivo (não visual)
        self.logger.info("Aplicação iniciada com sucesso")
        self.logger.info(f"Versão: {APP_VERSION}")
    
    def create_menu(self):
        """Cria a barra de menu"""
        menubar = self.menuBar()
        
        # Menu Configurações
        config_menu = menubar.addMenu('⚙️ Configurações')
        
        # Opção Sobre
        about_action = QAction('Sobre', self)
        about_action.triggered.connect(self.show_about)
        config_menu.addAction(about_action)
    
    def show_about(self):
        """Mostra informações sobre o app"""
        QMessageBox.about(
            self,
            "Sobre SAS-Caema",
            f"<h2>{APP_NAME}</h2>"
            f"<p><b>Versão:</b> {APP_VERSION}</p>"
            f"<p><b>Sistema de Automação de Suporte</b></p>"
            f"<p>Desenvolvido para Caema</p>"
            f"<p>© 2026</p>"
        )
    
    def run_checkup(self):
        """Executa o checkup em background"""
        self.logger.info("Iniciando checkup do sistema...")
        self.btn_checkup.setEnabled(False)
        self.btn_solution.setEnabled(False)
        self.statusBar().showMessage("Executando checkup...")
        
        # Cria e inicia thread
        self.checkup_thread = CheckupThread(auto_fix=True)
        self.checkup_thread.finished.connect(self.on_checkup_finished)
        self.checkup_thread.start()
    
    def on_checkup_finished(self, result: dict):
        """Callback quando checkup termina"""
        self.btn_checkup.setEnabled(True)
        self.btn_solution.setEnabled(True)
        
        if 'error' in result:
            self.logger.error(f"Erro durante checkup: {result['error']}")
            self.statusBar().showMessage("Erro no checkup")
            ResultDialogs.show_error_dialog(self, result['error'])
            return
        
        issues = result.get('issues_found', 0)
        fixes = result.get('fixes_applied', {})
        checks = result.get('checks', [])
        
        self.logger.info(f"Checkup concluído!")
        self.logger.info(f"Problemas encontrados: {issues}")
        
        if fixes:
            self.logger.info(f"Correções aplicadas: {len(fixes)}")
            for module, success in fixes.items():
                status = "✓" if success else "✗"
                self.logger.info(f"  {status} {module}")
        
        # Mostra resultados detalhados
        if issues == 0:
            self.statusBar().showMessage("Sistema OK")
            ResultDialogs.show_success_dialog(self)
        else:
            self.statusBar().showMessage(f"Checkup concluído - {issues} problema(s)")
            ResultDialogs.show_issues_dialog(self, checks, fixes)
    
    def show_solutions(self):
        """Mostra menu de soluções disponíveis"""
        try:
            self.logger.info("Abrindo menu de soluções...")
            
            # Obtém soluções disponíveis
            solutions = solutions_service.get_available_solutions()
            
            if not solutions:
                QMessageBox.information(
                    self,
                    "Executar Solução",
                    "Nenhuma solução de troubleshooting disponível no momento."
                )
                return
            
            # Abre dialog de seleção
            dialog = SolutionsDialog(solutions, self)
            result = dialog.exec_()
            
            if result == QDialog.Accepted:
                selected_id = dialog.get_selected_solution()
                
                if selected_id:
                    self.logger.info(f"Executando solução: {selected_id}")
                    self.statusBar().showMessage("Executando solução...")
                    
                    # Executa a solução
                    success = solutions_service.execute_solution(selected_id)
                    
                    if success:
                        self.statusBar().showMessage("Solução executada")
                    else:
                        self.statusBar().showMessage("Erro ao executar solução")
                        
        except Exception as e:
            self.logger.error(f"Erro ao abrir menu de soluções: {e}")
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao abrir menu de soluções:\n{str(e)}"
            )
    
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        self.logger.info("Encerrando aplicação...")
        event.accept()
