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
STEP_COUNT = 5
RESTART_TIMER_SECONDS = 120  # 2 minutos

# Textos das etapas
STEP_TITLES = {
    1: "Verificar Conexão do Cabo de Rede",
    2: "Verificar Alimentação do Roteador/Modem",
    3: "Verificar Indicadores de Conexão",
    4: "Reiniciar Equipamentos de Rede",
    5: "Verificar Conectividade de Internet"
}

STEP_INSTRUCTIONS = {
    1: "Verifique se o cabo de rede está firmemente conectado ao seu computador e ao roteador/switch.",
    2: "Certifique-se de que o roteador ou modem está ligado e funcionando corretamente.",
    3: "Observe as luzes indicadoras na porta de rede do seu computador e do roteador.",
    4: "Vamos reiniciar o modem/roteador para restabelecer a conexão.",
    5: "Agora vamos testar se a internet foi restabelecida."
}

# Imagens das etapas
STEP_IMAGES = {
    1: ASSETS_DIR / "step1_placeholder.png",
    2: ASSETS_DIR / "step2_placeholder.png",
    3: ASSETS_DIR / "step3_placeholder.png",
    4: ASSETS_DIR / "step4_placeholder.png",
    5: ASSETS_DIR / "step5_placeholder.png"
}
