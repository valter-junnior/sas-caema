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
from PyQt5.QtGui import QPixmap

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

        # Área de scroll para conteúdo longo
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

        # Título da etapa
        title_text = config.STEP_TITLES.get(self._step_number, f"Etapa {self._step_number}")
        title_lbl = QLabel(title_text)
        title_lbl.setFont(Fonts.heading(14))
        title_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        # Área de imagem
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

        # Instrução da etapa
        instruction = config.STEP_INSTRUCTIONS.get(self._step_number, "")
        if instruction:
            inst_lbl = BodyLabel(instruction)
            layout.addWidget(inst_lbl)

        # Conteúdo específico da etapa
        self._add_custom_content(layout)
        layout.addStretch()

    def _load_image(self):
        image_path = config.STEP_IMAGES.get(self._step_number)
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            scaled = pixmap.scaled(460, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self._image_label.setPixmap(scaled)
        else:
            self._image_label.setText(f"[Imagem — Etapa {self._step_number}]")

    def _add_custom_content(self, layout: QVBoxLayout):
        """Sobrescrever nas subclasses para adicionar conteúdo específico."""
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
    """Etapa 1: Verificação Física do Cabo de Rede."""

    def __init__(self, parent=None):
        super().__init__(1, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(self._make_checklist_card(
            "Confirme os itens abaixo:",
            [
                "Cabo conectado ao computador",
                "Cabo conectado ao roteador/switch",
                "Cabo sem danos visíveis",
            ],
        ))


class Step2Widget(BaseStepWidget):
    """Etapa 2: Verificação do Roteador/Modem."""

    def __init__(self, parent=None):
        super().__init__(2, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(self._make_checklist_card(
            "Confirme os itens abaixo:",
            [
                "Roteador/modem está ligado na tomada",
                "Luzes indicadoras estão acesas",
                "Equipamento não apresenta sinais de aquecimento excessivo",
            ],
        ))


class Step3Widget(BaseStepWidget):
    """Etapa 3: Verificação dos LEDs de Conexão."""

    def __init__(self, parent=None):
        super().__init__(3, parent)

    def _add_custom_content(self, layout: QVBoxLayout):
        layout.addWidget(InfoBanner(
            "✓  LED aceso/piscando = Conexão detectada\n"
            "✗  LED apagado = Sem conexão física",
            'info',
        ))
        layout.addWidget(self._make_checklist_card(
            "",
            [
                "LED da porta do computador está aceso",
                "LED da porta do roteador está aceso",
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
            "4. Aguarde aproximadamente 2 minutos para inicialização completa",
            'info',
        ))
        layout.addWidget(InfoBanner(
            "⏱️  Após realizar os passos acima, clique em 'Próximo' para testar a conectividade.",
            'warning',
        ))


class Step5Widget(BaseStepWidget):
    """Etapa 5: Teste de Conectividade."""

    test_completed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(5, parent)
        self._test_result = None

    def _add_custom_content(self, layout: QVBoxLayout):
        self._test_btn = SuccessButton("▶  Testar Conexão")
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
            self._result_label.setText("✓  Conexão restabelecida! O problema foi resolvido.")
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
                "✗  A conexão ainda não foi restabelecida.\n"
                "É necessário abrir um chamado para o suporte."
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

    
    def __init__(self, step_number: int, parent=None):
        super().__init__(parent)
        self.step_number = step_number
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Título da etapa
        title = config.STEP_TITLES.get(self.step_number, f"Etapa {self.step_number}")
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0078D4; padding: 10px;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Área para imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(250)
        self.image_label.setStyleSheet("background-color: #F0F0F0; border: 1px solid #CCCCCC; border-radius: 5px;")
        self.load_image()
        layout.addWidget(self.image_label)
        
        # Instruções
        instruction = config.STEP_INSTRUCTIONS.get(self.step_number, "")
        instruction_label = QLabel(instruction)
        instruction_label.setFont(QFont("Segoe UI", 11))
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("color: #333333; padding: 10px;")
        layout.addWidget(instruction_label)
        
        # Área customizável para cada etapa
        self.custom_content = QWidget()
        self.custom_layout = QVBoxLayout()
        self.custom_content.setLayout(self.custom_layout)
        layout.addWidget(self.custom_content)
        
        # Espaçamento flexível
        layout.addStretch()
    
    def load_image(self):
        """Carrega a imagem da etapa"""
        image_path = config.STEP_IMAGES.get(self.step_number)
        
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            # Redimensiona mantendo proporção
            scaled_pixmap = pixmap.scaled(400, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            # Placeholder text se imagem não existir
            self.image_label.setText(f"[Imagem da Etapa {self.step_number}]\nPLACEHOLDER")
            self.image_label.setStyleSheet("""
                background-color: #E0E0E0; 
                border: 2px dashed #999999; 
                border-radius: 5px;
                color: #666666;
                font-size: 14pt;
            """)
    
    def is_complete(self) -> bool:
        """
        Verifica se a etapa está completa
        Deve ser sobrescrito por subclasses se necessário
        """
        return True


class Step1Widget(BaseStepWidget):
    """Widget para Etapa 1: Verificação Física do Cabo de Rede"""
    
    def __init__(self, parent=None):
        super().__init__(1, parent)
        self.setup_checklist()
    
    def setup_checklist(self):
        """Configura o checklist da etapa 1"""
        checklist_items = [
            "Cabo conectado ao computador",
            "Cabo conectado ao roteador/switch",
            "Cabo sem danos visíveis"
        ]
        
        for item in checklist_items:
            checkbox = QCheckBox(item)
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.setStyleSheet("padding: 5px;")
            self.custom_layout.addWidget(checkbox)


class Step2Widget(BaseStepWidget):
    """Widget para Etapa 2: Verificação do Roteador/Modem"""
    
    def __init__(self, parent=None):
        super().__init__(2, parent)
        self.setup_checklist()
    
    def setup_checklist(self):
        """Configura o checklist da etapa 2"""
        checklist_items = [
            "Roteador/modem está ligado na tomada",
            "Luzes indicadoras estão acesas",
            "Equipamento não apresenta sinais de aquecimento excessivo"
        ]
        
        for item in checklist_items:
            checkbox = QCheckBox(item)
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.setStyleSheet("padding: 5px;")
            self.custom_layout.addWidget(checkbox)


class Step3Widget(BaseStepWidget):
    """Widget para Etapa 3: Verificação de LEDs"""
    
    def __init__(self, parent=None):
        super().__init__(3, parent)
        self.setup_content()
    
    def setup_content(self):
        """Configura o conteúdo da etapa 3"""
        # Informação sobre LEDs
        info_label = QLabel(
            "✓ LED aceso/piscando = Conexão detectada\n"
            "✗ LED apagado = Sem conexão física"
        )
        info_label.setFont(QFont("Segoe UI", 10))
        info_label.setStyleSheet("""
            background-color: #FFF4CE; 
            border: 1px solid #FFD700; 
            border-radius: 5px; 
            padding: 10px;
            color: #333333;
        """)
        self.custom_layout.addWidget(info_label)
        
        # Checklist
        checklist_items = [
            "LED da porta do computador está aceso",
            "LED da porta do roteador está aceso"
        ]
        
        for item in checklist_items:
            checkbox = QCheckBox(item)
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.setStyleSheet("padding: 5px; margin-top: 10px;")
            self.custom_layout.addWidget(checkbox)


class Step4Widget(BaseStepWidget):
    """Widget para Etapa 4: Reiniciar Equipamento"""
    
    def __init__(self, parent=None):
        super().__init__(4, parent)
        self.setup_content()
    
    def setup_content(self):
        """Configura o conteúdo da etapa 4"""
        # Lista de passos
        steps_text = (
            "1. Desligue o modem/roteador da tomada\n"
            "2. Aguarde 30 segundos\n"
            "3. Ligue novamente o equipamento\n"
            "4. Aguarde aproximadamente 2 minutos para inicialização completa"
        )
        
        steps_label = QLabel(steps_text)
        steps_label.setFont(QFont("Segoe UI", 10))
        steps_label.setStyleSheet("""
            background-color: #E8F4F8; 
            border: 1px solid #0078D4; 
            border-radius: 5px; 
            padding: 15px;
            color: #333333;
        """)
        self.custom_layout.addWidget(steps_label)
        
        # Label informativa
        info_label = QLabel(
            "⏱️ Após realizar os passos acima, clique em 'Próximo' para testar a conectividade."
        )
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            background-color: #FFF4CE; 
            border: 1px solid #FFD700; 
            border-radius: 5px; 
            padding: 10px;
            color: #333333;
            margin-top: 10px;
        """)
        self.custom_layout.addWidget(info_label)


class Step5Widget(BaseStepWidget):
    """Widget para Etapa 5: Teste de Conectividade"""
    
    test_completed = pyqtSignal(bool)  # Sinal com resultado do teste
    
    def __init__(self, parent=None):
        super().__init__(5, parent)
        self.test_result = None
        self.setup_content()
    
    def setup_content(self):
        """Configura o conteúdo da etapa 5"""
        # Botão de teste
        self.test_button = QPushButton("Testar Conexão")
        self.test_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.test_button.setMinimumHeight(50)
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #107C10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0E6A0E;
            }
            QPushButton:pressed {
                background-color: #0C5A0C;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        self.test_button.clicked.connect(self.run_test)
        self.custom_layout.addWidget(self.test_button)
        
        # Área de resultado
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Segoe UI", 11))
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumHeight(60)
        self.custom_layout.addWidget(self.result_label)
    
    def run_test(self):
        """Executa o teste de conectividade"""
        from modules.network_troubleshoot.services.network_checker import NetworkChecker
        
        self.test_button.setEnabled(False)
        self.result_label.setText("Testando conectividade...")
        self.result_label.setStyleSheet("color: #0078D4; padding: 10px;")
        
        # Força atualização da UI
        self.result_label.repaint()
        
        # Executa o teste
        checker = NetworkChecker()
        is_connected = checker.check_internet_connectivity()
        
        self.test_result = is_connected
        
        if is_connected:
            self.result_label.setText("✓ Conexão restabelecida! O problema foi resolvido.")
            self.result_label.setStyleSheet("""
                background-color: #DFF6DD; 
                border: 2px solid #107C10; 
                border-radius: 5px; 
                padding: 15px;
                color: #107C10;
                font-weight: bold;
            """)
        else:
            self.result_label.setText(
                "✗ A conexão ainda não foi restabelecida.\n"
                "É necessário abrir um chamado para o suporte."
            )
            self.result_label.setStyleSheet("""
                background-color: #FDE7E9; 
                border: 2px solid #E81123; 
                border-radius: 5px; 
                padding: 15px;
                color: #E81123;
                font-weight: bold;
            """)
        
        self.test_button.setEnabled(True)
        self.test_completed.emit(is_connected)
    
    def is_complete(self) -> bool:
        """Verifica se o teste foi executado"""
        return self.test_result is not None
    
    def get_test_result(self) -> bool:
        """Retorna o resultado do teste"""
        return self.test_result if self.test_result is not None else False
