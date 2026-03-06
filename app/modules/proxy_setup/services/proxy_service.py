"""
Serviço de configuração de proxy no Windows
"""
import subprocess
import sys
import winreg
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.proxy_setup import config

_IE_SETTINGS_KEY = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"


class ProxyService:
    """Responsável por ler, aplicar e remover configurações de proxy no Windows"""

    def __init__(self):
        self.logger = logger_service.get_logger('ProxyService')

    # ------------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------------

    def get_current_proxy(self) -> str:
        """
        Lê o servidor de proxy configurado atualmente nas configurações de internet do Windows.

        Returns:
            String no formato 'host:porta', ou string vazia se não houver proxy.
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _IE_SETTINGS_KEY)
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if not enabled:
                return ""
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
            winreg.CloseKey(key)
            return server or ""
        except FileNotFoundError:
            return ""
        except Exception as e:
            self.logger.error(f"Erro ao ler proxy atual: {e}")
            return ""

    def is_proxy_enabled(self) -> bool:
        """Retorna True se o proxy está habilitado nas configurações de internet."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _IE_SETTINGS_KEY)
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            winreg.CloseKey(key)
            return bool(enabled)
        except Exception:
            return False

    def is_correct_proxy_set(self) -> bool:
        """Retorna True se o proxy configurado é exatamente o proxy esperado."""
        return self.is_proxy_enabled() and self.get_current_proxy() == config.PROXY_SERVER

    # ------------------------------------------------------------------
    # Aplicação
    # ------------------------------------------------------------------

    def apply_proxy(self) -> bool:
        """
        Configura o proxy nas Configurações de Internet do Windows (registro HKCU)
        e propaga para o proxy do sistema via netsh winhttp.

        Returns:
            True se aplicado com sucesso, False caso contrário.
        """
        registry_ok = self._apply_registry_proxy()
        netsh_ok = self._apply_netsh_proxy()

        if registry_ok:
            self.logger.info(f"Proxy configurado com sucesso: {config.PROXY_SERVER}")
        else:
            self.logger.error("Falha ao configurar proxy no registro")

        return registry_ok

    def _apply_registry_proxy(self) -> bool:
        """Grava as chaves de proxy nas configurações de internet do usuário atual."""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                _IE_SETTINGS_KEY,
                0,
                winreg.KEY_SET_VALUE,
            )
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, config.PROXY_SERVER)
            winreg.CloseKey(key)
            self.logger.info(f"Registro atualizado: ProxyServer={config.PROXY_SERVER}, ProxyEnable=1")
            return True
        except PermissionError:
            self.logger.error("Sem permissão para gravar no registro")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao gravar proxy no registro: {e}")
            return False

    def _apply_netsh_proxy(self) -> bool:
        """Configura o proxy de sistema via netsh winhttp (usado por apps Win32)."""
        try:
            result = subprocess.run(
                [
                    "netsh", "winhttp", "set", "proxy",
                    config.PROXY_SERVER,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15,
            )
            if result.returncode == 0:
                self.logger.info("Proxy netsh winhttp configurado com sucesso")
            else:
                self.logger.warning(
                    f"netsh retornou código {result.returncode}: {result.stderr.decode(errors='ignore')}"
                )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            self.logger.warning("Timeout ao configurar proxy via netsh")
            return False
        except Exception as e:
            self.logger.warning(f"Erro ao configurar proxy via netsh: {e}")
            return False
