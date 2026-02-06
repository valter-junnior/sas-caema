"""
Dialog de seleção de soluções de troubleshooting
"""
from pathlib import Path
import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import PRIMARY_COLOR


class SolutionsDialog(QDialog):
    """Dialog para seleção de soluções de troubleshooting"""
    
    def __init__(self, solutions: list, parent=None):
        """
        Inicializa o dialog
        
        Args:
            solutions: Lista de soluções disponíveis
            parent: Widget pai
        """
        super().__init__(parent)
        self.solutions = solutions
        self.selected_solution = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do dialog"""
        self.setWindowTitle("Executar Solução")
        self.setMinimumSize(500, 400)
        self.resize(600, 500)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Título
        title_label = QLabel("Selecione uma Solução")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {PRIMARY_COLOR}; padding: 10px;")
        layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel(
            "Escolha uma solução de troubleshooting abaixo para iniciar o wizard de diagnóstico:"
        )
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("color: #666666; padding: 0 10px 10px 10px;")
        layout.addWidget(subtitle_label)
        
        # Lista de soluções
        self.solutions_list = QListWidget()
        self.solutions_list.setFont(QFont("Segoe UI", 11))
        self.solutions_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #EEEEEE;
            }
            QListWidget::item:selected {
                background-color: #E8F4F8;
                color: #0078D4;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        self.solutions_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # Adiciona soluções à lista
        for solution in self.solutions:
            item = QListWidgetItem()
            
            # Texto da solução com ícone
            icon = solution.get('icon', '🔧')
            name = solution.get('name', 'Solução sem nome')
            description = solution.get('description', '')
            
            item_text = f"{icon}  {name}"
            if description:
                item_text += f"\n    {description}"
            
            item.setText(item_text)
            item.setData(Qt.UserRole, solution['id'])
            
            self.solutions_list.addItem(item)
        
        # Seleciona primeiro item por padrão
        if self.solutions_list.count() > 0:
            self.solutions_list.setCurrentRow(0)
        
        layout.addWidget(self.solutions_list)
        
        # Botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Botão Cancelar
        cancel_button = QPushButton("Cancelar")
        cancel_button.setFont(QFont("Segoe UI", 10))
        cancel_button.setMinimumHeight(40)
        cancel_button.setMinimumWidth(120)
        cancel_button.setStyleSheet("""
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
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        button_layout.addStretch()
        
        # Botão Executar
        execute_button = QPushButton("Executar")
        execute_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        execute_button.setMinimumHeight(40)
        execute_button.setMinimumWidth(120)
        execute_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton:pressed {{
                background-color: #004578;
            }}
        """)
        execute_button.clicked.connect(self.on_execute)
        button_layout.addWidget(execute_button)
        
        layout.addLayout(button_layout)
    
    def on_item_double_clicked(self, item):
        """Callback quando item é clicado duas vezes"""
        self.on_execute()
    
    def on_execute(self):
        """Callback quando botão executar é clicado"""
        current_item = self.solutions_list.currentItem()
        
        if current_item:
            self.selected_solution = current_item.data(Qt.UserRole)
            self.accept()
    
    def get_selected_solution(self) -> str:
        """
        Retorna o ID da solução selecionada
        
        Returns:
            ID da solução ou None se nenhuma foi selecionada
        """
        return self.selected_solution
