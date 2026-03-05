"""
Sistema de design central do SAS-Caema.
Fonte única de verdade para todas as cores, fontes e estilos (princípio DRY).
"""
from PyQt5.QtGui import QFont


class Colors:
    # Primária (azul)
    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    PRIMARY_PRESSED = "#1E40AF"
    PRIMARY_SURFACE = "#EFF6FF"
    PRIMARY_BORDER = "#BFDBFE"

    # Sucesso (verde)
    SUCCESS = "#16A34A"
    SUCCESS_DARK = "#15803D"
    SUCCESS_SURFACE = "#F0FDF4"
    SUCCESS_BORDER = "#BBF7D0"

    # Perigo (vermelho)
    DANGER = "#DC2626"
    DANGER_DARK = "#B91C1C"
    DANGER_SURFACE = "#FEF2F2"
    DANGER_BORDER = "#FECACA"

    # Aviso (âmbar)
    WARNING = "#D97706"
    WARNING_SURFACE = "#FFFBEB"
    WARNING_BORDER = "#FDE68A"

    # Neutros
    SURFACE = "#FFFFFF"
    BACKGROUND = "#F8FAFC"
    BORDER = "#E2E8F0"
    BORDER_HOVER = "#CBD5E1"

    # Texto
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#94A3B8"
    TEXT_INVERSE = "#FFFFFF"

    # Header escuro
    HEADER_BG = "#0F172A"
    HEADER_SURFACE = "#1E293B"
    HEADER_TEXT = "#F1F5F9"
    HEADER_SUBTITLE = "#94A3B8"
    HEADER_ACCENT = "#2563EB"


class Fonts:
    FAMILY = "Segoe UI"

    @staticmethod
    def make(size: int, bold: bool = False) -> QFont:
        f = QFont(Fonts.FAMILY, size)
        f.setWeight(QFont.Bold if bold else QFont.Normal)
        return f

    @classmethod
    def title(cls, size: int = 20) -> QFont:
        return cls.make(size, bold=True)

    @classmethod
    def heading(cls, size: int = 13) -> QFont:
        return cls.make(size, bold=True)

    @classmethod
    def subheading(cls, size: int = 11) -> QFont:
        return cls.make(size, bold=False)

    @classmethod
    def body(cls, size: int = 10) -> QFont:
        return cls.make(size)

    @classmethod
    def caption(cls, size: int = 9) -> QFont:
        return cls.make(size)


class Styles:
    """Templates QSS reutilizáveis — todos os botões, cards e layout global."""

    @staticmethod
    def btn_primary() -> str:
        c = Colors
        return f"""
            QPushButton {{
                background-color: {c.PRIMARY};
                color: {c.TEXT_INVERSE};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-family: {Fonts.FAMILY};
                font-size: 10pt;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {c.PRIMARY_DARK}; }}
            QPushButton:pressed {{ background-color: {c.PRIMARY_PRESSED}; }}
            QPushButton:disabled {{
                background-color: {c.BORDER};
                color: {c.TEXT_MUTED};
            }}
        """

    @staticmethod
    def btn_secondary() -> str:
        c = Colors
        return f"""
            QPushButton {{
                background-color: {c.SURFACE};
                color: {c.TEXT_PRIMARY};
                border: 1.5px solid {c.BORDER};
                border-radius: 6px;
                padding: 8px 20px;
                font-family: {Fonts.FAMILY};
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {c.BACKGROUND};
                border-color: {c.BORDER_HOVER};
            }}
            QPushButton:pressed {{ background-color: {c.BORDER}; }}
            QPushButton:disabled {{
                color: {c.TEXT_MUTED};
                border-color: {c.BORDER};
            }}
        """

    @staticmethod
    def btn_success() -> str:
        c = Colors
        return f"""
            QPushButton {{
                background-color: {c.SUCCESS};
                color: {c.TEXT_INVERSE};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-family: {Fonts.FAMILY};
                font-size: 10pt;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {c.SUCCESS_DARK}; }}
            QPushButton:disabled {{
                background-color: {c.BORDER};
                color: {c.TEXT_MUTED};
            }}
        """

    @staticmethod
    def btn_ghost_danger() -> str:
        c = Colors
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {c.DANGER};
                border: 1.5px solid {c.DANGER_BORDER};
                border-radius: 6px;
                padding: 8px 20px;
                font-family: {Fonts.FAMILY};
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {c.DANGER_SURFACE};
                border-color: {c.DANGER};
            }}
        """

    @staticmethod
    def card() -> str:
        c = Colors
        return f"""
            QFrame#card {{
                background-color: {c.SURFACE};
                border: 1px solid {c.BORDER};
                border-radius: 10px;
            }}
        """

    @staticmethod
    def global_app() -> str:
        """Stylesheet global aplicado ao QApplication."""
        c = Colors
        return f"""
            QMainWindow, QDialog, QWidget {{
                background-color: {c.BACKGROUND};
                font-family: {Fonts.FAMILY};
                font-size: 10pt;
                color: {c.TEXT_PRIMARY};
            }}
            QScrollBar:vertical {{
                background: {c.BACKGROUND};
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {c.BORDER_HOVER};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {c.TEXT_MUTED};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar:horizontal {{
                height: 0;
            }}
            QMenuBar {{
                background-color: {c.HEADER_BG};
                color: {c.HEADER_TEXT};
                padding: 2px 0;
                font-size: 10pt;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 5px 14px;
            }}
            QMenuBar::item:selected {{
                background-color: {c.HEADER_SURFACE};
                border-radius: 4px;
            }}
            QMenu {{
                background-color: {c.SURFACE};
                border: 1px solid {c.BORDER};
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 7px 22px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {c.PRIMARY_SURFACE};
                color: {c.PRIMARY};
            }}
            QStatusBar {{
                background-color: {c.BACKGROUND};
                border-top: 1px solid {c.BORDER};
                color: {c.TEXT_SECONDARY};
                padding: 2px 10px;
                font-size: 9pt;
            }}
            QToolTip {{
                background-color: {c.TEXT_PRIMARY};
                color: {c.TEXT_INVERSE};
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 9pt;
            }}
            QProgressBar {{
                background-color: {c.BORDER};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {c.PRIMARY};
                border-radius: 4px;
            }}
            QCheckBox {{
                color: {c.TEXT_PRIMARY};
                font-size: 10pt;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {c.BORDER_HOVER};
                border-radius: 3px;
                background-color: {c.SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background-color: {c.PRIMARY};
                border-color: {c.PRIMARY};
            }}
            QCheckBox::indicator:hover {{
                border-color: {c.PRIMARY};
            }}
        """
