# Configuração do MySQL para o Sistema CRM

## Requisitos de Versão

O sistema foi desenvolvido para funcionar com **MySQL 5.6 ou superior**. 

### Versões Recomendadas:
- **MySQL 5.7+** (recomendado)
- **MySQL 8.0+** (ideal - melhor performance)
- **MariaDB 10.2+** (alternativa compatível)

### Versões Mínimas:
- **MySQL 5.6** (funcional, mas algumas features podem não estar disponíveis)
- **MariaDB 10.1+**

## Instalação do MySQL

### Windows

1. Baixe o MySQL Installer de: https://dev.mysql.com/downloads/installer/
2. Execute o instalador e escolha "Developer Default" ou "Server only"
3. Durante a instalação, anote a senha do usuário root
4. Certifique-se de que o serviço MySQL está rodando:
   ```powershell
   net start MySQL
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```

### Linux (CentOS/RHEL)

```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
sudo mysql_secure_installation
```

### macOS

```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

## Configuração do Banco de Dados

### 1. Conectar ao MySQL

```bash
mysql -u root -p
```

### 2. Criar Usuário (Opcional, mas recomendado)

```sql
CREATE USER 'crm_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON crm_desktop.* TO 'crm_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configurar o Sistema CRM

Edite o arquivo `core/settings.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'crm_user',  # ou 'root'
    'password': 'senha_segura',
    'database': 'crm_desktop',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
}
```

Ou use variáveis de ambiente (recomendado para produção):

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=crm_user
export DB_PASSWORD=senha_segura
export DB_NAME=crm_desktop
```

## Verificação da Instalação

### Verificar Versão do MySQL

```sql
SELECT VERSION();
```

### Verificar se o MySQL está rodando

**Windows:**
```powershell
Get-Service MySQL
```

**Linux:**
```bash
sudo systemctl status mysql
```

**macOS:**
```bash
brew services list | grep mysql
```

### Testar Conexão

O sistema testará automaticamente a conexão na primeira execução. Se houver problemas, você verá mensagens de erro detalhadas.

## Solução de Problemas

### Erro: "Can't connect to MySQL server"

1. Verifique se o MySQL está rodando
2. Verifique se a porta está correta (padrão: 3306)
3. Verifique se o firewall não está bloqueando a conexão

### Erro: "Access denied for user"

1. Verifique o usuário e senha em `core/settings.py`
2. Verifique se o usuário tem permissões:
   ```sql
   SHOW GRANTS FOR 'crm_user'@'localhost';
   ```

### Erro: "Unknown database"

O sistema criará o banco automaticamente. Se isso falhar, crie manualmente:

```sql
CREATE DATABASE crm_desktop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Erro: "Table doesn't exist"

Execute as migrações manualmente ou verifique o arquivo `core/migrations.py`.

## Performance

Para melhor performance, considere ajustar as seguintes configurações no `my.cnf` ou `my.ini`:

```ini
[mysqld]
innodb_buffer_pool_size = 256M
max_connections = 200
query_cache_size = 64M
```

## Backup

Para fazer backup do banco de dados:

```bash
mysqldump -u crm_user -p crm_desktop > backup_$(date +%Y%m%d).sql
```

Para restaurar:

```bash
mysql -u crm_user -p crm_desktop < backup_20231126.sql
```

## Segurança

1. **Nunca** use o usuário root em produção
2. Use senhas fortes
3. Limite o acesso do usuário apenas ao banco necessário
4. Considere usar SSL para conexões remotas
5. Mantenha o MySQL atualizado

