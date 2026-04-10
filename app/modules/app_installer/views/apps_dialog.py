"""
Dialog de instalação de aplicativos — grid plano com ícones reais dos EXEs.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QScrollArea, QFrame, QMessageBox, QLineEdit, QGridLayout,
    QProgressDialog,
)
from PyQt5.QtCore import Qt, pyqtSignal, QFileInfo, QThread
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtWidgets import QFileIconProvider

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import PrimaryButton, SecondaryButton
from modules.app_installer.services.catalog_service import CatalogService, AppEntry

_ICON_PROVIDER = QFileIconProvider()
_COLS = 4  # colunas no grid


def _get_icon(app: AppEntry) -> QIcon:
    if app.is_available:
        return _ICON_PROVIDER.icon(QFileInfo(str(app.installer_path)))
    return _ICON_PROVIDER.icon(QFileIconProvider.File)


class _DownloadThread(QThread):
    """Thread que baixa um instalador remoto e emite progresso."""

    progress = pyqtSignal(int, int)   # downloaded_bytes, total_bytes
    success = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, filename: str, dest: Path):
        super().__init__()
        self._filename = filename
        self._dest = dest

    def run(self):
        try:
            from common.services.assets_service import download_app
            download_app(
                self._filename,
                self._dest,
                progress_callback=lambda d, t: self.progress.emit(d, t),
            )
            self.success.emit()
        except Exception as exc:
            self.failed.emit(str(exc))


class AppCard(QFrame):
    """Card de aplicativo no grid."""

    install_requested = pyqtSignal(object)  # AppEntry

    def __init__(self, app: AppEntry, parent=None):
        super().__init__(parent)
        self._app = app
        self.setObjectName("appCard")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(168, 190)
        self._apply_style()
        self._build_ui()

    def _apply_style(self, hover: bool = False):
        border = Colors.PRIMARY if hover else Colors.BORDER
        bg = Colors.PRIMARY_SURFACE if hover else Colors.SURFACE
        self.setStyleSheet(f"""
            QFrame#appCard {{
                background-color: {bg};
                border: 1.5px solid {border};
                border-radius: 10px;
            }}
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(4)

        # Ícone do EXE (48×48)
        icon = _get_icon(self._app)
        pixmap = icon.pixmap(48, 48)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(pixmap)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFixedHeight(52)
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(icon_lbl)

        # Nome
        name_lbl = QLabel(self._app.display_name())
        name_lbl.setFont(Fonts.heading(9))
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setWordWrap(True)
        name_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent; border: none;")
        layout.addWidget(name_lbl)

        # Versão
        if self._app.display_version():
            ver_lbl = QLabel(self._app.display_version())
            ver_lbl.setFont(Fonts.caption(8))
            ver_lbl.setAlignment(Qt.AlignCenter)
            ver_lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent; border: none;")
            layout.addWidget(ver_lbl)

        # Empresa
        if self._app.display_company():
            co_lbl = QLabel(self._app.display_company())
            co_lbl.setFont(Fonts.caption(7))
            co_lbl.setAlignment(Qt.AlignCenter)
            co_lbl.setWordWrap(True)
            co_lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent; border: none;")
            layout.addWidget(co_lbl)

        layout.addStretch()

        # Badge disponibilidade
        if self._app.is_available:
            badge = QLabel("● Disponível")
            badge.setStyleSheet(f"color: {Colors.SUCCESS}; background: transparent; border: none;")
        else:
            badge = QLabel("⬇ Download ao instalar")
            badge.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent; border: none;")
        badge.setFont(Fonts.caption(7))
        badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(badge)

        btn = PrimaryButton("Instalar")
        btn.setMinimumHeight(32)
        btn.clicked.connect(lambda: self.install_requested.emit(self._app))
        layout.addWidget(btn)

    def enterEvent(self, event):
        self._apply_style(hover=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style(hover=False)
        super().leaveEvent(event)


class _CatalogUpdateThread(QThread):
    """Baixa catalog.csv remoto em background."""

    updated = pyqtSignal()   # emitido quando o arquivo foi realmente alterado

    def run(self):
        try:
            from common.services.assets_service import download_catalog
            from config import APPS_DIR
            import hashlib
            dest = APPS_DIR / "catalog.csv"
            before = dest.read_bytes() if dest.exists() else b""
            download_catalog(dest, timeout=10)
            after = dest.read_bytes() if dest.exists() else b""
            if before != after:
                self.updated.emit()
        except Exception:
            pass  # sem internet: usa cache local


class AppsDialog(QDialog):
    """Dialog principal do instalador de aplicativos."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._download_threads: list[_DownloadThread] = []
        self._catalog_thread: _CatalogUpdateThread | None = None
        self._service = CatalogService()
        self._all_apps = self._service.get_all()
        self._build_ui()
        self._start_catalog_update()

    def _start_catalog_update(self):
        """Inicia download do catalog.csv em background; recarrega grid se mudar."""
        self._catalog_thread = _CatalogUpdateThread()
        self._catalog_thread.updated.connect(self._on_catalog_updated)
        self._catalog_thread.start()

    def _on_catalog_updated(self):
        """Chamado na thread principal quando o catálogo foi atualizado."""
        self._service.reload()
        self._all_apps = self._service.get_all()
        current_search = self._search.text().strip()
        if current_search:
            self._on_search(current_search)
        else:
            self._render_apps(self._all_apps)

    def _build_ui(self):
        self.setWindowTitle("Instalador de Aplicativos")
        self.setMinimumSize(720, 540)
        self.resize(820, 600)
        self.setStyleSheet(f"QDialog {{ background-color: {Colors.BACKGROUND}; }}")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ───────────────────────────────────────────────
        header = QWidget()
        header.setObjectName("appsHeader")
        header.setStyleSheet(f"QWidget#appsHeader {{ background-color: {Colors.HEADER_BG}; }}")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(28, 18, 28, 18)
        hl.setSpacing(16)

        title_col = QVBoxLayout()
        title_col.setSpacing(3)
        t = QLabel("📦  Instalador de Aplicativos")
        t.setFont(Fonts.heading(14))
        t.setStyleSheet(f"color: {Colors.HEADER_TEXT}; background: transparent;")
        title_col.addWidget(t)
        s = QLabel("Instale os principais programas com um clique")
        s.setFont(Fonts.body(9))
        s.setStyleSheet(f"color: {Colors.HEADER_SUBTITLE}; background: transparent;")
        title_col.addWidget(s)
        hl.addLayout(title_col, stretch=1)

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Buscar...")
        self._search.setFixedSize(200, 36)
        self._search.setFont(Fonts.body(10))
        self._search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.HEADER_SURFACE};
                color: {Colors.HEADER_TEXT};
                border: 1px solid {Colors.HEADER_SURFACE};
                border-radius: 6px;
                padding: 0 10px;
            }}
            QLineEdit:focus {{ border: 1px solid {Colors.PRIMARY}; }}
        """)
        self._search.textChanged.connect(self._on_search)
        hl.addWidget(self._search)
        root.addWidget(header)

        # ── Scroll + grid ────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._grid_widget = QWidget()
        self._grid_widget.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setContentsMargins(28, 24, 28, 24)
        self._grid_layout.setSpacing(16)

        scroll.setWidget(self._grid_widget)
        root.addWidget(scroll, stretch=1)

        # ── Rodapé ───────────────────────────────────────────────
        footer = QWidget()
        footer.setObjectName("appsFooter")
        footer.setFixedHeight(58)
        footer.setStyleSheet(f"""
            QWidget#appsFooter {{
                background-color: {Colors.SURFACE};
                border-top: 1px solid {Colors.BORDER};
            }}
        """)
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 0, 24, 0)
        self._count_lbl = QLabel()
        self._count_lbl.setFont(Fonts.caption(9))
        self._count_lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent;")
        fl.addWidget(self._count_lbl)
        fl.addStretch()
        close_btn = SecondaryButton("Fechar")
        close_btn.clicked.connect(self.reject)
        fl.addWidget(close_btn)
        root.addWidget(footer)

        self._render_apps(self._all_apps)

    def _render_apps(self, apps: list):
        # Limpa grid
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        if not apps:
            lbl = QLabel("Nenhum aplicativo encontrado.")
            lbl.setFont(Fonts.body(11))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED}; background: transparent;")
            self._grid_layout.addWidget(lbl, 0, 0, 1, _COLS, Qt.AlignCenter)
            self._count_lbl.setText("0 aplicativos")
            return

        for i, app in enumerate(apps):
            card = AppCard(app)
            card.install_requested.connect(self._on_install)
            self._grid_layout.addWidget(card, i // _COLS, i % _COLS)

        # Padding expansível na linha final
        self._grid_layout.setRowStretch(len(apps) // _COLS + 1, 1)

        available = sum(1 for a in apps if a.is_available)
        self._count_lbl.setText(
            f"{len(apps)} aplicativo(s) — {available} disponível(is)"
        )

    def _on_search(self, text: str):
        text = text.strip().lower()
        if not text:
            self._render_apps(self._all_apps)
            return
        filtered = [
            a for a in self._all_apps
            if text in a.display_name().lower()
            or text in a.installer_filename.lower()
        ]
        self._render_apps(filtered)

    def _on_install(self, app: AppEntry):
        if app.is_available:
            self._launch(app)
        else:
            self._download_and_install(app)

    def _launch(self, app: AppEntry):
        if not self._service.launch_installer(app):
            QMessageBox.warning(
                self,
                "Não foi possível iniciar a instalação",
                f"Não foi possível iniciar a instalação de <b>{app.display_name()}</b>.<br><br>"
                f"Verifique se o instalador está disponível e tente novamente.",
            )

    def _download_and_install(self, app: AppEntry):
        prog = QProgressDialog(
            f"Baixando {app.display_name()}...", "Cancelar", 0, 100, self
        )
        prog.setWindowTitle("Baixando")
        prog.setWindowModality(Qt.WindowModal)
        prog.setMinimumDuration(0)
        prog.setValue(0)

        thread = _DownloadThread(app.installer_filename, app.installer_path)
        self._download_threads.append(thread)

        def on_progress(downloaded: int, total: int):
            if total:
                prog.setValue(int(downloaded / total * 100))
            else:
                prog.setValue(min(prog.value() + 1, 99))

        def on_success():
            prog.setValue(100)
            prog.close()
            self._launch(app)

        def on_failed(msg: str):
            prog.close()
            QMessageBox.warning(
                self,
                "Erro no download",
                f"Não foi possível baixar <b>{app.display_name()}</b>.<br><br>{msg}",
            )

        thread.progress.connect(on_progress)
        thread.success.connect(on_success)
        thread.failed.connect(on_failed)
        prog.canceled.connect(thread.terminate)
        thread.start()
        prog.exec_()
