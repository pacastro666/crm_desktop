"""
Model Tarefa
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tarefa:
    id: Optional[int] = None
    cliente_id: int = 0
    descricao: str = ""
    tipo: str = "Outro"  # Ligação, Email, Reunião, WhatsApp, Visita, Outro
    data_hora: Optional[datetime] = None
    status: str = "Pendente"  # Pendente, Concluída
    prioridade: str = "Média"  # Baixa, Média, Alta
    observacoes: str = ""
    criado_em: Optional[datetime] = None
    concluida_em: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'data_hora': self.data_hora,
            'status': self.status,
            'prioridade': self.prioridade,
            'observacoes': self.observacoes,
            'criado_em': self.criado_em,
            'concluida_em': self.concluida_em
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tarefa':
        """Cria um objeto Tarefa a partir de um dicionário"""
        return cls(**data)

