"""
Janela do wizard de configuração de proxy — layout moderno.
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
from modules.proxy_setup import config
from modules.proxy_setup.views.step_widgets import Step1Widget, Step2Widget, Step3Widget


class StepIndicator(QWidget):
    """Indicador visual de progresso (círculos + linhas)."""

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


class _StepController:
    """Controla o fluxo de etapas do wizard."""

    def __init__(self, total: int):
        self.current_step = 1
        self.total_steps = total

    def can_go_back(self) -> bool:
        return self.current_step > 1

    def can_proceed_to_next(self) -> bool:
        return self.current_step < self.total_steps

    def next_step(self) -> bool:
        if self.can_proceed_to_next():
            self.current_step += 1
            return True
        return False

    def previous_step(self) -> bool:
        if self.can_go_back():
            self.current_step -= 1
            return True
        return False

    def get_progress(self):
        return (self.current_step, self.total_steps)


class ProxyWizardWindow(QDialog):
    """Wizard de configuração de proxy — layout moderno."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logger_service.get_logger('ProxyWizardWindow')
        self._controller = _StepController(config.STEP_COUNT)
        self._apply_ok = False
        self._verify_ok = False
        self._build_ui()
        self.logger.info("Wizard de proxy iniciado")

    def _build_ui(self):
        self.setWindowTitle("Configuração de Proxy")
        self.setMinimumSize(680, 580)
        self.resize(760, 640)
        self.setStyleSheet(f"QDialog {{ background-color: {Colors.BACKGROUND}; }}")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
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
        title_lbl = QLabel("Configuração de Proxy")
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

        # Conteúdo empilhado
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {Colors.BACKGROUND};")

        self._step1 = Step1Widget()
        self._step2 = Step2Widget()
        self._step3 = Step3Widget()

        self.content_stack.addWidget(self._step1)
        self.content_stack.addWidget(self._step2)
        self.content_stack.addWidget(self._step3)

        self._step2.apply_completed.connect(self._on_apply_completed)
        self._step3.verify_completed.connect(self._on_verify_completed)

        root.addWidget(self.content_stack, stretch=1)

        # Rodapé
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

    def _current_widget(self):
        step, _ = self._controller.get_progress()
        widgets = [self._step1, self._step2, self._step3]
        return widgets[step - 1]

    def _update_ui(self):
        current, total = self._controller.get_progress()
        self._step_label.setText(f"Etapa {current} de {total}")
        self._step_indicator.set_current(current)
        self.content_stack.setCurrentIndex(current - 1)
        self._back_btn.setEnabled(self._controller.can_go_back())

        if current == total:
            self._next_btn.setText("Concluir")
            self._next_btn.setEnabled(self._current_widget().is_complete())
        else:
            self._next_btn.setText("Próximo →")
            self._next_btn.setEnabled(True)

    def _go_next(self):
        current, total = self._controller.get_progress()
        if current == total:
            self._finish()
            return
        if self._controller.next_step():
            self._update_ui()

    def _go_back(self):
        if self._controller.previous_step():
            self._update_ui()

    def _on_apply_completed(self, success: bool):
        self._apply_ok = success
        self._update_ui()

    def _on_verify_completed(self, success: bool):
        self._verify_ok = success
        self._update_ui()

    def _finish(self):
        from common.views.dialogs import ResultDialogs
        if self._verify_ok:
            ResultDialogs.show_info(
                self,
                "Proxy Configurado",
                f"O proxy foi configurado com sucesso!\n\nServidor: {config.PROXY_SERVER}",
                "✅",
            )
        else:
            ResultDialogs.show_info(
                self,
                "Verificação Incompleta",
                "O wizard foi concluído, mas a verificação não confirmou o proxy.\n"
                "Se o problema persistir, abra um chamado para o suporte técnico.",
                "🎫",
            )
        self.accept()

    def _confirm_cancel(self):
        reply = QMessageBox.question(
            self,
            "Cancelar Wizard",
            "Deseja cancelar a configuração de proxy?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.reject()
