"""
Aplicação principal do SAS-Caema
Interface gráfica com PyQt5
"""
import sys
import argparse
import winreg
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel,
                             QMessageBox, QProgressDialog, QMenuBar, QMenu, QAction)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config import APP_NAME, APP_VERSION, PRIMARY_COLOR, SUCCESS_COLOR, ERROR_COLOR, STARTUP_REGISTRY_KEY, STARTUP_REGISTRY_VALUE
from common.services.logger import logger_service
from modules.checkup.services.checkup_service import CheckupService


class StartupManager:
    """Gerencia a inicialização automática no Windows"""
    
    @staticmethod
    def is_enabled() -> bool:
        """Verifica se está configurado para iniciar com Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, STARTUP_REGISTRY_VALUE)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def enable() -> bool:
        """Ativa inicialização com Windows"""
        try:
            # Caminho do executável atual
            if getattr(sys, 'frozen', False):
                # Rodando como .exe
                exe_path = sys.executable
            else:
                # Rodando como script - usa pythonw para não abrir console
                exe_path = f'"{sys.executable}" "{Path(__file__).absolute()}"'
            
            # Adiciona argumento --startup para modo silencioso
            command = f'"{exe_path}" --startup'
            
            # Abre registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Define valor
            winreg.SetValueEx(
                key,
                STARTUP_REGISTRY_VALUE,
                0,
                winreg.REG_SZ,
                command
            )
            
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            logger_service.error(f"Erro ao ativar startup: {e}")
            return False
    
    @staticmethod
    def disable() -> bool:
        """Desativa inicialização com Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.DeleteValue(key, STARTUP_REGISTRY_VALUE)
            winreg.CloseKey(key)
            return True
            
        except FileNotFoundError:
            return True  # Já não estava configurado
        except Exception as e:
            logger_service.error(f"Erro ao desativar startup: {e}")
            return False


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
        
        # Opção de startup
        self.startup_action = QAction('Iniciar com Windows', self)
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(StartupManager.is_enabled())
        self.startup_action.triggered.connect(self.toggle_startup)
        config_menu.addAction(self.startup_action)
        
        config_menu.addSeparator()
        
        # Opção Sobre
        about_action = QAction('Sobre', self)
        about_action.triggered.connect(self.show_about)
        config_menu.addAction(about_action)
    
    def toggle_startup(self):
        """Ativa/desativa inicialização com Windows"""
        if self.startup_action.isChecked():
            if StartupManager.enable():
                self.logger.info("Inicialização automática ativada")
                QMessageBox.information(
                    self,
                    "Configuração Salva",
                    "✓ SAS-Caema irá iniciar automaticamente com o Windows.\n\n"
                    "O checkup será executado em segundo plano toda vez que você ligar o computador."
                )
            else:
                self.startup_action.setChecked(False)
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Não foi possível ativar a inicialização automática.\n"
                    "Verifique os logs para mais detalhes."
                )
        else:
            if StartupManager.disable():
                self.logger.info("Inicialização automática desativada")
                QMessageBox.information(
                    self,
                    "Configuração Salva",
                    "✓ SAS-Caema não iniciará mais automaticamente com o Windows."
                )
            else:
                self.startup_action.setChecked(True)
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Não foi possível desativar a inicialização automática.\n"
                    "Verifique os logs para mais detalhes."
                )
    
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
            self.show_error_dialog(result['error'])
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
            self.statusBar().showMessage("✓ Sistema OK")
            self.show_success_dialog()
        else:
            self.statusBar().showMessage(f"Checkup concluído - {issues} problema(s)")
            self.show_issues_dialog(checks, fixes)
    
    def get_module_name(self, module_id: str) -> str:
        """Obtém o nome legível do módulo a partir do ID"""
        # Mapeamento de IDs para nomes legíveis
        module_names = {
            'wallpaper': 'Papel de Parede',
            # Adicione mais módulos aqui conforme necessário
        }
        return module_names.get(module_id, module_id.title())
    
    def show_success_dialog(self):
        """Mostra dialog de sucesso estilizado"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Checkup Concluído")
        
        # Título e texto
        msg.setText("<h2 style='color: #107C10;'>✓ Sistema OK</h2>")
        msg.setInformativeText(
            "<p style='font-size: 11pt;'>Nenhum problema encontrado!</p>"
            "<p style='color: #666666;'>O sistema está funcionando corretamente.</p>"
        )
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        # Estilo do botão
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                min-width: 400px;
            }
            QPushButton {
                background-color: #107C10;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0E6A0E;
            }
        """)
        
        msg.exec_()
    
    def show_issues_dialog(self, checks: list, fixes: dict):
        """Mostra dialog de problemas com estilo melhorado"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Checkup Concluído")
        
        # Conta sucessos e falhas
        fixed_count = sum(1 for success in fixes.values() if success)
        failed_count = len(fixes) - fixed_count
        issues_count = sum(1 for c in checks if c['status'] != 'ok')
        
        # Título
        if failed_count == 0:
            title_color = "#107C10"
            title_icon = "✓"
            title_text = "Problemas Corrigidos"
        else:
            title_color = "#FF8C00"
            title_icon = "⚠"
            title_text = "Atenção Necessária"
        
        msg.setText(f"<h2 style='color: {title_color};'>{title_icon} {title_text}</h2>")
        
        # Monta detalhes
        details = f"<div style='font-size: 10pt;'>"
        details += f"<p><b>Problemas encontrados:</b> {issues_count}</p>"
        
        # Lista problemas
        details += "<p style='margin-top: 10px;'><b>Detalhes:</b></p>"
        details += "<ul style='margin-left: 20px;'>"
        for check in checks:
            if check['status'] != 'ok':
                module_id = check.get('module', 'unknown')
                module_name = self.get_module_name(module_id)
                check_message = check.get('message', 'Sem descrição')
                details += f"<li>{check_message}</li>"
        details += "</ul>"
        
        # Resultados das correções
        if fixes:
            details += "<p style='margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd;'><b>Resultados:</b></p>"
            
            if fixed_count > 0:
                details += f"<p style='color: #107C10;'>✓ <b>{fixed_count}</b> problema(s) corrigido(s) automaticamente</p>"
            
            if failed_count > 0:
                details += f"<p style='color: #E81123;'>✗ <b>{failed_count}</b> problema(s) não puderam ser corrigidos</p>"
                
                # Lista quais falharam
                details += "<p style='margin-top: 5px; font-size: 9pt; color: #666;'>Problemas não corrigidos:</p>"
                details += "<ul style='margin-left: 20px; font-size: 9pt; color: #666;'>"
                for module_id, success in fixes.items():
                    if not success:
                        module_name = self.get_module_name(module_id)
                        details += f"<li>{module_name}</li>"
                details += "</ul>"
                
                details += "<p style='margin-top: 10px; font-size: 9pt; color: #666; font-style: italic;'>"
                details += "Verifique os logs para mais detalhes sobre os erros."
                details += "</p>"
        
        details += "</div>"
        
        msg.setInformativeText(details)
        msg.setTextFormat(Qt.RichText)
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        # Estilo
        button_color = "#107C10" if failed_count == 0 else "#0078D4"
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
            }}
            QLabel {{
                min-width: 400px;
            }}
            QPushButton {{
                background-color: {button_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
        """)
        
        msg.exec_()
    
    def show_error_dialog(self, error_message: str):
        """Mostra dialog de erro estilizado"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Erro no Checkup")
        
        msg.setText("<h2 style='color: #E81123;'>✗ Erro</h2>")
        msg.setInformativeText(
            f"<p style='font-size: 10pt;'>Ocorreu um erro ao executar o checkup:</p>"
            f"<p style='font-family: Consolas; background-color: #f5f5f5; padding: 10px; "
            f"border-radius: 4px; color: #d32f2f;'>{error_message}</p>"
            f"<p style='font-size: 9pt; color: #666; margin-top: 10px;'>"
            f"Verifique os logs para mais informações."
            f"</p>"
        )
        msg.setTextFormat(Qt.RichText)
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                min-width: 400px;
            }
            QPushButton {
                background-color: #E81123;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #C50F1F;
            }
        """)
        
        msg.exec_()
    
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
        self.logger.info("Encerrando aplicação...")
        event.accept()


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
