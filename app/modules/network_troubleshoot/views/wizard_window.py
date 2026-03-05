"""
Janela do wizard de verificação de rede — redesign moderno.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QStackedWidget, QWidget, QFrame, QMessageBox,
)
from PyQt5.QtCore import Qt

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import PrimaryButton, SecondaryButton, GhostDangerButton
from common.services.logger import logger_service
from modules.network_troubleshoot import config
from modules.network_troubleshoot.services.step_validator import StepValidator
from modules.network_troubleshoot.views.step_widgets import (
    Step1Widget, Step2Widget, Step3Widget, Step4Widget, Step5Widget,
)


class StepIndicator(QWidget):
    """Indicador visual de progresso entre as etapas (círculos + linhas)."""

    def __init__(self, total: int, parent=None):
        super().__init__(parent)
        self._total = total
        self._current = 1
        self.setFixedHeight(52)
        self.setStyleSheet(f"background-color: {Colors.HEADER_BG};")
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(32, 0, 32, 0)
        self._layout.setSpacing(0)
        self._rebuild()

    def _rebuild(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i in range(1, self._total + 1):
            is_done = i < self._current
            is_active = i == self._current

            dot = QLabel("✓" if is_done else str(i))
            dot.setFixedSize(28, 28)
            dot.setAlignment(Qt.AlignCenter)
            dot.setFont(Fonts.caption(8))

            if is_done:
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {Colors.SUCCESS};
                        color: white;
                        border-radius: 14px;
                        font-weight: bold;
                    }}
                """)
            elif is_active:
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {Colors.PRIMARY};
                        color: white;
                        border-radius: 14px;
                        font-weight: bold;
                    }}
                """)
            else:
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {Colors.HEADER_SURFACE};
                        color: {Colors.TEXT_MUTED};
                        border-radius: 14px;
                    }}
                """)

            self._layout.addWidget(dot)

            if i < self._total:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFixedHeight(2)
                color = Colors.SUCCESS if is_done else Colors.HEADER_SURFACE
                line.setStyleSheet(f"background-color: {color}; border: none;")
                self._layout.addWidget(line, stretch=1)

    def set_current(self, step: int):
        self._current = step
        self._rebuild()


