"""
Repository para Interacao
"""
from typing import List, Optional
from models.interacao import Interacao
from repositories.base_repository import BaseRepository
from core.database import DatabaseManager


class InteracaoRepository(BaseRepository[Interacao]):
    """Repository para operações CRUD de Interacao"""
    
    def __init__(self):
        super().__init__('interacoes')
    
    def _row_to_entity(self, row: dict) -> Interacao:
        """Converte uma linha do banco em Interacao"""
        return Interacao(
            id=row.get('id'),
            cliente_id=row.get('cliente_id', 0),
            tipo=row.get('tipo', ''),
            descricao=row.get('descricao', ''),
            criado_em=row.get('criado_em')
        )
    
    def criar(self, interacao: Interacao) -> int:
        """Cria uma nova interação e retorna o ID"""
        query = """
            INSERT INTO interacoes (cliente_id, tipo, descricao)
            VALUES (%s, %s, %s)
        """
        params = (interacao.cliente_id, interacao.tipo, interacao.descricao)
        try:
            result = DatabaseManager.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Erro ao criar interação: {e}")
            raise
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Interacao]:
        """Busca interações de um cliente ordenadas por data"""
        query = """
            SELECT * FROM interacoes
            WHERE cliente_id = %s
            ORDER BY criado_em DESC
        """
        try:
            result = DatabaseManager.execute_query(query, (cliente_id,), fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar interações por cliente: {e}")
            return []

