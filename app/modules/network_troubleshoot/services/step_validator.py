"""
Serviço de validação de etapas do wizard
"""
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common.services.logger import logger_service
from modules.network_troubleshoot import config


class StepValidator:
    """Gerencia a validação e controle de fluxo entre etapas"""
    
    def __init__(self):
        """Inicializa o validador de etapas"""
        self.logger = logger_service.get_logger('StepValidator')
        self.completed_steps = set()
        self.current_step = 1
        self.total_steps = config.STEP_COUNT
    
    def validate_step(self, step_number: int) -> bool:
        """
        Valida se a etapa pode ser concluída
        
        Args:
            step_number: Número da etapa a validar
            
        Returns:
            True se a etapa pode ser concluída, False caso contrário
        """
        # Por padrão, todas as etapas podem ser concluídas
        # Esta lógica pode ser expandida no futuro com validações específicas
        
        if step_number < 1 or step_number > self.total_steps:
            self.logger.warning(f"Etapa inválida: {step_number}")
            return False
        
        return True
    
    def mark_step_complete(self, step_number: int) -> bool:
        """
        Marca etapa como concluída
        
        Args:
            step_number: Número da etapa a marcar como concluída
            
        Returns:
            True se marcado com sucesso, False caso contrário
        """
        if not self.validate_step(step_number):
            return False
        
        self.completed_steps.add(step_number)
        self.logger.info(f"Etapa {step_number} marcada como concluída")
        return True
    
    def can_proceed_to_next(self) -> bool:
        """
        Verifica se pode avançar para próxima etapa
        
        Returns:
            True se pode avançar, False caso contrário
        """
        # Pode avançar se não estiver na última etapa
        can_proceed = self.current_step < self.total_steps
        self.logger.debug(f"Pode avançar para próxima etapa: {can_proceed}")
        return can_proceed
    
    def can_go_back(self) -> bool:
        """
        Verifica se pode voltar para etapa anterior
        
        Returns:
            True se pode voltar, False caso contrário
        """
        # Pode voltar se não estiver na primeira etapa
        can_go_back = self.current_step > 1
        self.logger.debug(f"Pode voltar para etapa anterior: {can_go_back}")
        return can_go_back
    
    def next_step(self) -> bool:
        """
        Avança para próxima etapa
        
        Returns:
            True se avançou com sucesso, False caso contrário
        """
        if self.can_proceed_to_next():
            self.current_step += 1
            self.logger.info(f"Avançou para etapa {self.current_step}")
            return True
        return False
    
    def previous_step(self) -> bool:
        """
        Retorna para etapa anterior
        
        Returns:
            True se voltou com sucesso, False caso contrário
        """
        if self.can_go_back():
            self.current_step -= 1
            self.logger.info(f"Voltou para etapa {self.current_step}")
            return True
        return False
    
    def get_progress(self) -> tuple:
        """
        Retorna progresso atual
        
        Returns:
            Tupla (etapa_atual, total_etapas)
        """
        return (self.current_step, self.total_steps)
    
    def is_step_completed(self, step_number: int) -> bool:
        """
        Verifica se uma etapa específica foi concluída
        
        Args:
            step_number: Número da etapa
            
        Returns:
            True se a etapa foi concluída, False caso contrário
        """
        return step_number in self.completed_steps
    
    def reset(self):
        """Reseta o validador para o estado inicial"""
        self.completed_steps.clear()
        self.current_step = 1
        self.logger.info("Validador resetado")
