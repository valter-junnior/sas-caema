# Bugs e Melhorias - SAS-Caema

## ✅ Resolvido - 05/02/2026 21:00

### Timer na Etapa 4 atrapalhava o fluxo
**Descrição**: O timer de 2 minutos na etapa 4 (Reiniciar Equipamentos) bloqueava a navegação e atrapalhava o fluxo do wizard.

**Solução**: Removido o sistema de timer. Agora a etapa 4 apenas mostra as instruções com um aviso informativo para o usuário aguardar antes de avançar, mas sem bloqueio forçado.

**Arquivos modificados**:
- `app/modules/network_troubleshoot/views/step_widgets.py` - Simplificado Step4Widget
- `app/modules/network_troubleshoot/views/wizard_window.py` - Removida lógica de bloqueio

**Impacto**: Melhora significativa na experiência do usuário, permitindo fluxo mais natural.
