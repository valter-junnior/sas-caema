"""
Script para criar imagem de papel de parede padrão
"""
from PIL import Image, ImageDraw
from pathlib import Path


def create_default_wallpaper():
    """Cria uma imagem padrão caso o usuário não forneça uma"""
    
    # Dimensões Full HD
    width, height = 1920, 1080
    
    # Cria imagem com gradiente
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Cria gradiente azul
    for y in range(height):
        # Gradiente de azul escuro para azul médio
        r = int(10 + (y / height) * 20)
        g = int(30 + (y / height) * 60)
        b = int(60 + (y / height) * 100)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Adiciona marca d'água no centro
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text = "SAS - Caema"
    # Centraliza o texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Desenha texto semi-transparente (adiciona sombra)
    shadow_color = (0, 0, 0, 100)
    for offset_x in range(-2, 3):
        for offset_y in range(-2, 3):
            draw.text((x + offset_x, y + offset_y), text, font=font, fill=(0, 0, 0))
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # Salva
    output_path = Path(__file__).parent / "assets" / "wallpaper_base.png"
    output_path.parent.mkdir(exist_ok=True)
    image.save(output_path, quality=95)
    
    print(f"✓ Imagem padrão criada: {output_path}")
    print(f"  Dimensões: {width}x{height}")
    print("\nVocê pode substituir esta imagem pela sua própria!")


if __name__ == "__main__":
    create_default_wallpaper()
