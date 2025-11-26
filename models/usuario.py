"""
Model Usuario
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha_hash: str = ""
    nivel_acesso: str = "Vendedor"  # Admin, Vendedor, Visualizador
    ativo: bool = True
    criado_em: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha_hash': self.senha_hash,
            'nivel_acesso': self.nivel_acesso,
            'ativo': self.ativo,
            'criado_em': self.criado_em
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        """Cria um objeto Usuario a partir de um dicionário"""
        return cls(**data)

