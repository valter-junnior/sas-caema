"""
Widgets de cada etapa do wizard de configuração de proxy.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QApplication,
)
from PyQt5.QtCore import Qt, pyqtSignal

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import Card, InfoBanner, BodyLabel, SuccessButton
from modules.proxy_setup import config


class BaseStepWidget(QWidget):
    """Classe base para os widgets de etapa do wizard de proxy."""

    def __init__(self, step_number: int, parent=None):
        super().__init__(parent)
        self._step_number = step_number
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

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

        title_text = config.STEP_TITLES.get(self._step_number, f"Etapa {self._step_number}")
        title_lbl = QLabel(title_text)
        title_lbl.setFont(Fonts.heading(14))
        title_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        instruction = config.STEP_INSTRUCTIONS.get(self._step_number, "")
        if instruction:
            inst_lbl = BodyLabel(instruction)
            layout.addWidget(inst_lbl)

        self._add_custom_content(layout)
        layout.addStretch()

    def _add_custom_content(self, layout: QVBoxLayout):
        """Sobrescrever nas subclasses para adicionar conteúdo específico."""
        pass

    def _make_info_row(self, label: str, value: str) -> QWidget:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        hl = QHBoxLayout(row)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(8)

        lbl = QLabel(label)
        lbl.setFont(Fonts.body(10))
        lbl.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
        lbl.setFixedWidth(80)
        hl.addWidget(lbl)

        val = QLabel(value)
        val.setFont(Fonts.heading(10))
        val.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        hl.addWidget(val, stretch=1)

        return row

    def is_complete(self) -> bool:
        return True


class Step1Widget(BaseStepWidget):
    """Etapa 1: Informações sobre o proxy que será configurado."""

    def __init__(self, parent=None):
        super().__init__(1, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(InfoBanner(
            "Este assistente irá configurar automaticamente o proxy de rede neste computador.\n"
            "Nenhuma ação manual é necessária — basta seguir os passos.",
            'info',
        ))

        # Card com detalhes do proxy
        card = Card()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 16, 20, 16)
        cl.setSpacing(10)

        header = QLabel("Configurações que serão aplicadas")
        header.setFont(Fonts.heading(10))
        header.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        cl.addWidget(header)

        cl.addWidget(self._make_info_row("Servidor:", config.PROXY_HOST))
        cl.addWidget(self._make_info_row("Porta:", str(config.PROXY_PORT)))
        cl.addWidget(self._make_info_row("Endereço:", config.PROXY_SERVER))

        layout.addWidget(card)

        layout.addWidget(InfoBanner(
            "⚠️  Após configurar o proxy, o tráfego de rede será roteado pelo servidor acima.\n"
            "Clique em 'Próximo' para aplicar as configurações.",
            'warning',
        ))


class Step2Widget(BaseStepWidget):
    """Etapa 2: Aplicar as configurações de proxy."""

    apply_completed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(2, parent)
        self._apply_result = None

    def _add_custom_content(self, layout: QVBoxLayout):
        self._apply_btn = SuccessButton("▶  Aplicar Proxy Agora")
        self._apply_btn.setMinimumHeight(46)
        self._apply_btn.clicked.connect(self._run_apply)
        layout.addWidget(self._apply_btn)

        self._result_label = QLabel()
        self._result_label.setAlignment(Qt.AlignCenter)
        self._result_label.setWordWrap(True)
        self._result_label.setMinimumHeight(60)
        self._result_label.setFont(Fonts.body(10))
        self._result_label.setStyleSheet("background: transparent;")
        layout.addWidget(self._result_label)

        layout.addWidget(InfoBanner(
            "📋  O proxy será configurado nas Configurações de Internet do Windows\n"
            "e nas configurações de sistema (netsh winhttp).",
            'info',
        ))

    def _run_apply(self):
        from modules.proxy_setup.services.proxy_service import ProxyService

        self._apply_btn.setEnabled(False)
        self._result_label.setText("Aplicando configurações de proxy...")
        self._result_label.setStyleSheet(f"color: {Colors.PRIMARY}; background: transparent;")
        QApplication.processEvents()

        service = ProxyService()
        success = service.apply_proxy()
        self._apply_result = success

        if success:
            self._result_label.setText(
                f"✓  Proxy configurado com sucesso!\n{config.PROXY_SERVER}"
            )
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
                "✗  Falha ao aplicar as configurações de proxy.\n"
                "Verifique se o aplicativo possui permissões suficientes."
            )
            self._result_label.setStyleSheet(f"""
                color: {Colors.DANGER};
                background-color: {Colors.DANGER_SURFACE};
                border: 1.5px solid {Colors.DANGER_BORDER};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            """)

        self._apply_btn.setEnabled(True)
        self.apply_completed.emit(success)

    def is_complete(self) -> bool:
        return self._apply_result is not None

    def get_apply_result(self) -> bool:
        return bool(self._apply_result)


class Step3Widget(BaseStepWidget):
    """Etapa 3: Verificar se o proxy foi aplicado corretamente."""

    verify_completed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(3, parent)
        self._verify_result = None

    def _add_custom_content(self, layout: QVBoxLayout):
        self._verify_btn = SuccessButton("🔍  Verificar Configuração")
        self._verify_btn.setMinimumHeight(46)
        self._verify_btn.clicked.connect(self._run_verify)
        layout.addWidget(self._verify_btn)

        self._result_label = QLabel()
        self._result_label.setAlignment(Qt.AlignCenter)
        self._result_label.setWordWrap(True)
        self._result_label.setMinimumHeight(60)
        self._result_label.setFont(Fonts.body(10))
        self._result_label.setStyleSheet("background: transparent;")
        layout.addWidget(self._result_label)

        self._detail_label = QLabel()
        self._detail_label.setAlignment(Qt.AlignCenter)
        self._detail_label.setWordWrap(True)
        self._detail_label.setFont(Fonts.caption(9))
        self._detail_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent;")
        layout.addWidget(self._detail_label)

    def _run_verify(self):
        from modules.proxy_setup.services.proxy_service import ProxyService

        self._verify_btn.setEnabled(False)
        self._result_label.setText("Verificando...")
        self._result_label.setStyleSheet(f"color: {Colors.PRIMARY}; background: transparent;")
        self._detail_label.setText("")
        QApplication.processEvents()

        service = ProxyService()
        is_correct = service.is_correct_proxy_set()
        current = service.get_current_proxy()
        self._verify_result = is_correct

        if is_correct:
            self._result_label.setText("✓  Proxy configurado corretamente!")
            self._result_label.setStyleSheet(f"""
                color: {Colors.SUCCESS};
                background-color: {Colors.SUCCESS_SURFACE};
                border: 1.5px solid {Colors.SUCCESS_BORDER};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            """)
            self._detail_label.setText(f"Proxy ativo: {current}")
        else:
            self._result_label.setText(
                "✗  Proxy não está configurado corretamente.\n"
                "Volte ao passo anterior e tente aplicar novamente."
            )
            self._result_label.setStyleSheet(f"""
                color: {Colors.DANGER};
                background-color: {Colors.DANGER_SURFACE};
                border: 1.5px solid {Colors.DANGER_BORDER};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
            """)
            self._detail_label.setText(
                f"Proxy atual: {current or 'nenhum'} | Esperado: {config.PROXY_SERVER}"
            )

        self._verify_btn.setEnabled(True)
        self.verify_completed.emit(is_correct)

    def is_complete(self) -> bool:
        return self._verify_result is not None

    def get_verify_result(self) -> bool:
        return bool(self._verify_result)
