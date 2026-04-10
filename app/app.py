"""
Aplicação principal do SAS-Caema.
"""
import sys
import threading
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Styles, Fonts
from common.views.main_window import MainWindow

_ICON_PATH = ROOT_DIR / "assets" / "images" / "icon.ico"


def _fetch_catalog_background():
    """Baixa o catalog.csv remoto em segundo plano ao iniciar."""
    try:
        from common.services.assets_service import download_catalog
        from config import APPS_DIR
        download_catalog(APPS_DIR / "catalog.csv")
    except Exception:
        pass  # sem internet ou erro: usa cache local


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont(Fonts.FAMILY, 10))
    app.setStyleSheet(Styles.global_app())

    if _ICON_PATH.exists():
        from PyQt5.QtGui import QIcon
        app.setWindowIcon(QIcon(str(_ICON_PATH)))

    window = MainWindow()
    window.show()

    # Atualiza catálogo em background logo ao iniciar
    threading.Thread(target=_fetch_catalog_background, daemon=True).start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
