"""
Janela de feedback visual para checkup na inicialização
Exibe progresso em tempo real no canto inferior direito
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar, 
                             QApplication)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QFont

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import PRIMARY_COLOR, SUCCESS_COLOR, ERROR_COLOR


class StartupFeedbackWindow(QWidget):
    """
    Janela de feedback visual para o checkup na inicialização do Windows.
    Aparece no canto inferior direito com animação.
    """
    
    closed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.init_ui()
        self.position_window()
        
    def init_ui(self):
        """Inicializa a interface"""
        self.setFixedSize(400, 200)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Título
        self.title_label = QLabel("🔧 SAS-Caema")
        title_font = QFont("Segoe UI", 14, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Mensagem de status
        self.status_label = QLabel("Iniciando verificação do sistema...")
        status_font = QFont("Segoe UI", 10)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        layout.addWidget(self.progress_bar)
        
        # Detalhes (módulo atual)
        self.detail_label = QLabel("")
        detail_font = QFont("Segoe UI", 9)
        self.detail_label.setFont(detail_font)
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setStyleSheet("color: #666666;")
        layout.addWidget(self.detail_label)
        
        # Estilo padrão
        self.update_style(PRIMARY_COLOR)
        
    def update_style(self, color):
        """Atualiza o estilo da janela com a cor especificada"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
            }}
            QProgressBar {{
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
    
    def position_window(self):
        """Posiciona a janela no canto inferior direito"""
        screen = QApplication.desktop().screenGeometry()
        
        # Margem de 20px das bordas
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 60  # 60px para barra de tarefas
        
        self.move(x, y)
    
    def set_status(self, message: str, progress: int = None):
        """
        Atualiza a mensagem de status
        
        Args:
            message: Mensagem a exibir
            progress: Progresso de 0-100 (opcional)
        """
        self.status_label.setText(message)
        
        if progress is not None:
            self.progress_bar.setValue(progress)
    
    def set_detail(self, detail: str):
        """
        Atualiza o detalhe/módulo atual
        
        Args:
            detail: Texto do detalhe
        """
        self.detail_label.setText(detail)
    
    def show_checking(self, module_name: str, progress: int):
        """
        Mostra que está verificando um módulo
        
        Args:
            module_name: Nome do módulo
            progress: Progresso atual (0-100)
        """
        self.set_status("Verificando sistema...", progress)
        self.set_detail(f"📋 {module_name}")
        self.update_style(PRIMARY_COLOR)
    
    def show_fixing(self, module_name: str, progress: int):
        """
        Mostra que está corrigindo um problema
        
        Args:
            module_name: Nome do módulo
            progress: Progresso atual (0-100)
        """
        self.set_status("Corrigindo problemas...", progress)
        self.set_detail(f"🔧 {module_name}")
        self.update_style("#FF8C00")  # Laranja
    
    def show_success(self, message: str = "Sistema verificado com sucesso!"):
        """
        Mostra mensagem de sucesso
        
        Args:
            message: Mensagem de sucesso
        """
        self.set_status(message, 100)
        self.set_detail("✓ Tudo OK")
        self.update_style(SUCCESS_COLOR)
        
        # Fecha automaticamente após 3 segundos
        QTimer.singleShot(3000, self.close_with_animation)
    
    def show_error(self, message: str = "Erro ao verificar o sistema"):
        """
        Mostra mensagem de erro
        
        Args:
            message: Mensagem de erro
        """
        self.set_status(message, 100)
        self.set_detail("✗ Verifique os logs")
        self.update_style(ERROR_COLOR)
        
        # Fecha automaticamente após 5 segundos
        QTimer.singleShot(5000, self.close_with_animation)
    
    def show_partial_success(self, fixed: int, total: int):
        """
        Mostra sucesso parcial
        
        Args:
            fixed: Número de problemas corrigidos
            total: Total de problemas encontrados
        """
        self.set_status(f"{fixed} de {total} problemas corrigidos", 100)
        self.set_detail("⚠ Alguns problemas persistem")
        self.update_style("#FF8C00")
        
        # Fecha automaticamente após 4 segundos
        QTimer.singleShot(4000, self.close_with_animation)
    
    def close_with_animation(self):
        """Fecha a janela com animação de fade out"""
        # Por enquanto fecha direto, mas pode adicionar animação depois
        self.close()
        self.closed.emit()
    
    def showEvent(self, event):
        """Evento ao mostrar a janela - adiciona animação de entrada"""
        super().showEvent(event)
        
        # Animação de slide in (opcional - pode ser removida se preferir)
        # Começa um pouco abaixo e sobe
        screen = QApplication.desktop().screenGeometry()
        final_x = screen.width() - self.width() - 20
        final_y = screen.height() - self.height() - 60
        
        # Posição inicial (mais abaixo)
        self.move(final_x, screen.height())
        
        # Animação para posição final
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 300ms
        self.animation.setStartValue(QRect(final_x, screen.height(), self.width(), self.height()))
        self.animation.setEndValue(QRect(final_x, final_y, self.width(), self.height()))
        self.animation.start()
