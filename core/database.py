"""
Gerenciamento de conexão com banco de dados MySQL
"""
import mysql.connector
from mysql.connector import Error, pooling
from typing import Optional
import logging
from core.settings import DB_CONFIG

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de conexões com MySQL"""
    
    _connection_pool: Optional[pooling.MySQLConnectionPool] = None
    
    @classmethod
    def create_connection_pool(cls, pool_size: int = 5):
        """Cria um pool de conexões MySQL"""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="crm_pool",
                pool_size=pool_size,
                pool_reset_session=True,
                **DB_CONFIG
            )
            logger.info(f"Pool de conexões criado com sucesso (tamanho: {pool_size})")
            return True
        except Error as e:
            logger.error(f"Erro ao criar pool de conexões: {e}")
            return False
    
    @classmethod
    def get_connection(cls):
        """Obtém uma conexão do pool"""
        if cls._connection_pool is None:
            cls.create_connection_pool()
        
        try:
            connection = cls._connection_pool.get_connection()
            return connection
        except Error as e:
            logger.error(f"Erro ao obter conexão do pool: {e}")
            # Tentar criar conexão direta como fallback
            try:
                return mysql.connector.connect(**DB_CONFIG)
            except Error as fallback_error:
                logger.error(f"Erro ao criar conexão direta: {fallback_error}")
                raise
    
    @classmethod
    def test_connection(cls) -> bool:
        """Testa a conexão com o banco de dados"""
        try:
            conn = cls.get_connection()
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                logger.info(f"Conectado ao MySQL versão: {version[0]}")
                cursor.close()
                conn.close()
                return True
        except Error as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False
    
    @classmethod
    def execute_query(cls, query: str, params: tuple = None, fetch: bool = False):
        """Executa uma query e retorna o resultado se fetch=True"""
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid if cursor.lastrowid else True
            
            return result
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro ao executar query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    @classmethod
    def execute_many(cls, query: str, params_list: list):
        """Executa uma query múltiplas vezes com diferentes parâmetros"""
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return True
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro ao executar query múltipla: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

