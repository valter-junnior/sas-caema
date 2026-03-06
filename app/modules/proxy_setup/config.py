"""
Configurações do módulo de configuração de proxy
"""

# Configurações do Proxy
PROXY_HOST = "10.39.192.11"
PROXY_PORT = 3128
PROXY_SERVER = f"{PROXY_HOST}:{PROXY_PORT}"

# Configurações de UI
STEP_COUNT = 3

# Textos das etapas
STEP_TITLES = {
    1: "Informações do Proxy",
    2: "Aplicar Configurações",
    3: "Verificar Configuração",
}

STEP_INSTRUCTIONS = {
    1: "Revise as informações antes de aplicar o proxy.",
    2: "Aplicando as configurações de proxy no sistema.",
    3: "Verificando se o proxy foi configurado corretamente.",
}
