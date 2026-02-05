"""
Serviço para gerar papel de parede personalizado com informações do sistema
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Tuple, Optional
import os


class ImageGenerator:
    """Gera imagem de papel de parede com informações sobrepostas"""
    
    def __init__(self, base_image_path: Path, text_color: str = "#FFFFFF", 
                 text_size: int = 18, padding: int = 20, font_name: str = "Arial"):
        """
        Inicializa o gerador de imagens
        
        Args:
            base_image_path: Caminho para a imagem base
            text_color: Cor do texto em formato hex (#RRGGBB)
            text_size: Tamanho da fonte
            padding: Espaçamento das bordas em pixels
            font_name: Nome da fonte a usar
        """
        self.base_image_path = Path(base_image_path)
        self.text_color = text_color
        self.text_size = text_size
        self.padding = padding
        self.font_name = font_name
        
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Converte cor hexadecimal para RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _get_font(self) -> ImageFont.FreeTypeFont:
        """Obtém a fonte apropriada"""
        try:
            # Tenta usar fonte do sistema Windows
            font_paths = [
                f"C:/Windows/Fonts/{self.font_name}.ttf",
                f"C:/Windows/Fonts/{self.font_name}bd.ttf",  # Bold
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, self.text_size)
            
            # Se não encontrou, usa fonte padrão
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()
    
    def _add_text_with_shadow(self, draw: ImageDraw.ImageDraw, 
                              position: Tuple[int, int], 
                              text: str, 
                              font: ImageFont.FreeTypeFont,
                              text_color: Tuple[int, int, int]):
        """Adiciona texto com sombra para melhor legibilidade"""
        x, y = position
        
        # Desenha sombra (deslocada 1-2 pixels)
        shadow_color = (0, 0, 0)
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), text, 
                             font=font, fill=shadow_color)
        
        # Desenha texto principal
        draw.text(position, text, font=font, fill=text_color)
    
    def generate_wallpaper(self, info_text: str, output_path: Path,
                          position: str = "top-right") -> bool:
        """
        Gera o papel de parede com as informações
        
        Args:
            info_text: Texto com informações a adicionar
            output_path: Caminho onde salvar a imagem gerada
            position: Posição do texto (top-right, top-left, bottom-right, bottom-left)
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Verifica se imagem base existe
            if not self.base_image_path.exists():
                print(f"Erro: Imagem base não encontrada em {self.base_image_path}")
                return False
            
            # Abre imagem base
            image = Image.open(self.base_image_path)
            width, height = image.size
            
            # Cria objeto de desenho
            draw = ImageDraw.Draw(image)
            
            # Obtém fonte
            font = self._get_font()
            
            # Converte cor
            rgb_color = self._hex_to_rgb(self.text_color)
            
            # Divide texto em linhas
            lines = info_text.strip().split('\n')
            
            # Calcula dimensões do texto
            line_height = self.text_size + 5
            
            # Calcula posição baseada na escolha
            if position == "top-right":
                x = width - self.padding
                y = self.padding
                anchor = "rt"  # right-top
                
                # Desenha cada linha
                for i, line in enumerate(lines):
                    line_y = y + (i * line_height)
                    # Calcula posição x baseada no comprimento da linha
                    bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = bbox[2] - bbox[0]
                    line_x = x - line_width
                    self._add_text_with_shadow(draw, (line_x, line_y), 
                                               line, font, rgb_color)
                    
            elif position == "top-left":
                x = self.padding
                y = self.padding
                for i, line in enumerate(lines):
                    line_y = y + (i * line_height)
                    self._add_text_with_shadow(draw, (x, line_y), 
                                               line, font, rgb_color)
                    
            elif position == "bottom-right":
                x = width - self.padding
                y = height - self.padding - (len(lines) * line_height)
                for i, line in enumerate(lines):
                    line_y = y + (i * line_height)
                    bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = bbox[2] - bbox[0]
                    line_x = x - line_width
                    self._add_text_with_shadow(draw, (line_x, line_y), 
                                               line, font, rgb_color)
                    
            elif position == "bottom-left":
                x = self.padding
                y = height - self.padding - (len(lines) * line_height)
                for i, line in enumerate(lines):
                    line_y = y + (i * line_height)
                    self._add_text_with_shadow(draw, (x, line_y), 
                                               line, font, rgb_color)
            
            # Salva imagem
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, quality=95)
            print(f"Papel de parede gerado com sucesso: {output_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao gerar papel de parede: {e}")
            return False


if __name__ == "__main__":
    # Teste do módulo
    from pathlib import Path
    
    # Cria imagem de teste se não existir
    base_path = Path("../../../assets/wallpaper_base.png")
    if not base_path.exists():
        print("Criando imagem de teste...")
        test_img = Image.new('RGB', (1920, 1080), color=(30, 30, 30))
        base_path.parent.mkdir(parents=True, exist_ok=True)
        test_img.save(base_path)
    
    generator = ImageGenerator(
        base_image_path=base_path,
        text_color="#FFFFFF",
        text_size=18,
        padding=20
    )
    
    test_text = """Usuário: João Silva
Computador: DESKTOP-ABC123
IP: 192.168.1.100
MAC: AA:BB:CC:DD:EE:FF
Domínio: CAEMA
Sistema: Windows 11"""
    
    output = Path("../../../assets/wallpaper_test.png")
    generator.generate_wallpaper(test_text, output, position="top-right")
