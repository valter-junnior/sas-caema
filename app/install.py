"""
Script de instalação e configuração do SAS-Caema
Configura inicialização automática no Windows
"""
import sys
import winreg
from pathlib import Path
import subprocess
import os

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config import STARTUP_REGISTRY_KEY, STARTUP_REGISTRY_VALUE


class StartupManager:
    """Gerencia a inicialização automática no Windows"""
    
    @staticmethod
    def add_to_startup() -> bool:
        """
        Adiciona o SAS-Caema para iniciar com o Windows
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Caminho para o executável Python
            python_exe = sys.executable
            
            # Caminho para o script de checkup
            checkup_script = ROOT_DIR / "modules" / "checkup" / "main.py"
            
            # Comando para executar em modo silencioso
            command = f'"{python_exe}" "{checkup_script}" --silent'
            
            # Abre a chave do registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Define o valor
            winreg.SetValueEx(
                key,
                STARTUP_REGISTRY_VALUE,
                0,
                winreg.REG_SZ,
                command
            )
            
            winreg.CloseKey(key)
            
            print(f"✓ SAS-Caema adicionado à inicialização automática")
            print(f"  Comando: {command}")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao adicionar à inicialização: {e}")
            return False
    
    @staticmethod
    def remove_from_startup() -> bool:
        """
        Remove o SAS-Caema da inicialização automática
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Abre a chave do registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Remove o valor
            winreg.DeleteValue(key, STARTUP_REGISTRY_VALUE)
            winreg.CloseKey(key)
            
            print(f"✓ SAS-Caema removido da inicialização automática")
            return True
            
        except FileNotFoundError:
            print("ℹ SAS-Caema não estava na inicialização automática")
            return True
        except Exception as e:
            print(f"✗ Erro ao remover da inicialização: {e}")
            return False
    
    @staticmethod
    def is_in_startup() -> bool:
        """
        Verifica se o SAS-Caema está configurado para iniciar no Windows
        
        Returns:
            True se está configurado, False caso contrário
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                STARTUP_REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            
            try:
                value, _ = winreg.QueryValueEx(key, STARTUP_REGISTRY_VALUE)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
                
        except Exception:
            return False
    
    @staticmethod
    def install_dependencies() -> bool:
        """
        Instala as dependências do projeto
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            requirements_file = ROOT_DIR / "requirements.txt"
            
            if not requirements_file.exists():
                print("✗ Arquivo requirements.txt não encontrado")
                return False
            
            print("Instalando dependências...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ Dependências instaladas com sucesso")
                return True
            else:
                print(f"✗ Erro ao instalar dependências:\n{result.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao instalar dependências: {e}")
            return False


def main():
    """Função principal do instalador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Instalador SAS-Caema')
    parser.add_argument('--install', action='store_true', 
                       help='Instala e configura o SAS-Caema')
    parser.add_argument('--uninstall', action='store_true',
                       help='Remove o SAS-Caema da inicialização')
    parser.add_argument('--status', action='store_true',
                       help='Verifica o status da instalação')
    parser.add_argument('--dependencies', action='store_true',
                       help='Instala apenas as dependências')
    
    args = parser.parse_args()
    
    manager = StartupManager()
    
    if args.dependencies:
        print("=== Instalando Dependências ===")
        manager.install_dependencies()
        
    elif args.install:
        print("=== Instalando SAS-Caema ===")
        print()
        
        # Instala dependências
        if not manager.install_dependencies():
            print("\n✗ Falha na instalação")
            sys.exit(1)
        
        print()
        
        # Adiciona à inicialização
        if manager.add_to_startup():
            print()
            print("✓ Instalação concluída com sucesso!")
            print()
            print("O SAS-Caema agora irá iniciar automaticamente com o Windows")
            print("e executar verificações de rotina do sistema.")
        else:
            print("\n✗ Falha ao configurar inicialização automática")
            sys.exit(1)
    
    elif args.uninstall:
        print("=== Desinstalando SAS-Caema ===")
        if manager.remove_from_startup():
            print("\n✓ Desinstalação concluída")
        else:
            print("\n✗ Falha na desinstalação")
            sys.exit(1)
    
    elif args.status:
        print("=== Status do SAS-Caema ===")
        if manager.is_in_startup():
            print("✓ SAS-Caema está configurado para iniciar com o Windows")
        else:
            print("✗ SAS-Caema NÃO está configurado para iniciar com o Windows")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
