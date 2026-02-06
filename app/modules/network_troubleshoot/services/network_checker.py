"""
Serviço de verificação de conectividade de rede
"""
import subprocess
import platform
from pathlib import Path
import sys
import socket

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.network_troubleshoot import config


class NetworkChecker:
    """Serviço responsável por testar a conectividade de rede"""
    
    def __init__(self):
        """Inicializa o serviço de verificação de rede"""
        self.logger = logger_service.get_logger('NetworkChecker')
    
    def ping_host(self, host: str, timeout: int = 3) -> bool:
        """
        Executa ping para um host específico
        
        Args:
            host: Endereço IP ou hostname para ping
            timeout: Timeout em segundos
            
        Returns:
            True se ping foi bem-sucedido, False caso contrário
        """
        try:
            # Determina o comando ping baseado no sistema operacional
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            
            # Converte timeout para milissegundos no Windows
            timeout_value = str(timeout * 1000) if platform.system().lower() == 'windows' else str(timeout)
            
            # Executa o comando ping
            command = ['ping', param, '1', timeout_param, timeout_value, host]
            
            self.logger.debug(f"Executando ping para {host}...")
            
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout + 1
            )
            
            success = result.returncode == 0
            self.logger.debug(f"Ping para {host}: {'OK' if success else 'FALHOU'}")
            
            return success
            
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Timeout ao fazer ping para {host}")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao fazer ping para {host}: {e}")
            return False
    
    def check_internet_connectivity(self) -> bool:
        """
        Testa conexão realizando ping para múltiplos servidores
        
        Returns:
            True se pelo menos um servidor respondeu, False caso contrário
        """
        self.logger.info("Verificando conectividade de internet...")
        
        hosts = config.NETWORK_TEST_HOSTS
        timeout = config.PING_TIMEOUT
        
        successful_pings = 0
        
        for host in hosts:
            if self.ping_host(host, timeout):
                successful_pings += 1
        
        is_connected = successful_pings > 0
        
        self.logger.info(
            f"Conectividade: {'OK' if is_connected else 'FALHOU'} "
            f"({successful_pings}/{len(hosts)} hosts responderam)"
        )
        
        return is_connected
    
    def get_local_ip(self) -> str:
        """
        Obtém o endereço IP local da máquina
        
        Returns:
            Endereço IP local ou 'Desconhecido' se não conseguir obter
        """
        try:
            # Cria um socket para obter o IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            self.logger.error(f"Erro ao obter IP local: {e}")
            return "Desconhecido"
    
    def get_network_adapter_status(self) -> dict:
        """
        Verifica status dos adaptadores de rede (Windows)
        
        Returns:
            Dicionário com informações dos adaptadores
        """
        try:
            if platform.system().lower() != 'windows':
                return {'status': 'not_supported', 'adapters': []}
            
            # Executa ipconfig para obter informações dos adaptadores
            result = subprocess.run(
                ['ipconfig', '/all'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                return {
                    'status': 'ok',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'output': ''
                }
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar adaptadores: {e}")
            return {'status': 'error', 'output': ''}
    
    def get_diagnostic_info(self) -> dict:
        """
        Coleta informações de diagnóstico de rede
        
        Returns:
            Dicionário com informações de diagnóstico
        """
        self.logger.info("Coletando informações de diagnóstico...")
        
        info = {
            'timestamp': '',
            'local_ip': self.get_local_ip(),
            'internet_connectivity': self.check_internet_connectivity(),
            'ping_results': {}
        }
        
        # Testa ping para cada host individualmente
        for host in config.NETWORK_TEST_HOSTS:
            info['ping_results'][host] = self.ping_host(host, config.PING_TIMEOUT)
        
        # Obtém informações de adaptadores (Windows)
        adapter_info = self.get_network_adapter_status()
        info['adapter_status'] = adapter_info.get('status', 'unknown')
        
        self.logger.info("Informações de diagnóstico coletadas")
        
        return info
