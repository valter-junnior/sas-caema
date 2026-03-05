"""
Dialogs customizados do SAS-Caema.
Substitui QMessageBox por dialogs estilizados alinhados ao design system.
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.theme import Colors, Fonts
from common.widgets import (
    PrimaryButton, SecondaryButton, BodyLabel, InfoBanner,
)


# ---------------------------------------------------------------------------
# Base Dialog
# ---------------------------------------------------------------------------

class BaseDialog(QDialog):
    """Classe base para todos os dialogs customizados."""

    def __init__(self, parent=None, title: str = "", min_width: int = 440):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(min_width)
        self.setStyleSheet(f"QDialog {{ background-color: {Colors.SURFACE}; }}")
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)

    def _add_header(self, icon: str, title: str, subtitle: str = ""):
        header = QWidget()
        header.setObjectName("dialogHeader")
        header.setStyleSheet(
            f"QWidget#dialogHeader {{"
            f"background-color: {Colors.BACKGROUND}; "
            f"border-bottom: 1px solid {Colors.BORDER};"
            f"}}"
        )
        hl = QVBoxLayout(header)
        hl.setContentsMargins(28, 20, 28, 20)
        hl.setSpacing(6)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont(Fonts.FAMILY, 20))
        icon_lbl.setStyleSheet("background: transparent;")
        top_row.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setFont(Fonts.heading(13))
        title_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        top_row.addWidget(title_lbl)
        top_row.addStretch()
        hl.addLayout(top_row)

        if subtitle:
            sub = BodyLabel(subtitle)
            sub.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
            hl.addWidget(sub)

        self._root.addWidget(header)

    def _add_body(self) -> QVBoxLayout:
        body = QWidget()
        body.setStyleSheet(f"background-color: {Colors.SURFACE};")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(12)
        self._root.addWidget(body, stretch=1)
        return layout

    def _add_footer(self, *buttons):
        footer = QWidget()
        footer.setObjectName("dialogFooter")
        footer.setStyleSheet(
            f"QWidget#dialogFooter {{"
            f"background-color: {Colors.BACKGROUND}; "
            f"border-top: 1px solid {Colors.BORDER};"
            f"}}"
        )
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 14, 24, 14)
        fl.setSpacing(10)
        fl.addStretch()
        for btn in buttons:
            fl.addWidget(btn)
        self._root.addWidget(footer)


# ---------------------------------------------------------------------------
# Dialogs concretos
# ---------------------------------------------------------------------------

class InfoDialog(BaseDialog):
    """Dialog informativo genérico."""

    def __init__(self, parent, title: str, message: str, icon: str = "ℹ️"):
        super().__init__(parent, title)
        self._add_header(icon, title)
        body = self._add_body()
        body.addWidget(BodyLabel(message))
        ok_btn = PrimaryButton("OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        self._add_footer(ok_btn)


class SuccessDialog(BaseDialog):
    """Dialog de resultado de checkup bem-sucedido."""

    def __init__(self, parent):
        super().__init__(parent, "Checkup Concluído")
        self._add_header("✅", "Sistema OK", "Nenhum problema foi encontrado.")
        body = self._add_body()
        body.addWidget(InfoBanner("O sistema está funcionando corretamente.", 'success'))
        ok_btn = PrimaryButton("OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        self._add_footer(ok_btn)


class IssuesDialog(BaseDialog):
    """Dialog que apresenta os problemas encontrados e as correções aplicadas."""

    def __init__(self, parent, checks: list, fixes: dict):
        super().__init__(parent, "Checkup Concluído", min_width=500)

        fixed = sum(1 for v in fixes.values() if v)
        failed = len(fixes) - fixed
        issues_count = sum(1 for c in checks if c.get('status') != 'ok')

        icon = "⚠️" if failed > 0 else "✅"
        subtitle = "Atenção necessária" if failed > 0 else "Problemas corrigidos"
        self._add_header(icon, subtitle)

        body = self._add_body()

        if fixed > 0:
            body.addWidget(
                InfoBanner(f"✓  {fixed} problema(s) corrigido(s) automaticamente.", 'success')
            )
        if failed > 0:
            body.addWidget(
                InfoBanner(
                    f"✗  {failed} problema(s) não pud{'e' if failed == 1 else 'eram'} ser "
                    "corrigido(s). Verifique os logs para detalhes.",
                    'error',
                )
            )

        issues_with_text = [c for c in checks if c.get('status') != 'ok']
        if issues_with_text:
            details_title = QLabel("Detalhes:")
            details_title.setFont(Fonts.heading(10))
            details_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            body.addWidget(details_title)
            for check in issues_with_text:
                row = BodyLabel(f"• {check.get('message', 'Sem descrição')}")
                body.addWidget(row)

        ok_btn = PrimaryButton("OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        self._add_footer(ok_btn)


class ErrorDialog(BaseDialog):
    """Dialog de erro."""

    def __init__(self, parent, message: str):
        super().__init__(parent, "Erro")
        self._add_header("❌", "Ocorreu um problema")
        body = self._add_body()
        body.addWidget(InfoBanner(message, 'error'))
        note = BodyLabel("Verifique os logs para mais detalhes.")
        note.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        body.addWidget(note)
        ok_btn = PrimaryButton("OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        self._add_footer(ok_btn)


class AboutDialog(BaseDialog):
    """Dialog 'Sobre'."""

    def __init__(self, app_name: str, version: str, parent=None):
        super().__init__(parent, f"Sobre {app_name}")
        self._add_header("📌", app_name, "Sistema de Automação de Suporte")
        body = self._add_body()
        for text in [f"Versão: {version}", "Desenvolvido para Caema", "© 2026"]:
            body.addWidget(BodyLabel(text))
        ok_btn = PrimaryButton("Fechar")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(self.accept)
        self._add_footer(ok_btn)


# ---------------------------------------------------------------------------
# Factory estática (mantém compatibilidade com código existente)
# ---------------------------------------------------------------------------

class ResultDialogs:
    """Atalhos estáticos para exibir os dialogs de resultado."""

    @staticmethod
    def show_success(parent):
        SuccessDialog(parent).exec_()

    @staticmethod
    def show_issues(parent, checks: list, fixes: dict):
        IssuesDialog(parent, checks, fixes).exec_()

    @staticmethod
    def show_error(parent, message: str):
        ErrorDialog(parent, message).exec_()

    @staticmethod
    def show_info(parent, title: str, message: str, icon: str = "ℹ️"):
        InfoDialog(parent, title, message, icon).exec_()

    # Aliases para retrocompatibilidade
    @staticmethod
    def show_success_dialog(parent):
        ResultDialogs.show_success(parent)

    @staticmethod
    def show_issues_dialog(parent, checks: list, fixes: dict):
        ResultDialogs.show_issues(parent, checks, fixes)

    @staticmethod
    def show_error_dialog(parent, message: str):
        ResultDialogs.show_error(parent, message)

    
    @staticmethod
    def get_module_name(module_id: str) -> str:
        """Obtém o nome legível do módulo a partir do ID"""
        # Mapeamento de IDs para nomes legíveis
        module_names = {
            'wallpaper': 'Papel de Parede',
            # Adicione mais módulos aqui conforme necessário
        }
        return module_names.get(module_id, module_id.title())
    
    @staticmethod
    def show_success_dialog(parent):
        """Mostra dialog de sucesso estilizado"""
        msg = QMessageBox(parent)
        msg.setWindowTitle("Checkup Concluído")
        
        # Título e texto
        msg.setText("<h2 style='color: #107C10;'>Sistema OK</h2>")
        msg.setInformativeText(
            "<p style='font-size: 11pt;'>Nenhum problema encontrado!</p>"
            "<p style='color: #666666;'>O sistema está funcionando corretamente.</p>"
        )
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        # Estilo do botão
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                min-width: 400px;
            }
            QPushButton {
                background-color: #107C10;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0E6A0E;
            }
        """)
        
        msg.exec_()
    
    @staticmethod
    def show_issues_dialog(parent, checks: list, fixes: dict):
        """Mostra dialog de problemas com estilo melhorado"""
        msg = QMessageBox(parent)
        msg.setWindowTitle("Checkup Concluído")
        
        # Conta sucessos e falhas
        fixed_count = sum(1 for success in fixes.values() if success)
        failed_count = len(fixes) - fixed_count
        issues_count = sum(1 for c in checks if c['status'] != 'ok')
        
        # Título
        if failed_count == 0:
            title_color = "#107C10"
            title_text = "Problemas Corrigidos"
        else:
            title_color = "#FF8C00"
            title_text = "Atenção Necessária"
        
        msg.setText(f"<h2 style='color: {title_color};'>{title_text}</h2>")
        
        # Monta detalhes
        details = f"<div style='font-size: 10pt;'>"
        details += f"<p><b>Problemas encontrados:</b> {issues_count}</p>"
        
        # Lista problemas
        details += "<p style='margin-top: 10px;'><b>Detalhes:</b></p>"
        details += "<ul style='margin-left: 20px;'>"
        for check in checks:
            if check['status'] != 'ok':
                module_id = check.get('module', 'unknown')
                module_name = ResultDialogs.get_module_name(module_id)
                check_message = check.get('message', 'Sem descrição')
                details += f"<li>{check_message}</li>"
        details += "</ul>"
        
        # Resultados das correções
        if fixes:
            details += "<p style='margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd;'><b>Resultados:</b></p>"
            
            if fixed_count > 0:
                details += f"<p style='color: #107C10;'>✓ <b>{fixed_count}</b> problema(s) corrigido(s) automaticamente</p>"
            
            if failed_count > 0:
                details += f"<p style='color: #E81123;'>✗ <b>{failed_count}</b> problema(s) não puderam ser corrigidos</p>"
                
                # Lista quais falharam
                details += "<p style='margin-top: 5px; font-size: 9pt; color: #666;'>Problemas não corrigidos:</p>"
                details += "<ul style='margin-left: 20px; font-size: 9pt; color: #666;'>"
                for module_id, success in fixes.items():
                    if not success:
                        module_name = ResultDialogs.get_module_name(module_id)
                        details += f"<li>{module_name}</li>"
                details += "</ul>"
                
                details += "<p style='margin-top: 10px; font-size: 9pt; color: #666; font-style: italic;'>"
                details += "Verifique os logs para mais detalhes sobre os erros."
                details += "</p>"
        
        details += "</div>"
        
        msg.setInformativeText(details)
        msg.setTextFormat(Qt.RichText)
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        # Estilo
        button_color = "#107C10" if failed_count == 0 else "#0078D4"
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
            }}
            QLabel {{
                min-width: 400px;
            }}
            QPushButton {{
                background-color: {button_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
        """)
        
        msg.exec_()
    
    @staticmethod
    def show_error_dialog(parent, error_message: str):
        """Mostra dialog de erro estilizado"""
        msg = QMessageBox(parent)
        msg.setWindowTitle("Erro no Checkup")
        
        msg.setText("<h2 style='color: #E81123;'>✗ Erro</h2>")
        msg.setInformativeText(
            f"<p style='font-size: 10pt;'>Ocorreu um erro ao executar o checkup:</p>"
            f"<p style='font-family: Consolas; background-color: #f5f5f5; padding: 10px; "
            f"border-radius: 4px; color: #d32f2f;'>{error_message}</p>"
            f"<p style='font-size: 9pt; color: #666; margin-top: 10px;'>"
            f"Verifique os logs para mais informações."
            f"</p>"
        )
        msg.setTextFormat(Qt.RichText)
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                min-width: 400px;
            }
            QPushButton {
                background-color: #E81123;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 10pt;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #C50F1F;
            }
        """)
        
        msg.exec_()
