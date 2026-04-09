"""
Serviço de catálogo de aplicativos — lê o CSV e extrai metadados dos executáveis.
"""
import csv
import ctypes
import ctypes.wintypes
import sys
from dataclasses import dataclass, field
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import APPS_DIR
from common.services.logger import logger_service

CATALOG_PATH = APPS_DIR / "catalog.csv"
INSTALLERS_DIR = APPS_DIR


def _read_exe_metadata(path: Path) -> dict:
    """Extrai ProductName, FileVersion e CompanyName do EXE usando ctypes."""
    result = {'name': '', 'version': '', 'company': ''}
    try:
        ver = ctypes.windll.version
        filepath = str(path)
        size = ver.GetFileVersionInfoSizeW(filepath, None)
        if size == 0:
            return result
        buf = ctypes.create_string_buffer(size)
        if not ver.GetFileVersionInfoW(filepath, 0, size, buf):
            return result

        lp_buffer = ctypes.c_void_p()
        n = ctypes.c_uint()

        # Obtém idioma/codepage disponível
        ver.VerQueryValueW(buf, r'\VarFileInfo\Translation',
                           ctypes.byref(lp_buffer), ctypes.byref(n))
        if n.value == 0:
            return result

        langs = ctypes.cast(lp_buffer, ctypes.POINTER(ctypes.c_ushort))
        lang_id   = langs[0]
        codepage  = langs[1]
        prefix = f'\\StringFileInfo\\{lang_id:04X}{codepage:04X}\\'

        for key, dest in (
            ('ProductName',  'name'),
            ('FileVersion',  'version'),
            ('CompanyName',  'company'),
        ):
            lp = ctypes.c_void_p()
            nn = ctypes.c_uint()
            if ver.VerQueryValueW(buf, prefix + key, ctypes.byref(lp), ctypes.byref(nn)):
                val = ctypes.cast(lp, ctypes.c_wchar_p).value or ''
                result[dest] = val.strip().split('\x00')[0]

        # Limpa versão (remove sufixos como " (64-bit)")
        result['version'] = result['version'].split(' ')[0]
    except Exception:
        pass
    return result


@dataclass
class AppEntry:
    id: str
    installer_filename: str
    name: str = ''
    version: str = ''
    company: str = ''

    @property
    def installer_path(self) -> Path:
        return INSTALLERS_DIR / self.installer_filename

    @property
    def is_available(self) -> bool:
        return self.installer_path.exists()

    def display_name(self) -> str:
        return self.name or self.id.replace('_', ' ').title()

    def display_version(self) -> str:
        return f'v{self.version}' if self.version else ''

    def display_company(self) -> str:
        return self.company


class CatalogService:
    """Lê o catálogo (CSV com id + installer_filename)."""

    def __init__(self):
        self.logger = logger_service.get_logger('CatalogService')
        self._apps: list[AppEntry] = []
        self._load()

    def _load(self):
        if not CATALOG_PATH.exists():
            self.logger.warning(f"Catálogo não encontrado: {CATALOG_PATH}")
            return
        try:
            with open(CATALOG_PATH, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    installer_filename = (row.get('installer_filename') or '').strip()
                    entry = AppEntry(
                        id=(row.get('id') or '').strip(),
                        installer_filename=installer_filename,
                    )
                    if not entry.id or not entry.installer_filename:
                        continue
                    if entry.is_available:
                        meta = _read_exe_metadata(entry.installer_path)
                        entry.name    = meta['name']
                        entry.version = meta['version']
                        entry.company = meta['company']
                    self._apps.append(entry)
            self.logger.info(f"{len(self._apps)} apps carregados do catálogo")
        except Exception as e:
            self.logger.error(f"Erro ao carregar catálogo: {e}")

    def get_all(self) -> list[AppEntry]:
        return list(self._apps)

    def reload(self):
        """Relê o catálogo do disco (útil após download do catalog.csv)."""
        self._apps = []
        self._load()

    def launch_installer(self, app: AppEntry) -> bool:
        """Abre o instalador com elevação UAC via ShellExecute (runas)."""
        if not app.is_available:
            self.logger.warning(f"Instalador não encontrado: {app.installer_path}")
            return False
        try:
            import ctypes
            # ShellExecute com runas dispara o prompt de UAC automaticamente
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", str(app.installer_path), None, None, 1
            )
            # ShellExecute retorna > 32 em caso de sucesso
            if ret <= 32:
                raise OSError(f"ShellExecute retornou {ret}")
            self.logger.info(f"Instalador iniciado: {app.display_name()} ({app.installer_filename})")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao iniciar instalador de {app.display_name()}: {e}")
            return False
