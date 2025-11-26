"""
Configurações globais do sistema CRM
"""
import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações do banco de dados MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '4362106'),
    'database': os.getenv('DB_NAME', 'crm_desktop'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False
}

# Configurações da aplicação
APP_NAME = "CRM Desktop"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Sistema CRM"

# Caminhos de recursos
RESOURCES_DIR = BASE_DIR / 'resources'
ICONS_DIR = RESOURCES_DIR / 'icons'
STYLES_DIR = RESOURCES_DIR / 'styles'
DATABASE_DIR = RESOURCES_DIR / 'database'

# Criar diretórios se não existirem
for directory in [RESOURCES_DIR, ICONS_DIR, STYLES_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

