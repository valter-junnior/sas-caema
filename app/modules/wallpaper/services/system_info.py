"""
Serviço para coletar informações do sistema Windows
"""
import socket
import platform
import psutil
import os
from typing import Dict, Optional


class SystemInfoCollector:
    """Coleta informações relevantes do sistema para o suporte"""
    
    @staticmethod
    def get_username() -> str:
        """Retorna o nome do usuário atual"""
        try:
            return os.getlogin()
        except Exception:
            return os.environ.get('USERNAME', 'Unknown')
    
    @staticmethod
    def get_hostname() -> str:
        """Retorna o nome do computador"""
        try:
            return socket.gethostname()
        except Exception:
            return "Unknown"
    
    @staticmethod
    def get_ip_address() -> str:
        """Retorna o endereço IP principal (IPv4)"""
        try:
            # Conecta a um servidor externo para descobrir o IP local usado
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "N/A"
    
    @staticmethod
    def get_mac_address() -> str:
        """Retorna o endereço MAC da interface de rede principal"""
        try:
            # Obtém informações de todas as interfaces
            interfaces = psutil.net_if_addrs()
            
            # Prioriza interfaces Ethernet e Wi-Fi
            priority_names = ['Ethernet', 'Wi-Fi', 'eth0', 'wlan0']
            
            for name in priority_names:
                if name in interfaces:
                    for addr in interfaces[name]:
                        if addr.family == psutil.AF_LINK:
                            mac = addr.address.replace('-', ':').upper()
                            if mac != '00:00:00:00:00:00':
                                return mac
            
            # Se não encontrou nas prioritárias, pega a primeira disponível
            for interface_name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:
                        mac = addr.address.replace('-', ':').upper()
                        if mac != '00:00:00:00:00:00':
                            return mac
            
            return "N/A"
        except Exception as e:
            return "N/A"
    
    @staticmethod
    def get_domain() -> str:
        """Retorna o domínio do computador se estiver em um"""
        try:
            domain = os.environ.get('USERDOMAIN', '')
            hostname = socket.gethostname()
            
            # Se o domínio é diferente do hostname, está em um domínio
            if domain and domain.upper() != hostname.upper():
                return domain
            return "Workgroup"
        except Exception:
            return "N/A"
    
    @staticmethod
    def get_os_version() -> str:
        """Retorna a versão do Windows"""
        try:
            return f"{platform.system()} {platform.release()}"
        except Exception:
            return "Unknown"
    
    @staticmethod
    def get_all_info() -> Dict[str, str]:
        """Retorna todas as informações do sistema em um dicionário"""
        return {
            'username': SystemInfoCollector.get_username(),
            'hostname': SystemInfoCollector.get_hostname(),
            'ip_address': SystemInfoCollector.get_ip_address(),
            'mac_address': SystemInfoCollector.get_mac_address(),
            'domain': SystemInfoCollector.get_domain(),
            'os_version': SystemInfoCollector.get_os_version(),
        }
    
    @staticmethod
    def format_info_text(info: Optional[Dict[str, str]] = None) -> str:
        """Formata as informações em texto para exibição"""
        if info is None:
            info = SystemInfoCollector.get_all_info()
        
        lines = [
            f"Usuário: {info['username']}",
            f"Computador: {info['hostname']}",
            f"IP: {info['ip_address']}",
            f"MAC: {info['mac_address']}",
            f"Domínio: {info['domain']}",
            f"Sistema: {info['os_version']}",
        ]
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Teste do módulo
    collector = SystemInfoCollector()
    info = collector.get_all_info()
    print("Informações do Sistema:")
    print("=" * 50)
    print(collector.format_info_text(info))
