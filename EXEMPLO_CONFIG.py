"""
Arquivo de exemplo de configuração
Copie este arquivo e ajuste conforme necessário
Ou use variáveis de ambiente
"""

# Exemplo de configuração do banco de dados
# Você pode editar core/settings.py diretamente ou usar variáveis de ambiente

# Configuração usando variáveis de ambiente (recomendado):
# 
# Windows PowerShell:
# $env:DB_HOST="localhost"
# $env:DB_PORT="3306"
# $env:DB_USER="root"
# $env:DB_PASSWORD="sua_senha_aqui"
# $env:DB_NAME="crm_desktop"
#
# Linux/Mac:
# export DB_HOST=localhost
# export DB_PORT=3306
# export DB_USER=root
# export DB_PASSWORD=sua_senha_aqui
# export DB_NAME=crm_desktop

# Exemplo de configuração para MySQL local:
DB_CONFIG_EXEMPLO = {
    'host': 'localhost',        # Host do MySQL
    'port': 3306,               # Porta padrão do MySQL
    'user': 'root',             # Usuário do MySQL
    'password': 'sua_senha',    # Senha do MySQL
    'database': 'crm_desktop',  # Nome do banco (será criado automaticamente)
}

# Exemplo de configuração para MySQL remoto:
DB_CONFIG_REMOTO_EXEMPLO = {
    'host': '192.168.1.100',    # IP do servidor MySQL
    'port': 3306,
    'user': 'crm_user',
    'password': 'senha_segura',
    'database': 'crm_desktop',
}

# Para usar estas configurações, edite o arquivo core/settings.py
# ou defina as variáveis de ambiente antes de executar o sistema

