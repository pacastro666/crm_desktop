"""
Model Interacao (Histórico)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Interacao:
    id: Optional[int] = None
    cliente_id: int = 0
    tipo: str = ""  # cliente_criado, cliente_editado, oportunidade_criada, etc
    descricao: str = ""
    criado_em: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'criado_em': self.criado_em
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Interacao':
        """Cria um objeto Interacao a partir de um dicionário"""
        return cls(**data)

