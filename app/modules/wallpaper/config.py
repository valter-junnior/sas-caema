"""
Configurações do módulo de papel de parede
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para imports
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import WALLPAPER_CONFIG

# Exporta configurações
TEXT_COLOR = WALLPAPER_CONFIG["text_color"]
TEXT_SIZE = WALLPAPER_CONFIG["text_size"]
TEXT_POSITION = WALLPAPER_CONFIG["text_position"]
FONT = WALLPAPER_CONFIG["font"]
BACKGROUND_IMAGE = WALLPAPER_CONFIG["background_image"]
OUTPUT_PATH = WALLPAPER_CONFIG["output_path"]
PADDING = WALLPAPER_CONFIG["padding"]

# Estilo de exibição do papel de parede
WALLPAPER_STYLE = "fill"  # fill, fit, stretch, tile, center, span
