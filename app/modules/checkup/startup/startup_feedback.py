"""
Janela de feedback do checkup automático na inicialização.
Toast moderno no canto inferior direito — visual sincronizado com o app.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QApplication, QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QColor

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts

# ── Constantes ─────────────────────────────────────────────────────────────
_W, _H      = 440, 250
_MARGIN     = 20
_TASKBAR    = 56  # altura estimada da barra de tarefas do Windows

_CLOSE_SUCCESS = 5_000   # ms
_CLOSE_PARTIAL = 10_000
_CLOSE_ERROR   = 12_000


class StartupFeedbackWindow(QWidget):
    """Toast de feedback do checkup automático na inicialização do Windows."""

    closed = pyqtSignal()

    # ── Ciclo de vida ──────────────────────────────────────────────────────

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFixedSize(_W, _H)
        self._build_ui()
        self._apply_shadow()
        self._position()

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._make_header())
        root.addWidget(self._make_body(), stretch=1)
        root.addWidget(self._make_strip())

    def _make_header(self):
        header = QWidget()
        header.setObjectName("sfHeader")
        header.setFixedHeight(52)
        header.setStyleSheet(f"""
            QWidget#sfHeader {{
                background-color: {Colors.HEADER_BG};
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 12, 0)
        layout.setSpacing(0)

        title = QLabel("SAS-Caema  —  Verificação Automática")
        title.setFont(Fonts.heading(10))
        title.setStyleSheet(f"color: {Colors.HEADER_TEXT}; background: transparent;")
        layout.addWidget(title, stretch=1)

        btn = QPushButton("✕")
        btn.setFixedSize(28, 28)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self._dismiss)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {Colors.HEADER_SUBTITLE};
                font-size: 13px;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background: {Colors.HEADER_SURFACE};
                color: {Colors.DANGER};
            }}
        """)
        layout.addWidget(btn)
        return header

    def _make_body(self):
        body = QWidget()
        body.setObjectName("sfBody")
        body.setStyleSheet(f"QWidget#sfBody {{ background-color: {Colors.SURFACE}; }}")

        layout = QVBoxLayout(body)
        layout.setContentsMargins(24, 18, 24, 20)
        layout.setSpacing(0)

        self._status_lbl = QLabel("Iniciando verificação do sistema...")
        self._status_lbl.setFont(Fonts.subheading(11))
        self._status_lbl.setWordWrap(True)
        self._status_lbl.setStyleSheet(
            f"color: {Colors.TEXT_PRIMARY}; background: transparent;"
        )
        layout.addWidget(self._status_lbl)

        layout.addSpacing(4)

        self._detail_lbl = QLabel("")
        self._detail_lbl.setFont(Fonts.caption(9))
        self._detail_lbl.setWordWrap(True)
        self._detail_lbl.setStyleSheet(
            f"color: {Colors.TEXT_MUTED}; background: transparent;"
        )
        layout.addWidget(self._detail_lbl)

        layout.addSpacing(16)

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(8)
        self._set_progress_color(Colors.PRIMARY)
        layout.addWidget(self._progress)

        layout.addSpacing(12)

        self._phase_lbl = QLabel("Aguarde...")
        self._phase_lbl.setFont(Fonts.caption(9))
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.PRIMARY}; background: transparent;"
        )
        layout.addWidget(self._phase_lbl)

        return body

    def _make_strip(self):
        self._strip = QWidget()
        self._strip.setFixedHeight(4)
        self._strip.setStyleSheet(f"""
            background-color: {Colors.PRIMARY};
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        """)
        return self._strip

    # ── Helpers visuais ────────────────────────────────────────────────────

    def _set_progress_color(self, color: str):
        self._progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {Colors.BORDER};
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)

    def _set_accent(self, color: str):
        self._set_progress_color(color)
        self._strip.setStyleSheet(f"""
            background-color: {color};
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        """)

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

    def _position(self):
        screen = QApplication.desktop().screenGeometry()
        self.move(screen.width() - _W - _MARGIN, screen.height() - _H - _TASKBAR)

    # ── Slots públicos (conectados à thread) ───────────────────────────────

    def show_checking(self, module_name: str, progress: int):
        """Fase 1 — verificação em andamento."""
        self._status_lbl.setText("Verificando sistema...")
        self._detail_lbl.setText(f"Analisando: {module_name}")
        self._progress.setValue(progress)
        self._phase_lbl.setText("🔍  Fase 1 de 2 — Verificação")
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.PRIMARY}; background: transparent;"
        )
        self._set_accent(Colors.PRIMARY)

    def show_fixing(self, module_name: str, progress: int):
        """Fase 2 — correção em andamento."""
        self._status_lbl.setText("Corrigindo problemas encontrados...")
        self._detail_lbl.setText(f"Aplicando correção: {module_name}")
        self._progress.setValue(progress)
        self._phase_lbl.setText("🔧  Fase 2 de 2 — Correção")
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.WARNING}; background: transparent;"
        )
        self._set_accent(Colors.WARNING)

    def show_success(self, message: str = ""):
        """Conclusão sem problemas encontrados."""
        self._status_lbl.setText("Sistema verificado com sucesso!")
        self._detail_lbl.setText("Nenhum problema encontrado. Tudo em ordem.")
        self._progress.setValue(100)
        self._phase_lbl.setText("✓  Concluído")
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.SUCCESS}; background: transparent;"
        )
        self._set_accent(Colors.SUCCESS)
        QTimer.singleShot(_CLOSE_SUCCESS, self._dismiss)

    def show_partial_success(self, fixed: int, total: int):
        """Alguns problemas corrigidos, outros precisam de atenção manual."""
        self._status_lbl.setText(
            f"{fixed} de {total} problema(s) corrigido(s) automaticamente."
        )
        self._detail_lbl.setText(
            "Os demais requerem atenção manual. Abra o SAS-Caema para detalhes."
        )
        self._progress.setValue(100)
        self._phase_lbl.setText("⚠  Concluído com avisos")
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.WARNING}; background: transparent;"
        )
        self._set_accent(Colors.WARNING)
        QTimer.singleShot(_CLOSE_PARTIAL, self._dismiss)

    def show_error(self, message: str):
        """Erro crítico durante o checkup."""
        self._status_lbl.setText("Erro durante a verificação automática.")
        self._detail_lbl.setText(message or "Verifique os logs para mais detalhes.")
        self._progress.setValue(100)
        self._phase_lbl.setText("✗  Falha")
        self._phase_lbl.setStyleSheet(
            f"color: {Colors.DANGER}; background: transparent;"
        )
        self._set_accent(Colors.DANGER)
        QTimer.singleShot(_CLOSE_ERROR, self._dismiss)

    # ── Ciclo de vida ──────────────────────────────────────────────────────

    def _dismiss(self):
        self.close()
        self.closed.emit()

    def showEvent(self, event):
        """Slide-up suave ao exibir."""
        super().showEvent(event)
        screen = QApplication.desktop().screenGeometry()
        x = screen.width() - _W - _MARGIN
        y_final = screen.height() - _H - _TASKBAR

        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(350)
        self._anim.setStartValue(QRect(x, y_final + 20, _W, _H))
        self._anim.setEndValue(QRect(x, y_final, _W, _H))
        self._anim.start()
