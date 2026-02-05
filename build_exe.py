"""
Script para criar executável (.exe) do SAS-Caema
Usa PyInstaller para empacotar a aplicação
"""
import subprocess
import sys
import os
from pathlib import Path
import shutil

# Cores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

def print_colored(text, color):
    """Imprime texto colorido no terminal"""
    print(f"{color}{text}{RESET}")

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print_colored("PyInstaller não encontrado. Instalando...", YELLOW)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print_colored("✓ PyInstaller instalado com sucesso!", GREEN)
        return True
    except:
        print_colored("✗ Erro ao instalar PyInstaller", RED)
        return False

def build_exe():
    """Cria o executável"""
    print_colored("\n" + "="*60, BLUE)
    print_colored("    SAS-Caema - Build de Executável", BLUE)
    print_colored("="*60 + "\n", BLUE)
    
    # Verifica PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # Caminhos
    root_dir = Path(__file__).parent
    app_dir = root_dir / "app"
    dist_dir = root_dir / "releases"
    build_dir = root_dir / "build"
    spec_file = root_dir / "SAS-Caema.spec"
    
    # Remove builds anteriores
    print_colored("[1/4] Limpando builds anteriores...", YELLOW)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if spec_file.exists():
        os.remove(spec_file)
    
    # Prepara comando PyInstaller
    print_colored("[2/4] Configurando PyInstaller...", YELLOW)
    
    pyinstaller_args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=SAS-Caema",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--specpath={root_dir}",
        
        # Adiciona dados necessários
        f"--add-data={app_dir / 'assets'};assets",
        f"--add-data={app_dir / 'modules'};modules",
        f"--add-data={app_dir / 'common'};common",
        f"--add-data={app_dir / 'config.py'};.",
        f"--add-data={app_dir / 'version.py'};.",
        
        # Imports ocultos necessários
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageDraw",
        "--hidden-import=PIL.ImageFont",
        "--hidden-import=psutil",
        "--hidden-import=winotify",
        
        # Arquivo principal
        str(app_dir / "app.py"),
    ]
    
    # Executa PyInstaller
    print_colored("[3/4] Gerando executável...", YELLOW)
    print_colored("      Aguarde, isso pode levar alguns minutos...", YELLOW)
    
    try:
        result = subprocess.run(
            pyinstaller_args,
            capture_output=True,
            text=True,
            cwd=root_dir
        )
        
        if result.returncode != 0:
            print_colored("✗ Erro ao gerar executável:", RED)
            print(result.stderr)
            return False
        
    except Exception as e:
        print_colored(f"✗ Erro ao executar PyInstaller: {e}", RED)
        return False
    
    # Limpa arquivos temporários
    print_colored("[4/4] Limpando arquivos temporários...", YELLOW)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if spec_file.exists():
        os.remove(spec_file)
    
    # Verifica se executável foi criado
    exe_path = dist_dir / "SAS-Caema.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print_colored("\n" + "="*60, GREEN)
        print_colored("    ✓ BUILD CONCLUÍDO COM SUCESSO!", GREEN)
        print_colored("="*60, GREEN)
        print_colored(f"\nExecutável criado: {exe_path}", GREEN)
        print_colored(f"Tamanho: {size_mb:.2f} MB", GREEN)
        print_colored("\nVocê pode distribuir este executável!", GREEN)
        print_colored("Ele não precisa de Python instalado para funcionar.\n", GREEN)
        return True
    else:
        print_colored("✗ Executável não foi criado", RED)
        return False

def main():
    """Função principal"""
    try:
        success = build_exe()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_colored("\n\n✗ Build cancelado pelo usuário", RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n✗ Erro inesperado: {e}", RED)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
