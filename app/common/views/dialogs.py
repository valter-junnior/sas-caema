"""
Diálogos de resultado do checkup
"""
import sys
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))


class ResultDialogs:
    """Classe para gerenciar os diálogos de resultado"""
    
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
        msg.setText("<h2 style='color: #107C10;'>✓ Sistema OK</h2>")
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
            title_icon = "✓"
            title_text = "Problemas Corrigidos"
            msg.setIcon(QMessageBox.Information)
        else:
            title_color = "#FF8C00"
            title_icon = "⚠"
            title_text = "Atenção Necessária"
            msg.setIcon(QMessageBox.Warning)
        
        msg.setText(f"<h2 style='color: {title_color};'>{title_icon} {title_text}</h2>")
        
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
