"""
Serviço para configurar o papel de parede no Windows
"""
import ctypes
from pathlib import Path
import winreg
import os
from typing import Optional


class WallpaperSetter:
    """Configura o papel de parede do Windows"""
    
    # Constantes do Windows para SPI_SETDESKWALLPAPER
    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02
    
    @staticmethod
    def set_wallpaper(image_path: Path, style: str = "fill") -> bool:
        """
        Define o papel de parede do Windows
        
        Args:
            image_path: Caminho completo para a imagem
            style: Estilo de exibição ('fill', 'fit', 'stretch', 'tile', 'center', 'span')
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Converte para caminho absoluto
            abs_path = str(image_path.absolute())
            
            # Verifica se arquivo existe
            if not os.path.exists(abs_path):
                print(f"Erro: Arquivo não encontrado: {abs_path}")
                return False
            
            # Define o estilo no registro
            WallpaperSetter._set_wallpaper_style(style)
            
            # Define o papel de parede usando ctypes
            result = ctypes.windll.user32.SystemParametersInfoW(
                WallpaperSetter.SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                WallpaperSetter.SPIF_UPDATEINIFILE | WallpaperSetter.SPIF_SENDWININICHANGE
            )
            
            if result:
                print(f"Papel de parede definido com sucesso: {abs_path}")
                return True
            else:
                print("Erro ao definir papel de parede")
                return False
                
        except Exception as e:
            print(f"Erro ao configurar papel de parede: {e}")
            return False
    
    @staticmethod
    def _set_wallpaper_style(style: str) -> None:
        """
        Define o estilo de exibição do papel de parede no registro do Windows
        
        Args:
            style: Estilo ('fill', 'fit', 'stretch', 'tile', 'center', 'span')
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Mapeamento de estilos
            styles = {
                'fill': ('10', '0'),      # Preencher
                'fit': ('6', '0'),        # Ajustar
                'stretch': ('2', '0'),    # Estender
                'tile': ('0', '1'),       # Lado a lado
                'center': ('0', '0'),     # Centralizar
                'span': ('22', '0'),      # Expandir
            }
            
            if style.lower() not in styles:
                style = 'fill'  # Padrão
            
            wallpaper_style, tile_wallpaper = styles[style.lower()]
            
            # Define os valores no registro
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, wallpaper_style)
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, tile_wallpaper)
            
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"Erro ao definir estilo do papel de parede: {e}")
    
    @staticmethod
    def get_current_wallpaper() -> Optional[str]:
        """
        Obtém o caminho do papel de parede atual
        
        Returns:
            Caminho do papel de parede ou None se erro
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                winreg.KEY_READ
            )
            
            wallpaper, _ = winreg.QueryValueEx(key, "Wallpaper")
            winreg.CloseKey(key)
            
            return wallpaper if wallpaper else None
            
        except Exception as e:
            print(f"Erro ao obter papel de parede atual: {e}")
            return None


if __name__ == "__main__":
    # Teste do módulo
    import sys
    
    if len(sys.argv) > 1:
        test_image = Path(sys.argv[1])
        if test_image.exists():
            setter = WallpaperSetter()
            current = setter.get_current_wallpaper()
            print(f"Papel de parede atual: {current}")
            
            if setter.set_wallpaper(test_image, style="fill"):
                print("Teste concluído com sucesso!")
        else:
            print(f"Arquivo não encontrado: {test_image}")
    else:
        print("Uso: python wallpaper_setter.py <caminho_da_imagem>")
