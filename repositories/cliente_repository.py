"""
Repository para Cliente
"""
from typing import List, Optional
from models.cliente import Cliente
from repositories.base_repository import BaseRepository
from core.database import DatabaseManager


class ClienteRepository(BaseRepository[Cliente]):
    """Repository para operações CRUD de Cliente"""
    
    def __init__(self):
        super().__init__('clientes')
    
    def _row_to_entity(self, row: dict) -> Cliente:
        """Converte uma linha do banco em Cliente"""
        return Cliente(
            id=row.get('id'),
            nome=row.get('nome', ''),
            email=row.get('email', ''),
            telefone=row.get('telefone', ''),
            empresa=row.get('empresa', ''),
            cnpj_cpf=row.get('cnpj_cpf', ''),
            endereco_rua=row.get('endereco_rua', ''),
            endereco_numero=row.get('endereco_numero', ''),
            endereco_bairro=row.get('endereco_bairro', ''),
            endereco_cidade=row.get('endereco_cidade', ''),
            endereco_estado=row.get('endereco_estado', ''),
            endereco_cep=row.get('endereco_cep', ''),
            observacoes=row.get('observacoes', ''),
            criado_em=row.get('criado_em'),
            atualizado_em=row.get('atualizado_em')
        )
    
    def criar(self, cliente: Cliente) -> int:
        """Cria um novo cliente e retorna o ID"""
        query = """
            INSERT INTO clientes (nome, email, telefone, empresa, cnpj_cpf,
                                endereco_rua, endereco_numero, endereco_bairro,
                                endereco_cidade, endereco_estado, endereco_cep, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            cliente.nome, cliente.email, cliente.telefone, cliente.empresa,
            cliente.cnpj_cpf, cliente.endereco_rua, cliente.endereco_numero,
            cliente.endereco_bairro, cliente.endereco_cidade, cliente.endereco_estado,
            cliente.endereco_cep, cliente.observacoes
        )
        try:
            result = DatabaseManager.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Erro ao criar cliente: {e}")
            raise
    
    def atualizar(self, cliente: Cliente) -> bool:
        """Atualiza um cliente existente"""
        query = """
            UPDATE clientes SET
                nome = %s, email = %s, telefone = %s, empresa = %s, cnpj_cpf = %s,
                endereco_rua = %s, endereco_numero = %s, endereco_bairro = %s,
                endereco_cidade = %s, endereco_estado = %s, endereco_cep = %s,
                observacoes = %s
            WHERE id = %s
        """
        params = (
            cliente.nome, cliente.email, cliente.telefone, cliente.empresa,
            cliente.cnpj_cpf, cliente.endereco_rua, cliente.endereco_numero,
            cliente.endereco_bairro, cliente.endereco_cidade, cliente.endereco_estado,
            cliente.endereco_cep, cliente.observacoes, cliente.id
        )
        try:
            DatabaseManager.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False
    
    def buscar(self, termo: str) -> List[Cliente]:
        """Busca clientes por nome, email, empresa ou cidade"""
        query = """
            SELECT * FROM clientes
            WHERE nome LIKE %s OR email LIKE %s OR empresa LIKE %s OR endereco_cidade LIKE %s
            ORDER BY nome
        """
        termo_like = f"%{termo}%"
        params = (termo_like, termo_like, termo_like, termo_like)
        try:
            result = DatabaseManager.execute_query(query, params, fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar clientes: {e}")
            return []

