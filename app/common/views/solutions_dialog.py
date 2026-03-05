"""
Dialog de seleção de soluções — layout moderno baseado em cards.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import PrimaryButton, SecondaryButton, BodyLabel


class SolutionCard(QFrame):
    """Card selecionável para uma solução de troubleshooting."""

    selected = pyqtSignal(str)  # emite o id da solução

    def __init__(self, solution: dict, parent=None):
        super().__init__(parent)
        self._solution_id = solution['id']
        self._is_selected = False
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._apply_style(selected=False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(14)

        icon_lbl = QLabel(solution.get('icon', '🔧'))
        icon_lbl.setFont(QFont(Fonts.FAMILY, 18))
        icon_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        icon_lbl.setFixedWidth(40)
        icon_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(3)

        name_lbl = QLabel(solution.get('name', ''))
        name_lbl.setFont(Fonts.heading(11))
        name_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        text_col.addWidget(name_lbl)

        desc_lbl = QLabel(solution.get('description', ''))
        desc_lbl.setFont(Fonts.body(9))
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
        text_col.addWidget(desc_lbl)

        layout.addLayout(text_col, stretch=1)

    def _apply_style(self, selected: bool):
        if selected:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.PRIMARY_SURFACE};
                    border: 2px solid {Colors.PRIMARY};
                    border-radius: 8px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.SURFACE};
                    border: 1.5px solid {Colors.BORDER};
                    border-radius: 8px;
                }}
                QFrame:hover {{
                    border-color: {Colors.PRIMARY};
                    background-color: {Colors.BACKGROUND};
                }}
            """)

    def set_selected(self, selected: bool):
        self._is_selected = selected
        self._apply_style(selected)

    def mousePressEvent(self, event):
        self.selected.emit(self._solution_id)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.selected.emit(self._solution_id)
        # Propaga para o dialog encontrar via parent
        parent = self.parent()
        while parent and not isinstance(parent, SolutionsDialog):
            parent = parent.parent()
        if parent:
            parent.accept()

    @property
    def solution_id(self) -> str:
        return self._solution_id


class SolutionsDialog(QDialog):
    """Dialog para selecionar uma solução de troubleshooting."""

    def __init__(self, solutions: list, parent=None):
        super().__init__(parent)
        self._solutions = solutions
        self._selected_id = solutions[0]['id'] if solutions else None
        self._cards: list = []
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Executar Solução")
        self.setMinimumSize(520, 380)
        self.setModal(True)
        self.setStyleSheet(f"QDialog {{ background-color: {Colors.SURFACE}; }}")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet(
            f"background-color: {Colors.BACKGROUND}; "
            f"border-bottom: 1px solid {Colors.BORDER};"
        )
        hl = QVBoxLayout(header)
        hl.setContentsMargins(28, 22, 28, 22)
        hl.setSpacing(4)

        title = QLabel("Executar Solução")
        title.setFont(Fonts.heading(14))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        hl.addWidget(title)

        subtitle = BodyLabel("Selecione um wizard de diagnóstico guiado para iniciar.")
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
        hl.addWidget(subtitle)

        root.addWidget(header)

        # Área de cards
        cards_widget = QWidget()
        cards_widget.setStyleSheet(f"background-color: {Colors.SURFACE};")
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.setContentsMargins(24, 20, 24, 20)
        cards_layout.setSpacing(10)

        for solution in self._solutions:
            card = SolutionCard(solution)
            card.selected.connect(self._on_card_selected)
            self._cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()

        # Pré-seleciona o primeiro
        if self._cards:
            self._cards[0].set_selected(True)

        root.addWidget(cards_widget, stretch=1)

        # Footer com botões
        footer = QWidget()
        footer.setStyleSheet(
            f"background-color: {Colors.BACKGROUND}; "
            f"border-top: 1px solid {Colors.BORDER};"
        )
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 14, 24, 14)
        fl.setSpacing(10)

        cancel_btn = SecondaryButton("Cancelar")
        cancel_btn.setMinimumWidth(110)
        cancel_btn.clicked.connect(self.reject)
        fl.addWidget(cancel_btn)

        fl.addStretch()

        execute_btn = PrimaryButton("Executar Solução")
        execute_btn.setMinimumWidth(150)
        execute_btn.clicked.connect(self.accept)
        fl.addWidget(execute_btn)

        root.addWidget(footer)

    def _on_card_selected(self, solution_id: str):
        self._selected_id = solution_id
        for card in self._cards:
            card.set_selected(card.solution_id == solution_id)

    def get_selected_solution(self) -> str:
        return self._selected_id

