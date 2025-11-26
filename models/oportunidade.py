"""
Model Oportunidade
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Oportunidade:
    id: Optional[int] = None
    cliente_id: int = 0
    titulo: str = ""
    etapa: str = "Lead"  # Lead, Qualificação, Proposta, Negociação, Fechado, Perdido
    valor: float = 0.0
    probabilidade: int = 0  # 0-100
    data_prevista_fechamento: Optional[date] = None
    responsavel: str = ""
    observacoes: str = ""
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'titulo': self.titulo,
            'etapa': self.etapa,
            'valor': float(self.valor),
            'probabilidade': self.probabilidade,
            'data_prevista_fechamento': self.data_prevista_fechamento,
            'responsavel': self.responsavel,
            'observacoes': self.observacoes,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Oportunidade':
        """Cria um objeto Oportunidade a partir de um dicionário"""
        return cls(**data)

