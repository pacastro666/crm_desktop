"""
Repository base com operações CRUD genéricas
"""
from typing import List, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from core.database import DatabaseManager

T = TypeVar('T', bound=object)


class BaseRepository(ABC, Generic[T]):
    """Classe base para repositories"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    @abstractmethod
    def _row_to_entity(self, row: dict) -> T:
        """Converte uma linha do banco em entidade"""
        pass
    
    def buscar_por_id(self, id: int) -> Optional[T]:
        """Busca uma entidade por ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        try:
            result = DatabaseManager.execute_query(query, (id,), fetch=True)
            if result:
                return self._row_to_entity(result[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar por ID: {e}")
            return None
    
    def listar_todos(self) -> List[T]:
        """Lista todas as entidades"""
        query = f"SELECT * FROM {self.table_name} ORDER BY id DESC"
        try:
            result = DatabaseManager.execute_query(query, fetch=True)
            return [self._row_to_entity(row) for row in result]
        except Exception as e:
            print(f"Erro ao listar todos: {e}")
            return []
    
    def excluir(self, id: int) -> bool:
        """Exclui uma entidade por ID"""
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        try:
            DatabaseManager.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Erro ao excluir: {e}")
            return False

