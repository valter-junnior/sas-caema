"""
Aplicação principal do SAS-Caema
Interface gráfica com PyQt5
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from common.views.main_window import MainWindow


def main():
    """Função principal"""
    # Cria aplicação Qt
    app = QApplication(sys.argv)
    
    # Define estilo da aplicação
    app.setStyle('Fusion')
    
    # Cria e mostra janela principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
