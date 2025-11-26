"""
Repository para Tarefa
"""
from typing import List, Optional
from datetime import datetime
from models.tarefa import Tarefa
from repositories.base_repository import BaseRepository
from core.database import DatabaseManager


class TarefaRepository(BaseRepository[Tarefa]):
    """Repository para operações CRUD de Tarefa"""
    
    def __init__(self):
        super().__init__('tarefas')
    
    def _row_to_entity(self, row: dict) -> Tarefa:
        """Converte uma linha do banco em Tarefa"""
        return Tarefa(
            id=row.get('id'),
            cliente_id=row.get('cliente_id', 0),
            descricao=row.get('descricao', ''),
            tipo=row.get('tipo', 'Outro'),
            data_hora=row.get('data_hora'),
            status=row.get('status', 'Pendente'),
            prioridade=row.get('prioridade', 'Média'),
            observacoes=row.get('observacoes', ''),
            criado_em=row.get('criado_em'),
            concluida_em=row.get('concluida_em')
        )
    
    def criar(self, tarefa: Tarefa) -> int:
        """Cria uma nova tarefa e retorna o ID"""
        query = """
            INSERT INTO tarefas (cliente_id, descricao, tipo, data_hora, status, prioridade, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            tarefa.cliente_id, tarefa.descricao, tarefa.tipo,
            tarefa.data_hora, tarefa.status, tarefa.prioridade, tarefa.observacoes
        )
        try:
            result = DatabaseManager.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            raise
    
    def atualizar(self, tarefa: Tarefa) -> bool:
        """Atualiza uma tarefa existente"""
        query = """
            UPDATE tarefas SET
                cliente_id = %s, descricao = %s, tipo = %s, data_hora = %s,
                status = %s, prioridade = %s, observacoes = %s
            WHERE id = %s
        """
        params = (
            tarefa.cliente_id, tarefa.descricao, tarefa.tipo,
            tarefa.data_hora, tarefa.status, tarefa.prioridade,
            tarefa.observacoes, tarefa.id
        )
        try:
            DatabaseManager.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")
            return False
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Tarefa]:
        """Busca tarefas de um cliente"""
        query = "SELECT * FROM tarefas WHERE cliente_id = %s ORDER BY data_hora DESC"
        try:
            result = DatabaseManager.execute_query(query, (cliente_id,), fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar tarefas por cliente: {e}")
            return []
    
    def buscar_por_status(self, status: str) -> List[Tarefa]:
        """Busca tarefas por status"""
        query = "SELECT * FROM tarefas WHERE status = %s ORDER BY data_hora"
        try:
            result = DatabaseManager.execute_query(query, (status,), fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar tarefas por status: {e}")
            return []
    
    def buscar_pendentes_hoje(self) -> List[Tarefa]:
        """Busca tarefas pendentes de hoje"""
        query = """
            SELECT * FROM tarefas
            WHERE status = 'Pendente' AND DATE(data_hora) = CURDATE()
            ORDER BY data_hora
        """
        try:
            result = DatabaseManager.execute_query(query, fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar tarefas pendentes hoje: {e}")
            return []
    
    def buscar_atrasadas(self) -> List[Tarefa]:
        """Busca tarefas pendentes atrasadas"""
        query = """
            SELECT * FROM tarefas
            WHERE status = 'Pendente' AND data_hora < NOW()
            ORDER BY data_hora
        """
        try:
            result = DatabaseManager.execute_query(query, fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao buscar tarefas atrasadas: {e}")
            return []
    
    def marcar_concluida(self, id: int) -> bool:
        """Marca uma tarefa como concluída"""
        query = """
            UPDATE tarefas SET status = 'Concluída', concluida_em = NOW()
            WHERE id = %s
        """
        try:
            DatabaseManager.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Erro ao marcar tarefa como concluída: {e}")
            return False

