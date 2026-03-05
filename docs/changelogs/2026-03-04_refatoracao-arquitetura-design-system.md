# 2026-03-04 — Refatoração Completa: Arquitetura MVVM + Design System

## Resumo

Refatoração completa do diretório `/app` com foco em:
- Arquitetura limpa inspirada em MVVM
- Sistema de design centralizado (DRY)
- Visual moderno próximo ao padrão web (Tailwind/Material)
- Clean Code em todas as camadas

---

## Arquivos Criados

### `app/common/theme.py`
Fonte única de verdade para todo o design system:
- `Colors` — paleta de cores completa (primária, sucesso, perigo, aviso, neutros, header)
- `Fonts` — factory de `QFont` padronizados (title, heading, subheading, body, caption)
- `Styles` — templates QSS reutilizáveis para botões, cards e stylesheet global da aplicação

### `app/common/widgets.py`
Biblioteca de componentes reutilizáveis (aplica o princípio DRY):
- `PrimaryButton`, `SecondaryButton`, `SuccessButton`, `GhostDangerButton`
- `Card` — container branco com borda e sombra suave
- `Divider` — separador horizontal fino
- `TitleLabel`, `HeadingLabel`, `BodyLabel`, `CaptionLabel`
- `HeaderBar` — barra de header escura com título e subtítulo
- `InfoBanner` — banner colorido para info/sucesso/aviso/erro

---

## Arquivos Modificados

### `app/app.py`
- Aplica `Styles.global_app()` ao `QApplication` — estilo global consistente
- Aplica fonte padrão `Segoe UI 10pt` antes de criar a janela

### `app/common/views/main_window.py`
Redesenho completo:
- **Header escuro** com nome do app e subtítulo (borda azul inferior)
- **Cards de ação** (`ActionCard`) substituem botões planos — ícone, título, descrição, botão
- **Rodapé de status** com indicador colorido (●) — sem mais `statusBar()` nativo
- Menu `Configurações` usa `AboutDialog` customizado
- Callbacks renomeados com prefixo `_` (privados): `_run_checkup`, `_show_solutions`, etc.

### `app/common/views/dialogs.py`
Substituição completa de `QMessageBox` por dialogs customizados:
- `BaseDialog` — base com header/body/footer padronizados
- `InfoDialog`, `SuccessDialog`, `IssuesDialog`, `ErrorDialog`, `AboutDialog`
- `ResultDialogs` mantido como factory estática com aliases retrocompatíveis

### `app/common/views/solutions_dialog.py`
- `SolutionCard` — card clicável por solução com ícone, nome e descrição
- Seleção visual via borda colorida (azul quando ativo)
- Layout header + área de cards + rodapé com botões

### `app/modules/network_troubleshoot/views/wizard_window.py`
- `StepIndicator` — indicador de progresso com círculos numerados + linhas conectoras
  - Círculos: concluído (verde ✓), ativo (azul), pendente (cinza)
- Header escuro com título e label "Etapa X de Y"
- Botões de navegação usando componentes do design system
- Callbacks privados com aliases públicos para retrocompatibilidade

### `app/modules/network_troubleshoot/views/step_widgets.py`
- `BaseStepWidget` refatorado com scroll area, imagem, instrução e layout padronizados
- `_make_checklist_card()` — helper DRY para criar cards de checklist
- `Step1Widget` a `Step4Widget` usam `InfoBanner` e cards limpos
- `Step5Widget` usa `SuccessButton` e feedback com border colorida

### `app/modules/checkup/startup/startup_feedback.py`
- Importações atualizadas: usa `Colors` e `Fonts` do design system
- Cores hardcoded (`#FF8C00`, `SUCCESS_COLOR`, `ERROR_COLOR`) substituídas por `Colors.*`
- Fontes criadas via `Fonts.heading()`, `Fonts.subheading()`, `Fonts.caption()`

---

## Arquivos Não Alterados

Arquivos de lógica de negócios sem UI foram preservados integralmente:
- `config.py`, `version.py`
- `common/services/logger.py`, `solutions_service.py`
- `modules/checkup/services/checkup_service.py`
- `modules/checkup/threads/checkup_thread.py`
- `modules/checkup/startup/main.py`
- `modules/network_troubleshoot/services/network_checker.py`, `step_validator.py`
- `modules/wallpaper/**`
- `/build/**`, `/installer/**`
