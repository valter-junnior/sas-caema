"""
Widgets para cada etapa do wizard de troubleshooting
"""
from pathlib import Path
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from modules.network_troubleshoot import config


class BaseStepWidget(QWidget):
    """Classe base para widgets de etapa"""
    
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
