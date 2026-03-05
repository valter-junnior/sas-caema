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
                item.widget().setParent(None)

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
        if self.validator.previous_step():
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



    
