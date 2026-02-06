"""
Janela principal do wizard de troubleshooting de rede
"""
from pathlib import Path
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QStackedWidget, QWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.network_troubleshoot import config
from modules.network_troubleshoot.services.step_validator import StepValidator
from modules.network_troubleshoot.views.step_widgets import (
    Step1Widget, Step2Widget, Step3Widget, Step4Widget, Step5Widget
)


class WizardWindow(QDialog):
    """Janela do wizard de troubleshooting de rede"""
    
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
