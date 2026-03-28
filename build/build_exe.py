"""
Script para criar executáveis (.exe) do SAS-Caema
Gera dois executáveis:
- SAS-Caema.exe: Aplicação principal
- SAS-Caema-Startup.exe: Modo startup com feedback visual
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

def build_main_exe(root_dir, app_dir, dist_dir, build_dir):
    """Cria o executável principal"""
    print_colored("\n[ETAPA 1/2] Gerando executável principal...", BLUE)
    
    spec_file = root_dir / "SAS-Caema.spec"
    manifest_file = Path(__file__).parent / "app.manifest"
    icon_file = root_dir / "app" / "assets" / "images" / "icon.ico"
    
    pyinstaller_args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=SAS-Caema",
        "--onefile",
        "--windowed",
        f"--manifest={manifest_file}",  # Força admin permanentemente
        f"--icon={icon_file}",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--specpath={root_dir}",
        
        # Adiciona dados necessários
        f"--add-data={app_dir / 'assets' / 'images'};assets/images",
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
        "--hidden-import=common.theme",
        "--hidden-import=common.widgets",
        
        # Arquivo principal
        str(app_dir / "app.py"),
    ]
    
    try:
        result = subprocess.run(
            pyinstaller_args,
            capture_output=True,
            text=True,
            cwd=root_dir
        )
        
        if result.returncode != 0:
            print_colored("✗ Erro ao gerar executável principal:", RED)
            print(result.stderr)
            return False
        
        # Remove spec file
        if spec_file.exists():
            os.remove(spec_file)
        
        print_colored("✓ Executável principal criado com sucesso!", GREEN)
        return True
        
    except Exception as e:
        print_colored(f"✗ Erro ao executar PyInstaller: {e}", RED)
        return False

def build_startup_exe(root_dir, app_dir, dist_dir, build_dir):
    """Cria o executável de startup com feedback visual"""
    print_colored("\n[ETAPA 2/2] Gerando executável de startup...", BLUE)
    
    spec_file = root_dir / "SAS-Caema-Startup.spec"
    manifest_file = Path(__file__).parent / "startup.manifest"
    icon_file = root_dir / "app" / "assets" / "images" / "icon.ico"
    
    pyinstaller_args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=SAS-Caema-Startup",
        "--onefile",
        "--windowed",
        f"--manifest={manifest_file}",  # Força admin permanentemente
        f"--icon={icon_file}",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--specpath={root_dir}",
        
        # Adiciona dados necessários
        f"--add-data={app_dir / 'assets' / 'images'};assets/images",
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
        "--hidden-import=common.theme",
        "--hidden-import=common.widgets",
        
        # Arquivo de startup
        str(app_dir / "modules" / "checkup" / "startup" / "main.py"),
    ]
    
    try:
        result = subprocess.run(
            pyinstaller_args,
            capture_output=True,
            text=True,
            cwd=root_dir
        )
        
        if result.returncode != 0:
            print_colored("✗ Erro ao gerar executável de startup:", RED)
            print(result.stderr)
            return False
        
        # Remove spec file
        if spec_file.exists():
            os.remove(spec_file)
        
        print_colored("✓ Executável de startup criado com sucesso!", GREEN)
        return True
        
    except Exception as e:
        print_colored(f"✗ Erro ao executar PyInstaller: {e}", RED)
        return False

def build_all():
    """Cria todos os executáveis"""
    print_colored("\n" + "="*70, BLUE)
    print_colored("    SAS-Caema - Build de Executáveis", BLUE)
    print_colored("="*70 + "\n", BLUE)
    
    # Verifica PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # Caminhos (script está em build/, então parent.parent é a raiz)
    root_dir = Path(__file__).parent.parent
    app_dir = root_dir / "app"
    dist_dir = root_dir / "releases"
    build_dir = root_dir / "build_temp"
    
    # Remove builds anteriores
    print_colored("[PREPARAÇÃO] Limpando builds anteriores...", YELLOW)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Cria diretório de releases
    dist_dir.mkdir(exist_ok=True)

    # Build do executável principal
    if not build_main_exe(root_dir, app_dir, dist_dir, build_dir):
        return False
    
    # Build do executável de startup
    if not build_startup_exe(root_dir, app_dir, dist_dir, build_dir):
        return False
    
    # Limpa arquivos temporários
    print_colored("\n[LIMPEZA] Removendo arquivos temporários...", YELLOW)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Verifica executáveis criados
    main_exe = dist_dir / "SAS-Caema.exe"
    startup_exe = dist_dir / "SAS-Caema-Startup.exe"
    
    if main_exe.exists() and startup_exe.exists():
        main_size = main_exe.stat().st_size / (1024 * 1024)
        startup_size = startup_exe.stat().st_size / (1024 * 1024)
        
        print_colored("\n" + "="*70, GREEN)
        print_colored("    ✓ BUILD CONCLUÍDO COM SUCESSO!", GREEN)
        print_colored("="*70, GREEN)
        print_colored(f"\n📦 Executáveis criados em: {dist_dir}\n", GREEN)
        print_colored(f"   • SAS-Caema.exe          ({main_size:.2f} MB)", GREEN)
        print_colored(f"     → Aplicação principal\n", GREEN)
        print_colored(f"   • SAS-Caema-Startup.exe  ({startup_size:.2f} MB)", GREEN)
        print_colored(f"     → Modo startup com feedback visual\n", GREEN)
        print_colored("="*70, GREEN)
        print_colored("\n🚀 Próximo passo: Gerar instalador", BLUE)
        print_colored("   Execute: installer.bat\n", BLUE)
        return True
    else:
        print_colored("✗ Erro: Executáveis não foram criados", RED)
        return False

def main():
    """Função principal"""
    try:
        success = build_all()
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
