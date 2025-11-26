"""
Model Cliente
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    telefone: str = ""
    empresa: str = ""
    cnpj_cpf: str = ""
    endereco_rua: str = ""
    endereco_numero: str = ""
    endereco_bairro: str = ""
    endereco_cidade: str = ""
    endereco_estado: str = ""
    endereco_cep: str = ""
    observacoes: str = ""
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'empresa': self.empresa,
            'cnpj_cpf': self.cnpj_cpf,
            'endereco_rua': self.endereco_rua,
            'endereco_numero': self.endereco_numero,
            'endereco_bairro': self.endereco_bairro,
            'endereco_cidade': self.endereco_cidade,
            'endereco_estado': self.endereco_estado,
            'endereco_cep': self.endereco_cep,
            'observacoes': self.observacoes,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cliente':
        """Cria um objeto Cliente a partir de um dicionário"""
        return cls(**data)

