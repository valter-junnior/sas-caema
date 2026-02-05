# Bugs e Issues

## ✅ Resolvido - 05/02/2026 15:30

### Issue #1: Scripts batch necessários?
**Pergunta:** run.bat e setup.bat ainda são necessários?

**Resposta:** ✅ Sim, mantidos pois são úteis como atalhos:
- `run.bat` - Executa a aplicação com Python rapidamente
- `setup.bat` - Instala dependências e configura tudo automaticamente
- Facilitam uso para quem prefere Python ao executável

### Issue #2: Documentação redundante
**Problema:** Muitos arquivos .md repetindo informações

**Solução:** ✅ Consolidado e simplificado:
- README.md único na raiz (essencial)
- Removidos: QUICK_START.md, IMPLEMENTAÇÃO_COMPLETA.md, BUGS_FIXED.md, BUGS_RESOLVED.md, BUILD_GUIDE.md
- Mantidos: documentacao.md, todo.md, utils.md, prompt.md
- Criado sistema de changelogs em docs/changelogs/

---

## 📋 Issues Abertas

Nenhuma no momento.

---

## 📝 Reportar Novo Bug

Para reportar um problema:
1. Descreva o comportamento esperado vs atual
2. Inclua passos para reproduzir
3. Adicione logs relevantes de `app/logs/`
4. Mencione versão do Windows e Python (se aplicável)