class WizardWindow(QDialog):
    """Wizard de troubleshooting de rede — layout moderno."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logger_service.get_logger('WizardWindow')
        self.validator = StepValidator()
        self.test_result = False
        self._build_ui()
        self.logger.info("Wizard de troubleshooting iniciado")

    def _build_ui(self):
        self.setWindowTitle("Verificação de Cabos de Rede")
        self.setMinimumSize(680, 620)
        self.resize(780, 680)
        self.setStyleSheet(f"QDialog {{ background-color: {Colors.BACKGROUND}; }}")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header escuro ─────────────────────────────────────────
        header = QWidget()
        header.setObjectName("wizardHeader")
        header.setStyleSheet(f"""
            QWidget#wizardHeader {{
                background-color: {Colors.HEADER_BG};
                border-bottom: 1px solid {Colors.HEADER_SURFACE};
            }}
        """)
        hl = QVBoxLayout(header)
        hl.setContentsMargins(32, 16, 32, 0)
        hl.setSpacing(6)

        title_row = QHBoxLayout()
        title_lbl = QLabel("Verificação de Cabos de Rede")
        title_lbl.setFont(Fonts.heading(14))
        title_lbl.setStyleSheet(f"color: {Colors.HEADER_TEXT}; background: transparent;")
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        self._step_label = QLabel()
        self._step_label.setFont(Fonts.caption(9))
        self._step_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent;")
        title_row.addWidget(self._step_label)
        hl.addLayout(title_row)

        self._step_indicator = StepIndicator(config.STEP_COUNT)
        hl.addWidget(self._step_indicator)

        root.addWidget(header)

        # ── Conteúdo empilhado (uma etapa por vez) ────────────────
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {Colors.BACKGROUND};")

        self.step_widgets = [
            Step1Widget(), Step2Widget(), Step3Widget(),
            Step4Widget(), Step5Widget(),
        ]
        for w in self.step_widgets:
            self.content_stack.addWidget(w)

        self.step_widgets[4].test_completed.connect(self._on_test_completed)
        root.addWidget(self.content_stack, stretch=1)

        # ── Rodapé com botões ─────────────────────────────────────
        footer = QWidget()
        footer.setObjectName("wizardFooter")
        footer.setFixedHeight(68)
        footer.setStyleSheet(f"""
            QWidget#wizardFooter {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
            }}
        """)
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 14, 24, 14)
        fl.setSpacing(10)

        self._back_btn = SecondaryButton("← Voltar")
        self._back_btn.setMinimumWidth(110)
        self._back_btn.clicked.connect(self._go_back)
        fl.addWidget(self._back_btn)

        fl.addStretch()

        self._cancel_btn = GhostDangerButton("Cancelar")
        self._cancel_btn.setMinimumWidth(110)
        self._cancel_btn.clicked.connect(self._confirm_cancel)
        fl.addWidget(self._cancel_btn)

        self._next_btn = PrimaryButton("Próximo →")
        self._next_btn.setMinimumWidth(130)
        self._next_btn.clicked.connect(self._go_next)
        fl.addWidget(self._next_btn)

        root.addWidget(footer)

        self._update_ui()

    def _update_ui(self):
        current, total = self.validator.get_progress()
        self._step_label.setText(f"Etapa {current} de {total}")
        self._step_indicator.set_current(current)
        self.content_stack.setCurrentIndex(current - 1)
        self._back_btn.setEnabled(self.validator.can_go_back())

        if current == total:
            self._next_btn.setText("Concluir")
            self._next_btn.setEnabled(self.step_widgets[current - 1].is_complete())
        else:
            self._next_btn.setText("Próximo →")
            self._next_btn.setEnabled(True)

        self.logger.debug(f"UI atualizada para etapa {current}/{total}")

    def _go_next(self):
        current, total = self.validator.get_progress()
        if current == total:
            self._finish()
            return
        self.validator.mark_step_complete(current)
        if self.validator.next_step():
            self._update_ui()
            self.logger.info(f"Avançou para etapa {self.validator.current_step}")

    def _go_back(self):
        if self.validator.prev_step():
            self._update_ui()

    def _on_test_completed(self, success: bool):
        self.test_result = success
        self._update_ui()

    def _finish(self):
        from common.views.dialogs import ResultDialogs
        if self.test_result:
            ResultDialogs.show_info(
                self,
                "Conexão Restabelecida",
                "A conexão de internet foi restabelecida com sucesso!\nO problema foi resolvido.",
                "✅",
            )
        else:
            ResultDialogs.show_info(
                self,
                "Suporte Necessário",
                "A conexão não foi restabelecida após o diagnóstico.\n"
                "Por favor, abra um chamado para o suporte técnico.",
                "🎫",
            )
        self.accept()

    def _confirm_cancel(self):
        reply = QMessageBox.question(
            self,
            "Cancelar Wizard",
            "Deseja cancelar o wizard de diagnóstico?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.reject()

    # Aliases públicos mantidos por compatibilidade
    def update_ui(self):
        self._update_ui()

    def go_next(self):
        self._go_next()

    def go_back(self):
        self._go_back()

    def on_test_completed(self, success: bool):
        self._on_test_completed(success)

    def finish_wizard(self):
        self._finish()

    def confirm_cancel(self):
        self._confirm_cancel()



    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logger_service.get_logger('WizardWindow')
        self.validator = StepValidator()
        self.test_result = False
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do wizard"""
        self.setWindowTitle("Verificação de Cabos de Rede")
        self.setMinimumSize(700, 600)
        self.resize(800, 700)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.setLayout(main_layout)
        
        # Área de progresso
        self.progress_label = QLabel()
        self.progress_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            background-color: #0078D4; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        main_layout.addWidget(self.progress_label)
        
        # Área de conteúdo (QStackedWidget para alternar entre etapas)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Criar e adicionar widgets de etapas
        self.step_widgets = [
            Step1Widget(),
            Step2Widget(),
            Step3Widget(),
            Step4Widget(),
            Step5Widget()
        ]
        
        for widget in self.step_widgets:
            self.content_stack.addWidget(widget)
        
        # Conectar sinais do Step5Widget (teste)
        self.step_widgets[4].test_completed.connect(self.on_test_completed)
        
        # Área de botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Botão Voltar
        self.back_button = QPushButton("← Voltar")
        self.back_button.setFont(QFont("Segoe UI", 10))
        self.back_button.setMinimumHeight(40)
        self.back_button.setMinimumWidth(120)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:disabled {
                background-color: #F8F8F8;
                color: #AAAAAA;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)
        
        # Espaçamento
        button_layout.addStretch()
        
        # Botão Cancelar
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setFont(QFont("Segoe UI", 10))
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #E81123;
                border: 1px solid #E81123;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #FDE7E9;
            }
        """)
        self.cancel_button.clicked.connect(self.confirm_cancel)
        button_layout.addWidget(self.cancel_button)
        
        # Botão Próximo
        self.next_button = QPushButton("Próximo →")
        self.next_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.next_button.setMinimumHeight(40)
        self.next_button.setMinimumWidth(120)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        self.next_button.clicked.connect(self.go_next)
        button_layout.addWidget(self.next_button)
        
        main_layout.addLayout(button_layout)
        
        # Atualiza a interface inicial
        self.update_ui()
        
        self.logger.info("Wizard de troubleshooting iniciado")
    
    def update_ui(self):
        """Atualiza a interface baseado na etapa atual"""
        current, total = self.validator.get_progress()
        
        # Atualiza label de progresso
        self.progress_label.setText(f"Etapa {current} de {total}")
        
        # Atualiza stack widget
        self.content_stack.setCurrentIndex(current - 1)
        
        # Atualiza botões
        self.back_button.setEnabled(self.validator.can_go_back())
        
        # Na última etapa
        if current == total:
            self.next_button.setText("Concluir")
            # Desabilita até teste ser executado
            current_widget = self.step_widgets[current - 1]
            self.next_button.setEnabled(current_widget.is_complete())
        else:
            self.next_button.setText("Próximo →")
            self.next_button.setEnabled(True)
        
        self.logger.debug(f"UI atualizada para etapa {current}/{total}")
    
    def go_next(self):
        """Avança para a próxima etapa"""
        current, total = self.validator.get_progress()
        
        # Se está na última etapa, conclui o wizard
        if current == total:
            self.finish_wizard()
            return
        
        # Marca etapa atual como concluída e avança
        self.validator.mark_step_complete(current)
        
        if self.validator.next_step():
            self.update_ui()
            self.logger.info(f"Avançou para etapa {self.validator.current_step}")
    
    def go_back(self):
        """Volta para a etapa anterior"""
        if self.validator.previous_step():
            self.update_ui()
            self.logger.info(f"Voltou para etapa {self.validator.current_step}")
    
    def on_test_completed(self, result: bool):
        """Callback quando o teste de conectividade termina"""
        self.test_result = result
        self.logger.info(f"Teste de conectividade concluído: {'Sucesso' if result else 'Falha'}")
        self.update_ui()  # Habilita botão concluir
    
    def finish_wizard(self):
        """Conclui o wizard e mostra resultado final"""
        step5_widget = self.step_widgets[4]
        test_result = step5_widget.get_test_result()
        
        self.logger.info(f"Wizard concluído - Resultado: {'Internet OK' if test_result else 'Sem conectividade'}")
        
        if test_result:
            # Internet OK - Mostra mensagem de sucesso
            QMessageBox.information(
                self,
                "Problema Resolvido",
                "<h3>✓ Conexão Restabelecida!</h3>"
                "<p>O problema de conectividade foi resolvido com sucesso.</p>"
                "<p>Sua internet está funcionando normalmente.</p>",
                QMessageBox.Ok
            )
            self.accept()  # Fecha o dialog com sucesso
        else:
            # Sem internet - Mostra orientação para abrir chamado
            reply = QMessageBox.warning(
                self,
                "Abrir Chamado ao Suporte",
                "<h3>Problema Não Resolvido</h3>"
                "<p>Infelizmente, não foi possível restabelecer a conexão com os procedimentos básicos.</p>"
                "<p><b>É necessário abrir um chamado para o suporte técnico.</b></p>"
                "<p>Entre em contato com o suporte informando que seguiu os passos de verificação de cabos.</p>",
                QMessageBox.Ok
            )
            self.accept()  # Fecha o dialog
    
    def confirm_cancel(self):
        """Confirma o cancelamento do wizard"""
        reply = QMessageBox.question(
            self,
            "Cancelar Verificação",
            "Deseja realmente cancelar a verificação de cabos?\n\n"
            "Seu progresso será perdido.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.logger.info("Wizard cancelado pelo usuário")
            self.reject()  # Fecha o dialog como cancelado
    
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        # Se tentar fechar com X, confirma cancelamento
        self.confirm_cancel()
        event.ignore()  # Ignora o evento, deixa confirm_cancel controlar
