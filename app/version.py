"""
Arquivo de versão do SAS-Caema
"""

__version__ = "1.0.1-beta"
__author__ = "Eduarda Cristina"
__date__ = "2026-04-10"

VERSION_INFO = {
    "major": 1,
    "minor": 0,
  "patch": 1,
  "release": "beta"
}

CHANGELOG = """
# Changelog

## [1.0.1-beta] - 2026-04-10

### ✨ Alterado
- Fluxo de distribuicao de aplicativos migrado para host remoto dedicado de assets
- Download de catalogo e instaladores padronizado via servico `assets_service`
- Catalogo de aplicativos atualizado para o formato `id,nome,installer_filename`
- Leitura de metadados de executaveis melhorada no CatalogService

### ✅ Beneficios
- Distribuicao de apps desacoplada do ciclo de release de codigo
- Nomes de aplicativos controlados pelo catalogo para exibicao consistente
- Melhor resiliencia no carregamento de metadados

## [1.0.0] - 2026-02-05

### ✨ Adicionado
- Interface gráfica principal com PyQt5
- Módulo de papel de parede personalizado
  - Coleta automática de informações do sistema
  - Geração de imagem com texto sobreposto
  - Configuração automática no Windows
- Módulo de checkup do sistema
  - Verificações automáticas
  - Correção automática de problemas
  - Sistema de notificações
- Sistema de logs estruturado
- Instalação e configuração automática
- Inicialização automática com o Windows
- Scripts batch para facilitar uso
- Documentação completa

### 🎯 Recursos Principais
- ✅ Papel de parede com informações de suporte
- ✅ Checkup automático na inicialização
- ✅ Interface intuitiva e moderna
- ✅ Sistema de logs detalhado
- ✅ Fácil instalação e configuração

### 📝 Módulos Implementados
- Wallpaper (Papel de Parede)
- Checkup (Verificação do Sistema)

### 🔜 Próximas Versões
- Módulo de instalação de aplicativos
- Módulo de configuração de proxy
- Módulo de instalação de impressoras
- Base de conhecimento integrada
"""
