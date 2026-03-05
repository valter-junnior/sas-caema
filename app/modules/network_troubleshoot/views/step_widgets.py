"""
Widgets de cada etapa do wizard de troubleshooting de rede.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QScrollArea, QFrame, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import Card, InfoBanner, HeadingLabel, BodyLabel, SuccessButton
from modules.network_troubleshoot import config


class BaseStepWidget(QWidget):
    """Classe base para todos os widgets de etapa."""

    def __init__(self, step_number: int, parent=None):
        super().__init__(parent)
        self._step_number = step_number
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Ãrea de scroll para conteÃºdo longo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        outer.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # TÃ­tulo da etapa
        title_text = config.STEP_TITLES.get(self._step_number, f"Etapa {self._step_number}")
        title_lbl = QLabel(title_text)
        title_lbl.setFont(Fonts.heading(14))
        title_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        # Ãrea de imagem
        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignCenter)
        self._image_label.setMinimumHeight(180)
        self._image_label.setMaximumHeight(220)
        self._image_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.BORDER};
                border: 1.5px dashed {Colors.BORDER_HOVER};
                border-radius: 8px;
                color: {Colors.TEXT_MUTED};
                font-size: 12pt;
            }}
        """)
        self._load_image()
        layout.addWidget(self._image_label)

        # InstruÃ§Ã£o da etapa
        instruction = config.STEP_INSTRUCTIONS.get(self._step_number, "")
        if instruction:
            inst_lbl = BodyLabel(instruction)
            layout.addWidget(inst_lbl)

        # ConteÃºdo especÃ­fico da etapa
        self._add_custom_content(layout)
        layout.addStretch()

    def _load_image(self):
        image_path = config.STEP_IMAGES.get(self._step_number)
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            scaled = pixmap.scaled(460, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self._image_label.setPixmap(scaled)
        else:
            self._image_label.setText(f"[Imagem â€” Etapa {self._step_number}]")

    def _add_custom_content(self, layout: QVBoxLayout):
        """Sobrescrever nas subclasses para adicionar conteÃºdo especÃ­fico."""
        pass

    def _make_checkbox(self, text: str) -> QCheckBox:
        cb = QCheckBox(text)
        cb.setFont(Fonts.body(10))
        return cb

    def _make_checklist_card(self, label: str, items: list) -> Card:
        card = Card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 14, 16, 14)
        cl.setSpacing(8)

        if label:
            lbl = QLabel(label)
            lbl.setFont(Fonts.heading(10))
            lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
            cl.addWidget(lbl)

        for item in items:
            cl.addWidget(self._make_checkbox(item))

        return card

    def is_complete(self) -> bool:
        return True


class Step1Widget(BaseStepWidget):
    """Etapa 1: VerificaÃ§Ã£o FÃ­sica do Cabo de Rede."""

    def __init__(self, parent=None):
        super().__init__(1, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(self._make_checklist_card(
            "Confirme os itens abaixo:",
            [
                "Cabo conectado ao computador",
                "Cabo conectado ao roteador/switch",
                "Cabo sem danos visÃ­veis",
            ],
        ))


class Step2Widget(BaseStepWidget):
    """Etapa 2: VerificaÃ§Ã£o do Roteador/Modem."""

    def __init__(self, parent=None):
        super().__init__(2, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(self._make_checklist_card(
            "Confirme os itens abaixo:",
            [
                "Roteador/modem estÃ¡ ligado na tomada",
                "Luzes indicadoras estÃ£o acesas",
                "Equipamento nÃ£o apresenta sinais de aquecimento excessivo",
            ],
        ))


class Step3Widget(BaseStepWidget):
    """Etapa 3: VerificaÃ§Ã£o dos LEDs de ConexÃ£o."""

    def __init__(self, parent=None):
        super().__init__(3, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(InfoBanner(
            "âœ“  LED aceso/piscando = ConexÃ£o detectada\n"
            "âœ—  LED apagado = Sem conexÃ£o fÃ­sica",
            'info',
        ))
        layout.addWidget(self._make_checklist_card(
            "",
            [
                "LED da porta do computador estÃ¡ aceso",
                "LED da porta do roteador estÃ¡ aceso",
            ],
        ))


class Step4Widget(BaseStepWidget):
    """Etapa 4: Reiniciar Equipamentos de Rede."""

    def __init__(self, parent=None):
        super().__init__(4, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(InfoBanner(
            "1. Desligue o modem/roteador da tomada\n"
            "2. Aguarde 30 segundos\n"
            "3. Ligue novamente o equipamento\n"
            "4. Aguarde aproximadamente 2 minutos para inicializaÃ§Ã£o completa",
            'info',
        ))
        layout.addWidget(InfoBanner(
            "â±ï¸  ApÃ³s realizar os passos acima, clique em 'PrÃ³ximo' para testar a conectividade.",
            'warning',
        ))


class Step5Widget(BaseStepWidget):
    """Etapa 5: Teste de Conectividade."""

    test_completed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(5, parent)
        self._test_result = None

    def _add_custom_content(self, layout: QVBoxLayout):
        self._test_btn = SuccessButton("â–¶  Testar ConexÃ£o")
        self._test_btn.setMinimumHeight(46)
        self._test_btn.clicked.connect(self._run_test)
        layout.addWidget(self._test_btn)

        self._result_label = QLabel()
        self._result_label.setAlignment(Qt.AlignCenter)
        self._result_label.setWordWrap(True)
        self._result_label.setMinimumHeight(60)
        self._result_label.setFont(Fonts.body(10))
        self._result_label.setStyleSheet("background: transparent;")
        layout.addWidget(self._result_label)

    def _run_test(self):
        from modules.network_troubleshoot.services.network_checker import NetworkChecker
        from PyQt5.QtWidgets import QApplication

        self._test_btn.setEnabled(False)
        self._result_label.setText("Testando conectividade...")
        self._result_label.setStyleSheet(f"color: {Colors.PRIMARY}; background: transparent;")
        QApplication.processEvents()

        checker = NetworkChecker()
        connected = checker.check_internet_connectivity()
        self._test_result = connected

        if connected:
            self._result_label.setText("âœ“  ConexÃ£o restabelecida! O problema foi resolvido.")
            self._result_label.setStyleSheet(f"""
                color: {Colors.SUCCESS};
                background-color: {Colors.SUCCESS_SURFACE};
                border: 1.5px solid {Colors.SUCCESS_BORDER};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            """)
        else:
            self._result_label.setText(
                "âœ—  A conexÃ£o ainda nÃ£o foi restabelecida.\n"
                "Ã‰ necessÃ¡rio abrir um chamado para o suporte."
            )
            self._result_label.setStyleSheet(f"""
                color: {Colors.DANGER};
                background-color: {Colors.DANGER_SURFACE};
                border: 1.5px solid {Colors.DANGER_BORDER};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            """)

        self._test_btn.setEnabled(True)
        self.test_completed.emit(connected)

    def is_complete(self) -> bool:
        return self._test_result is not None

    def get_test_result(self) -> bool:
        return bool(self._test_result)
