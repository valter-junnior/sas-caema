"""
Configurações do módulo de verificação de rede
"""
from pathlib import Path

# Diretórios
ASSETS_DIR = Path(__file__).parent / "assets"

# Configurações de teste de rede
NETWORK_TEST_HOSTS = [
    "8.8.8.8",        # Google DNS
    "1.1.1.1",        # Cloudflare DNS
]
PING_TIMEOUT = 3      # segundos
PING_COUNT = 4        # número de pings

# Configurações de UI
STEP_COUNT = 3
RESTART_TIMER_SECONDS = 120  # 2 minutos

# Textos das etapas
STEP_TITLES = {
    1: "Verificar Cabos e Equipamento",
    2: "Reiniciar Modem/Roteador",
    3: "Testar Conexão",
}

STEP_INSTRUCTIONS = {
    1: "Confirme os itens físicos antes de continuar.",
    2: "Reinicie o modem/roteador para restabelecer a conexão.",
    3: "Agora vamos verificar se a internet foi restabelecida.",
}

# Imagens das etapas
STEP_IMAGES = {
    1: ASSETS_DIR / "step1_placeholder.png",
    2: ASSETS_DIR / "step2_placeholder.png",
    3: ASSETS_DIR / "step3_placeholder.png",
}
