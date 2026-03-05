"""
Janela principal da aplicação — arquitetura MVVM-inspirada.
A View é responsável apenas pela UI; a lógica de negócios fica nos serviços.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QAction, QSizePolicy, QDialog,
)
from PyQt5.QtCore import Qt

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import APP_NAME, APP_VERSION
from common.theme import Colors, Fonts
from common.widgets import (
    Card, HeaderBar, PrimaryButton, SuccessButton,
    BodyLabel, HeadingLabel,
)
from common.services.logger import logger_service
from common.services.solutions_service import solutions_service
from modules.checkup.threads.checkup_thread import CheckupThread
from common.views.dialogs import ResultDialogs
from common.views.solutions_dialog import SolutionsDialog


class ActionCard(Card):
    """Card de ação única com ícone, título, descrição e botão."""

    def __init__(
        self,
        icon: str,
        title: str,
        description: str,
        button_text: str,
        button_style: str = 'primary',
        parent=None,
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(Fonts.title(26))
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setFont(Fonts.heading(14))
        title_lbl.setStyleSheet(
            f"color: {Colors.TEXT_PRIMARY}; background: transparent; border: none;"
        )
        layout.addWidget(title_lbl)

        desc_lbl = BodyLabel(description)
        desc_lbl.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; background: transparent; border: none;"
        )
        layout.addWidget(desc_lbl)

        layout.addStretch()

        self.button = (
            SuccessButton(button_text)
            if button_style == 'success'
            else PrimaryButton(button_text)
        )
        self.button.setMinimumHeight(42)
        layout.addWidget(self.button)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class MainWindow(QMainWindow):
    """Janela principal da aplicação."""

    def __init__(self):
        super().__init__()
        self.logger = logger_service.get_logger('MainWindow')
        self.checkup_thread = None
        self._build_ui()
        self._build_menu()

    # ------------------------------------------------------------------
    # Construção da UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 880, 580)
        self.setMinimumSize(720, 500)

        root = QWidget()
        root.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header (card flutuante com margem)
        header_wrapper = QWidget()
        header_wrapper.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        hw_layout = QVBoxLayout(header_wrapper)
        hw_layout.setContentsMargins(20, 14, 20, 0)
        hw_layout.setSpacing(0)
        hw_layout.addWidget(HeaderBar(APP_NAME, "Sistema de Automação de Suporte"))
        root_layout.addWidget(header_wrapper)

        # Área de conteúdo
        content_wrapper = QWidget()
        content_wrapper.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(32, 28, 32, 28)
        content_layout.setSpacing(20)

        welcome = QLabel("O que você quer fazer hoje?")
        welcome.setFont(Fonts.heading(16))
        welcome.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        content_layout.addWidget(welcome)

        # Cards de ação
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self._checkup_card = ActionCard(
            icon="🔍",
            title="Rodar Checkup",
            description=(
                "Verifica o estado atual do sistema e corrige "
                "problemas automaticamente, como papel de parede incorreto."
            ),
            button_text="Iniciar Checkup",
            button_style='primary',
        )
        self._checkup_card.button.clicked.connect(self._run_checkup)
        cards_layout.addWidget(self._checkup_card)

        self._solutions_card = ActionCard(
            icon="🔧",
            title="Executar Solução",
            description=(
                "Selecione um wizard de diagnóstico guiado para "
                "resolver problemas de rede, impressora e outros."
            ),
            button_text="Ver Soluções",
            button_style='success',
        )
        self._solutions_card.button.clicked.connect(self._show_solutions)
        cards_layout.addWidget(self._solutions_card)

        content_layout.addLayout(cards_layout)
        content_layout.addStretch()
        root_layout.addWidget(content_wrapper, stretch=1)

        # Rodapé de status
        root_layout.addWidget(self._build_footer())

        self.logger.info(f"Aplicação iniciada — versão {APP_VERSION}")

    def _build_footer(self) -> QWidget:
        footer = QWidget()
        footer.setObjectName("mainFooter")
        footer.setFixedHeight(40)
        footer.setStyleSheet(f"""
            QWidget#mainFooter {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
            }}
        """)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(6)

        self._status_dot = QLabel("●")
        self._status_dot.setStyleSheet(
            f"color: {Colors.SUCCESS}; background: transparent; border: none;"
        )
        layout.addWidget(self._status_dot)

        self._status_label = QLabel("Pronto")
        self._status_label.setFont(Fonts.caption(9))
        self._status_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; background: transparent; border: none;"
        )
        layout.addWidget(self._status_label)

        layout.addStretch()

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setFont(Fonts.caption(9))
        version_label.setStyleSheet(
            f"color: {Colors.TEXT_MUTED}; background: transparent; border: none;"
        )
        layout.addWidget(version_label)
        return footer

    def _build_menu(self):
        menubar = self.menuBar()
        config_menu = menubar.addMenu('Configurações')
        about_action = QAction('Sobre', self)
        about_action.triggered.connect(self._show_about)
        config_menu.addAction(about_action)

    # ------------------------------------------------------------------
    # Controle de status
    # ------------------------------------------------------------------

    def _set_status(self, text: str, state: str = 'idle'):
        """Atualiza o indicador de status no rodapé. state: idle|running|ok|error"""
        dot_colors = {
            'idle':    Colors.TEXT_MUTED,
            'running': Colors.WARNING,
            'ok':      Colors.SUCCESS,
            'error':   Colors.DANGER,
        }
        color = dot_colors.get(state, Colors.TEXT_MUTED)
        self._status_dot.setStyleSheet(
            f"color: {color}; background: transparent; border: none;"
        )
        self._status_label.setText(text)

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _show_about(self):
        from common.views.dialogs import AboutDialog
        AboutDialog(APP_NAME, APP_VERSION, self).exec_()

    def _run_checkup(self):
        self.logger.info("Iniciando checkup do sistema...")
        self._checkup_card.button.setEnabled(False)
        self._solutions_card.button.setEnabled(False)
        self._set_status("Executando checkup...", 'running')

        self.checkup_thread = CheckupThread(auto_fix=True)
        self.checkup_thread.finished.connect(self._on_checkup_finished)
        self.checkup_thread.start()

    def _on_checkup_finished(self, result: dict):
        self._checkup_card.button.setEnabled(True)
        self._solutions_card.button.setEnabled(True)

        if 'error' in result:
            self.logger.error(f"Erro durante checkup: {result['error']}")
            self._set_status("Erro no checkup", 'error')
            ResultDialogs.show_error(self, result['error'])
            return

        issues = result.get('issues_found', 0)
        fixes = result.get('fixes_applied', {})
        checks = result.get('checks', [])

        self.logger.info(f"Checkup concluído — {issues} problema(s)")

        if issues == 0:
            self._set_status("Sistema OK", 'ok')
            ResultDialogs.show_success(self)
        else:
            self._set_status(f"Checkup concluído — {issues} problema(s)", 'error')
            ResultDialogs.show_issues(self, checks, fixes)

    def _show_solutions(self):
        try:
            self.logger.info("Abrindo menu de soluções...")
            solutions = solutions_service.get_available_solutions()

            if not solutions:
                ResultDialogs.show_info(
                    self,
                    "Nenhuma solução disponível",
                    "Nenhuma solução de troubleshooting está disponível no momento.",
                )
                return

            dialog = SolutionsDialog(solutions, self)
            if dialog.exec_() == QDialog.Accepted:
                selected_id = dialog.get_selected_solution()
                if not selected_id:
                    return

                self.logger.info(f"Executando solução: {selected_id}")
                self._set_status("Executando solução...", 'running')
                from PyQt5.QtWidgets import QApplication
                QApplication.processEvents()

                success = solutions_service.execute_solution(selected_id)

                if success:
                    self._set_status("Solução executada com sucesso", 'ok')
                    if selected_id == 'wallpaper_fix':
                        ResultDialogs.show_info(
                            self,
                            "Papel de Parede Atualizado",
                            "O papel de parede foi gerado e configurado com sucesso!\n"
                            "As informações do sistema estão visíveis na tela.",
                            "🖼️",
                        )
                else:
                    self._set_status("Erro ao executar solução", 'error')
                    if selected_id == 'wallpaper_fix':
                        ResultDialogs.show_error(
                            self,
                            "Não foi possível gerar ou configurar o papel de parede.\n"
                            "Verifique os logs para mais detalhes.",
                        )
                    elif selected_id != 'network_troubleshoot':
                        ResultDialogs.show_error(
                            self,
                            "Não foi possível executar a solução.\n"
                            "Verifique os logs para mais detalhes.",
                        )
            else:
                self._set_status("Pronto")

        except Exception as e:
            self.logger.error(f"Erro ao abrir menu de soluções: {e}")
            ResultDialogs.show_error(self, str(e))

    def closeEvent(self, event):
        self.logger.info("Encerrando aplicação...")
        event.accept()


    
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
                    
                    # Força processamento de eventos para atualizar UI
                    from PyQt5.QtWidgets import QApplication
                    QApplication.processEvents()
                    
                    # Executa a solução
                    success = solutions_service.execute_solution(selected_id)
                    
                    if success:
                        self.statusBar().showMessage("Solução executada com sucesso")
                        
                        # Feedback específico por tipo de solução
                        if selected_id == 'wallpaper_fix':
                            QMessageBox.information(
                                self,
                                "Papel de Parede Atualizado",
                                "O papel de parede foi gerado e configurado com sucesso!\n\n"
                                "As informações do sistema estão agora visíveis na tela."
                            )
                        elif selected_id == 'network_troubleshoot':
                            # Wizard já mostra seu próprio feedback
                            pass
                    else:
                        self.statusBar().showMessage("Erro ao executar solução")
                        
                        # Erro específico por tipo de solução
                        if selected_id == 'wallpaper_fix':
                            QMessageBox.warning(
                                self,
                                "Erro ao Atualizar Papel de Parede",
                                "Não foi possível gerar ou configurar o papel de parede.\n\n"
                                "Verifique os logs para mais detalhes."
                            )
                        else:
                            QMessageBox.warning(
                                self,
                                "Erro",
                                "Não foi possível executar a solução.\n\n"
                                "Verifique os logs para mais detalhes."
                            )
                        
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
