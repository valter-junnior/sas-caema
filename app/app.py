"""
Aplicação principal do SAS-Caema.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Styles, Fonts
from common.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont(Fonts.FAMILY, 10))
    app.setStyleSheet(Styles.global_app())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
