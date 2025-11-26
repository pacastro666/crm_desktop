"""
Repository para Oportunidade
"""
from typing import List, Optional
from datetime import date
from models.oportunidade import Oportunidade
from repositories.base_repository import BaseRepository
from core.database import DatabaseManager


class OportunidadeRepository(BaseRepository[Oportunidade]):
    """Repository para operações CRUD de Oportunidade"""
    
    def __init__(self):
        super().__init__('oportunidades')
    
    def _row_to_entity(self, row: dict) -> Oportunidade:
        """Converte uma linha do banco em Oportunidade"""
        return Oportunidade(
            id=row.get('id'),
            cliente_id=row.get('cliente_id', 0),
            titulo=row.get('titulo', ''),
            etapa=row.get('etapa', 'Lead'),
            valor=float(row.get('valor', 0.0)),
            probabilidade=row.get('probabilidade', 0),
            data_prevista_fechamento=row.get('data_prevista_fechamento'),
            responsavel=row.get('responsavel', ''),
            observacoes=row.get('observacoes', ''),
            criado_em=row.get('criado_em'),
            atualizado_em=row.get('atualizado_em')
        )
    
    def criar(self, oportunidade: Oportunidade) -> int:
        """Cria uma nova oportunidade e retorna o ID"""
        query = """
            INSERT INTO oportunidades (cliente_id, titulo, etapa, valor, probabilidade,
                                     data_prevista_fechamento, responsavel, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            oportunidade.cliente_id, oportunidade.titulo, oportunidade.etapa,
            oportunidade.valor, oportunidade.probabilidade,
            oportunidade.data_prevista_fechamento, oportunidade.responsavel,
            oportunidade.observacoes
        )
        try:
            result = DatabaseManager.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Erro ao criar oportunidade: {e}")
            raise
    
    def atualizar(self, oportunidade: Oportunidade) -> bool:
        """Atualiza uma oportunidade existente"""
        query = """
            UPDATE oportunidades SET
                cliente_id = %s, titulo = %s, etapa = %s, valor = %s,
                probabilidade = %s, data_prevista_fechamento = %s,
                responsavel = %s, observacoes = %s
            WHERE id = %s
        """
        params = (
            oportunidade.cliente_id, oportunidade.titulo, oportunidade.etapa,
            oportunidade.valor, oportunidade.probabilidade,
            oportunidade.data_prevista_fechamento, oportunidade.responsavel,
            oportunidade.observacoes, oportunidade.id
        )
        try:
            DatabaseManager.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Erro ao atualizar oportunidade: {e}")
            return False
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Oportunidade]:
        """Busca oportunidades de um cliente"""
        query = "SELECT * FROM oportunidades WHERE cliente_id = %s ORDER BY criado_em DESC"
        try:
            result = DatabaseManager.execute_query(query, (cliente_id,), fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar oportunidades por cliente: {e}")
            return []
    
    def buscar_por_etapa(self, etapa: str) -> List[Oportunidade]:
        """Busca oportunidades por etapa"""
        query = "SELECT * FROM oportunidades WHERE etapa = %s ORDER BY data_prevista_fechamento"
        try:
            result = DatabaseManager.execute_query(query, (etapa,), fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar oportunidades por etapa: {e}")
            return []
    
    def atualizar_etapa(self, id: int, nova_etapa: str) -> bool:
        """Atualiza apenas a etapa de uma oportunidade"""
        query = "UPDATE oportunidades SET etapa = %s WHERE id = %s"
        try:
            DatabaseManager.execute_query(query, (nova_etapa, id))
            return True
        except Exception as e:
            print(f"Erro ao atualizar etapa: {e}")
            return False

