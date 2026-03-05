"""
Biblioteca de componentes reutilizáveis do SAS-Caema.
Centraliza widgets compartilhados para manter o princípio DRY em todas as views.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts, Styles


# ---------------------------------------------------------------------------
# Botões
# ---------------------------------------------------------------------------

class PrimaryButton(QPushButton):
    """Botão de ação principal (azul)."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(Styles.btn_primary())
        self.setFont(Fonts.body(10))
        self.setMinimumHeight(38)
        self.setCursor(Qt.PointingHandCursor)


class SecondaryButton(QPushButton):
    """Botão secundário / contorno."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(Styles.btn_secondary())
        self.setFont(Fonts.body(10))
        self.setMinimumHeight(38)
        self.setCursor(Qt.PointingHandCursor)


class SuccessButton(QPushButton):
    """Botão de ação verde (sucesso)."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(Styles.btn_success())
        self.setFont(Fonts.body(10))
        self.setMinimumHeight(38)
        self.setCursor(Qt.PointingHandCursor)


class GhostDangerButton(QPushButton):
    """Botão ghost de perigo/cancelar."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(Styles.btn_ghost_danger())
        self.setFont(Fonts.body(10))
        self.setMinimumHeight(38)
        self.setCursor(Qt.PointingHandCursor)


# ---------------------------------------------------------------------------
# Containers / Layout
# ---------------------------------------------------------------------------

class Card(QFrame):
    """Card branco com borda e sombra suave."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet(Styles.card())
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 18))
        self.setGraphicsEffect(shadow)


class Divider(QFrame):
    """Separador horizontal fino."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFixedHeight(1)
        self.setStyleSheet(f"background-color: {Colors.BORDER}; border: none;")


# ---------------------------------------------------------------------------
# Labels de texto
# ---------------------------------------------------------------------------

class TitleLabel(QLabel):
    """Label de título grande (20pt bold)."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setFont(Fonts.title(20))
        self.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        self.setWordWrap(True)


class HeadingLabel(QLabel):
    """Label de cabeçalho de seção (13pt bold)."""
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setFont(Fonts.heading(13))
        self.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        self.setWordWrap(True)


class BodyLabel(QLabel):
    """Label de corpo de texto padrão (10pt)."""
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setFont(Fonts.body(10))
        self.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
        self.setWordWrap(True)


class CaptionLabel(QLabel):
    """Label de legenda pequena e discreta (9pt)."""
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setFont(Fonts.caption(9))
        self.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent;")
        self.setWordWrap(True)


# ---------------------------------------------------------------------------
# Widgets compostos
# ---------------------------------------------------------------------------

class HeaderBar(QWidget):
    """Barra de header escura com título e subtítulo."""
    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.HEADER_BG};
                border-bottom: 3px solid {Colors.PRIMARY};
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 22, 32, 22)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(Fonts.title(20))
        title_label.setStyleSheet(
            f"color: {Colors.HEADER_TEXT}; background: transparent; border: none;"
        )
        layout.addWidget(title_label)

        if subtitle:
            sub = QLabel(subtitle)
            sub.setFont(Fonts.body(10))
            sub.setStyleSheet(
                f"color: {Colors.HEADER_SUBTITLE}; background: transparent; border: none;"
            )
            layout.addWidget(sub)


class InfoBanner(QFrame):
    """Banner colorido para mensagens de info/sucesso/aviso/erro."""

    _PALETTE = {
        'info':    (Colors.PRIMARY, Colors.PRIMARY_SURFACE, Colors.PRIMARY_BORDER),
        'success': (Colors.SUCCESS, Colors.SUCCESS_SURFACE, Colors.SUCCESS_BORDER),
        'warning': (Colors.WARNING, Colors.WARNING_SURFACE, Colors.WARNING_BORDER),
        'error':   (Colors.DANGER,  Colors.DANGER_SURFACE,  Colors.DANGER_BORDER),
    }

    def __init__(self, text: str, kind: str = 'info', parent=None):
        super().__init__(parent)
        self.setObjectName("infoBanner")
        color, bg, border = self._PALETTE.get(kind, self._PALETTE['info'])
        self.setStyleSheet(f"""
            QFrame#infoBanner {{
                background-color: {bg};
                border: 1px solid {border};
                border-left: 4px solid {color};
                border-radius: 6px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        label = QLabel(text)
        label.setFont(Fonts.body(10))
        label.setWordWrap(True)
        label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(label)
