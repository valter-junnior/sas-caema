"""
Janela de feedback visual para checkup na inicialização.
Exibe progresso em tempo real no canto inferior direito com animação.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QApplication, QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QFont, QColor

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts


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
        self.add_shadow()
        self.position_window()
        
    def init_ui(self):
        """Inicializa a interface"""
        # Janela maior para evitar sobreposições
        self.setFixedSize(450, 320)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # Header com botão fechar
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 10, 10, 0)
        header_layout.addStretch()
        
        # Botão fechar
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(32, 32)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close_with_animation)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #95a5a6;
                font-size: 28px;
                font-weight: normal;
                border-radius: 16px;
                padding-bottom: 4px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                color: #e74c3c;
            }
        """)
        header_layout.addWidget(self.close_button, 0, Qt.AlignTop)
        main_layout.addLayout(header_layout)
        
        # Container de conteúdo - mais espaçamento
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(35, 10, 35, 35)
        content_layout.setSpacing(0)
        
        # Título - altura fixa maior
        self.title_label = QLabel("SAS-Caema")
        self.title_label.setFont(Fonts.heading(16))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedSize(380, 40)
        self.title_label.setScaledContents(False)
        content_layout.addWidget(self.title_label, 0, Qt.AlignHCenter)
        
        # Espaço fixo
        content_layout.addSpacing(18)
        
        # Mensagem de status - SEM WordWrap para evitar expansão
        # self.status_label = QLabel("Iniciando verificação...")
        self.status_label = QLabel("Corrigindo problemas encontrados...")
        self.status_label.setFont(Fonts.subheading(11))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(False)
        self.status_label.setFixedSize(380, 65)
        self.status_label.setScaledContents(False)
        content_layout.addWidget(self.status_label, 0, Qt.AlignHCenter)
        
        # Espaço fixo
        content_layout.addSpacing(22)
        
        # Barra de progresso - altura fixa
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedSize(380, 12)
        content_layout.addWidget(self.progress_bar, 0, Qt.AlignHCenter)
        
        # Espaço fixo
        content_layout.addSpacing(22)
        
        # Detalhes (módulo atual) - altura fixa
        self.detail_label = QLabel("")
        self.detail_label.setFont(Fonts.caption(9))
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setFixedSize(380, 35)
        self.detail_label.setScaledContents(False)
        content_layout.addWidget(self.detail_label, 0, Qt.AlignHCenter)
        
        main_layout.addLayout(content_layout)
        
        # Estilo padrão
        self.update_style(Colors.PRIMARY)
        
    def update_style(self, color):
        """Atualiza o estilo da janela com a cor especificada"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                border: 3px solid {color};
                border-radius: 20px;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: #f5f5f5;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)
        
        # Estilo especial para título
        self.title_label.setStyleSheet(f"""
            color: {color};
            background-color: transparent;
            border: none;
            font-weight: bold;
        """)
        
        # Estilo para status
        self.status_label.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            background-color: transparent;
            border: none;
        """)
        
        # Estilo para detalhes
        self.detail_label.setStyleSheet(f"""
            color: {Colors.TEXT_MUTED};
            background-color: transparent;
            border: none;
        """)
        
        # Reaplica estilo do botão fechar para não ser sobrescrito
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #95a5a6;
                font-size: 28px;
                font-weight: normal;
                border-radius: 16px;
                padding-bottom: 4px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                color: #e74c3c;
            }
        """)
    
    def add_shadow(self):
        """Adiciona sombra suave à janela"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
    
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
        # self.set_status("Verificando sistema...", progress)
        # self.set_detail(f"Analisando: {module_name}")
        self.update_style(Colors.PRIMARY)
    
    def show_fixing(self, module_name: str, progress: int):
        """
        Mostra que está corrigindo um problema
        
        Args:
            module_name: Nome do módulo
            progress: Progresso atual (0-100)
        """
        self.update_style(Colors.WARNING)
    
    def show_success(self, message: str = "Sistema verificado com sucesso"):
        """
        Mostra mensagem de sucesso
        
        Args:
            message: Mensagem de sucesso
        """
        self.set_status(message, 100)
        self.set_detail("Sua máquina está funcionando perfeitamente")
        self.update_style(Colors.SUCCESS)
        
        # Fecha automaticamente após 10 segundos
        QTimer.singleShot(10000, self.close_with_animation)
    
    def show_error(self, message: str = "Erro ao verificar o sistema"):
        """
        Mostra mensagem de erro
        
        Args:
            message: Mensagem de erro
        """
        self.set_status(message, 100)
        self.set_detail("Verifique os logs para mais detalhes")
        self.update_style(Colors.DANGER)
        
        # Fecha automaticamente após 15 segundos
        QTimer.singleShot(15000, self.close_with_animation)
    
    def show_partial_success(self, fixed: int, total: int):
        """
        Mostra sucesso parcial
        
        Args:
            fixed: Número de problemas corrigidos
            total: Total de problemas encontrados
        """
        self.set_status(f"{fixed} de {total} problemas foram corrigidos", 100)
        self.set_detail("Alguns problemas requerem atenção manual")
        self.update_style(Colors.WARNING)
        
        # Fecha automaticamente após 13 segundos
        QTimer.singleShot(13000, self.close_with_animation)
    
    def close_with_animation(self):
        """Fecha a janela com animação de fade out"""
        # Por enquanto fecha direto, mas pode adicionar animação depois
        self.close()
        self.closed.emit()
    
    def showEvent(self, event):
        """Evento ao mostrar a janela - adiciona animação de entrada suave"""
        super().showEvent(event)
        
        # Animação de slide-up suave
        screen = QApplication.desktop().screenGeometry()
        final_x = screen.width() - self.width() - 20
        final_y = screen.height() - self.height() - 60
        
        # Posição inicial (20px mais abaixo)
        start_y = final_y + 20
        
        # Animação suave para posição final
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)  # 400ms - mais suave
        self.animation.setStartValue(QRect(final_x, start_y, self.width(), self.height()))
        self.animation.setEndValue(QRect(final_x, final_y, self.width(), self.height()))
        self.animation.start()
