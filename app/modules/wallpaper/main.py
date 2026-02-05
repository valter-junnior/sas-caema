"""
Módulo principal do Wallpaper - orquestra a geração e configuração do papel de parede
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from modules.wallpaper.services.system_info import SystemInfoCollector
from modules.wallpaper.services.image_generator import ImageGenerator
from modules.wallpaper.services.wallpaper_setter import WallpaperSetter
from modules.wallpaper import config


class WallpaperModule:
    """Classe principal do módulo de papel de parede"""
    
    def __init__(self):
        """Inicializa o módulo com as configurações"""
        self.system_info = SystemInfoCollector()
        self.image_generator = ImageGenerator(
            base_image_path=config.BACKGROUND_IMAGE,
            text_color=config.TEXT_COLOR,
            text_size=config.TEXT_SIZE,
            padding=config.PADDING,
            font_name=config.FONT
        )
        self.wallpaper_setter = WallpaperSetter()
        
    def execute(self) -> bool:
        """
        Executa o processo completo de criação e configuração do papel de parede
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            print("=== Módulo de Papel de Parede ===")
            print("1. Coletando informações do sistema...")
            
            # Coleta informações do sistema
            info = self.system_info.get_all_info()
            info_text = self.system_info.format_info_text(info)
            
            print(f"   Usuário: {info['username']}")
            print(f"   Computador: {info['hostname']}")
            print(f"   IP: {info['ip_address']}")
            print(f"   MAC: {info['mac_address']}")
            
            print("\n2. Gerando imagem do papel de parede...")
            
            # Gera a imagem com as informações
            success = self.image_generator.generate_wallpaper(
                info_text=info_text,
                output_path=config.OUTPUT_PATH,
                position=config.TEXT_POSITION
            )
            
            if not success:
                print("   Erro ao gerar imagem!")
                return False
            
            print("   Imagem gerada com sucesso!")
            
            print("\n3. Configurando papel de parede no Windows...")
            
            # Define como papel de parede
            success = self.wallpaper_setter.set_wallpaper(
                image_path=config.OUTPUT_PATH,
                style=config.WALLPAPER_STYLE
            )
            
            if success:
                print("   Papel de parede configurado com sucesso!")
                print("\n✓ Módulo executado com sucesso!")
                return True
            else:
                print("   Erro ao configurar papel de parede!")
                return False
                
        except Exception as e:
            print(f"\n✗ Erro ao executar módulo: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def check(self) -> dict:
        """
        Verifica se o papel de parede está configurado corretamente
        
        Returns:
            Dicionário com status da verificação
        """
        try:
            current_wallpaper = self.wallpaper_setter.get_current_wallpaper()
            expected_wallpaper = str(config.OUTPUT_PATH.absolute())
            
            # Se não há wallpaper configurado, precisa atualizar
            if not current_wallpaper:
                return {
                    'module': 'wallpaper',
                    'status': 'needs_update',
                    'current': 'None',
                    'expected': expected_wallpaper,
                    'message': 'Papel de parede precisa ser atualizado'
                }
            
            # Normaliza os paths para comparação
            # Remove espaços, converte para lowercase para comparação case-insensitive
            # e resolve paths completos
            try:
                current_normalized = Path(current_wallpaper).resolve()
                expected_normalized = Path(expected_wallpaper).resolve()
                
                # Compara os paths normalizados
                # Usa os.path.samefile para lidar com links simbólicos e diferentes formatos
                import os
                is_configured = os.path.samefile(current_normalized, expected_normalized)
                
            except (OSError, ValueError):
                # Se samefile falhar (arquivo não existe), compara strings
                current_normalized = Path(current_wallpaper).resolve()
                expected_normalized = Path(expected_wallpaper).resolve()
                is_configured = (current_normalized == expected_normalized)
            
            return {
                'module': 'wallpaper',
                'status': 'ok' if is_configured else 'needs_update',
                'current': str(current_normalized),
                'expected': str(expected_normalized),
                'message': 'Papel de parede configurado' if is_configured else 'Papel de parede precisa ser atualizado'
            }
            
        except Exception as e:
            return {
                'module': 'wallpaper',
                'status': 'error',
                'message': f'Erro ao verificar: {str(e)}'
            }


def main():
    """Função principal para execução standalone"""
    module = WallpaperModule()
    
    # Verifica o status atual
    print("Verificando status atual...")
    status = module.check()
    print(f"Status: {status['status']}")
    print(f"Mensagem: {status['message']}")
    print()
    
    # Executa se necessário
    if status['status'] != 'ok':
        success = module.execute()
        sys.exit(0 if success else 1)
    else:
        print("Papel de parede já está configurado corretamente!")
        sys.exit(0)


if __name__ == "__main__":
    main()
