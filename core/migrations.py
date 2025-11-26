"""
Scripts de criação e atualização das tabelas do banco de dados MySQL
"""
import logging
from core.database import DatabaseManager
from mysql.connector import Error

logger = logging.getLogger(__name__)

class Migrations:
    """Gerencia as migrações do banco de dados"""
    
    @staticmethod
    def create_database_if_not_exists():
        """Cria o banco de dados se não existir"""
        from core.settings import DB_CONFIG
        import mysql.connector
        
        # Conectar sem especificar o database
        config = DB_CONFIG.copy()
        database_name = config.pop('database')
        
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"Banco de dados '{database_name}' verificado/criado com sucesso")
            cursor.close()
            conn.close()
            return True
        except Error as e:
            logger.error(f"Erro ao criar banco de dados: {e}")
            return False
    
    @staticmethod
    def table_exists(table_name: str) -> bool:
        """Verifica se uma tabela existe"""
        conn = None
        cursor = None
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = %s
            """, (table_name,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            logger.error(f"Erro ao verificar existência da tabela '{table_name}': {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    @staticmethod
    def all_tables_exist() -> bool:
        """Verifica se todas as tabelas necessárias existem"""
        required_tables = ['clientes', 'oportunidades', 'tarefas', 'interacoes', 'usuarios']
        for table in required_tables:
            if not Migrations.table_exists(table):
                return False
        return True
    
    @staticmethod
    def create_tables():
        """Cria todas as tabelas do sistema"""
        Migrations.create_database_if_not_exists()
        
        # Verificar se todas as tabelas já existem
        if Migrations.all_tables_exist():
            logger.info("Todas as tabelas já existem. Migrações não necessárias.")
            return True
        
        tables = {
            'clientes': """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    telefone VARCHAR(20),
                    empresa VARCHAR(255),
                    cnpj_cpf VARCHAR(18),
                    endereco_rua VARCHAR(255),
                    endereco_numero VARCHAR(20),
                    endereco_bairro VARCHAR(100),
                    endereco_cidade VARCHAR(100),
                    endereco_estado VARCHAR(2),
                    endereco_cep VARCHAR(10),
                    observacoes TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_nome (nome(191)),
                    INDEX idx_email (email(191)),
                    INDEX idx_empresa (empresa(191)),
                    INDEX idx_cidade (endereco_cidade)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'oportunidades': """
                CREATE TABLE IF NOT EXISTS oportunidades (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INT NOT NULL,
                    titulo VARCHAR(255) NOT NULL,
                    etapa ENUM('Lead', 'Qualificação', 'Proposta', 'Negociação', 'Fechado', 'Perdido') NOT NULL DEFAULT 'Lead',
                    valor DECIMAL(15, 2) DEFAULT 0.00,
                    probabilidade INT DEFAULT 0 CHECK (probabilidade >= 0 AND probabilidade <= 100),
                    data_prevista_fechamento DATE,
                    responsavel VARCHAR(255),
                    observacoes TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                    INDEX idx_cliente (cliente_id),
                    INDEX idx_etapa (etapa),
                    INDEX idx_data_fechamento (data_prevista_fechamento)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'tarefas': """
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INT NOT NULL,
                    descricao VARCHAR(500) NOT NULL,
                    tipo ENUM('Ligação', 'Email', 'Reunião', 'WhatsApp', 'Visita', 'Outro') DEFAULT 'Outro',
                    data_hora DATETIME NOT NULL,
                    status ENUM('Pendente', 'Concluída') DEFAULT 'Pendente',
                    prioridade ENUM('Baixa', 'Média', 'Alta') DEFAULT 'Média',
                    observacoes TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    concluida_em TIMESTAMP NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                    INDEX idx_cliente (cliente_id),
                    INDEX idx_data_hora (data_hora),
                    INDEX idx_status (status),
                    INDEX idx_prioridade (prioridade)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'interacoes': """
                CREATE TABLE IF NOT EXISTS interacoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INT NOT NULL,
                    tipo VARCHAR(50) NOT NULL,
                    descricao TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                    INDEX idx_cliente (cliente_id),
                    INDEX idx_tipo (tipo),
                    INDEX idx_criado_em (criado_em)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'usuarios': """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(191) UNIQUE NOT NULL,
                    senha_hash VARCHAR(255) NOT NULL,
                    nivel_acesso ENUM('Admin', 'Vendedor', 'Visualizador') DEFAULT 'Vendedor',
                    ativo TINYINT(1) DEFAULT 1,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        }
        
        conn = None
        cursor = None
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            tabelas_criadas = []
            tabelas_com_erro = []
            
            for table_name, create_sql in tables.items():
                try:
                    # Verificar se a tabela já existe antes de criar
                    if Migrations.table_exists(table_name):
                        logger.debug(f"Tabela '{table_name}' já existe, pulando criação")
                        tabelas_criadas.append(table_name)
                        continue
                    
                    cursor.execute(create_sql)
                    conn.commit()
                    logger.info(f"Tabela '{table_name}' criada com sucesso")
                    tabelas_criadas.append(table_name)
                except Error as e:
                    logger.error(f"Erro ao criar tabela '{table_name}': {e}")
                    tabelas_com_erro.append((table_name, str(e)))
                    conn.rollback()
                    # Continua tentando criar as outras tabelas
                    continue
            
            # Se houve erros, mas algumas tabelas foram criadas, avisar
            if tabelas_com_erro:
                logger.warning(f"Algumas tabelas tiveram erros: {tabelas_com_erro}")
                # Se nenhuma tabela foi criada, retornar False
                if not tabelas_criadas:
                    return False
            
            # Se chegou aqui e não houve erros críticos, está OK
            if not tabelas_com_erro:
                logger.info("Todas as tabelas foram criadas/verificadas com sucesso")
            else:
                logger.warning(f"Migrações concluídas com avisos. Tabelas criadas: {len(tabelas_criadas)}, Erros: {len(tabelas_com_erro)}")
            
            return True
            
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro ao criar tabelas: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    @staticmethod
    def run_migrations():
        """Executa todas as migrações (apenas se necessário)"""
        # Verificar se todas as tabelas já existem
        if Migrations.all_tables_exist():
            logger.info("Banco de dados já está configurado. Todas as tabelas existem.")
            return True
        
        logger.info("Iniciando migrações do banco de dados...")
        if Migrations.create_tables():
            logger.info("Migrações concluídas com sucesso")
            return True
        else:
            logger.error("Falha ao executar migrações")
            return False

