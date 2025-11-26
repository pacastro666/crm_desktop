# Sistema CRM Desktop

Sistema CRM (Customer Relationship Management) completo para desktop desenvolvido com PySide6 e MySQL.

## Características

- ✅ Gestão completa de clientes
- ✅ Gestão de oportunidades/vendas com funil
- ✅ Gestão de tarefas e follow-ups
- ✅ Histórico de interações
- ✅ Dashboard com métricas
- ✅ Relatórios e exportação CSV
- ✅ Interface moderna e intuitiva

## Requisitos

### Software Necessário

- **Python 3.10+**
- **MySQL 5.6 ou superior** (recomendado MySQL 5.7+ ou MariaDB 10.2+)
- **pip** (gerenciador de pacotes Python)

### Nota sobre Versão do MySQL

O sistema foi desenvolvido para funcionar com **MySQL 5.6 ou superior**. Se você tiver uma versão anterior, pode ser necessário ajustar algumas queries SQL. Recomendamos:

- **MySQL 5.7+** (recomendado)
- **MySQL 8.0+** (ideal)
- **MariaDB 10.2+** (alternativa compatível)

## Instalação

### 1. Clone ou baixe o projeto

```bash
cd "E:\sistemas\python crm"
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

Edite o arquivo `core/settings.py` ou configure as variáveis de ambiente:

```python
DB_CONFIG = {
    'host': 'localhost',      # Host do MySQL
    'port': 3306,              # Porta do MySQL
    'user': 'root',            # Usuário do MySQL
    'password': 'sua_senha',   # Senha do MySQL
    'database': 'crm_desktop', # Nome do banco de dados
}
```

Ou use variáveis de ambiente:

```bash
# Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="sua_senha"
$env:DB_NAME="crm_desktop"

# Linux/Mac
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=sua_senha
export DB_NAME=crm_desktop
```

### 6. Certifique-se de que o MySQL está rodando

O sistema criará automaticamente o banco de dados e as tabelas na primeira execução.

## Execução

```bash
python main.py
```

## Estrutura do Projeto

```
crm_desktop/
├── main.py                 # Ponto de entrada
├── core/                   # Módulo core
│   ├── database.py        # Gerenciamento de conexão MySQL
│   ├── settings.py        # Configurações
│   └── migrations.py      # Migrações do banco
├── models/                # Modelos de dados
├── repositories/          # Camada de acesso a dados
├── services/              # Regras de negócio
├── ui/                    # Interface gráfica
│   ├── main_window.py    # Janela principal
│   └── views/            # Telas do sistema
├── utils/                 # Utilitários
└── requirements.txt       # Dependências
```

## Funcionalidades

### Módulo de Clientes
- Cadastro completo de clientes
- Busca e filtros
- Edição e exclusão
- Visualização de detalhes
- Exportação CSV

### Módulo de Oportunidades
- Criação de oportunidades vinculadas a clientes
- Funil de vendas (Lead → Qualificação → Proposta → Negociação → Fechado/Perdido)
- Filtros por etapa, cliente, período
- Cálculo de valor em negociação

### Módulo de Tarefas
- Criação de tarefas vinculadas a clientes
- Tipos: Ligação, Email, Reunião, WhatsApp, Visita, Outro
- Prioridades: Baixa, Média, Alta
- Alertas de tarefas atrasadas
- Marcação de conclusão

### Dashboard
- Métricas principais
- Gráficos de oportunidades por etapa
- Lista de próximas tarefas
- Valor total em negociação

## Troubleshooting

### Erro de conexão com MySQL

1. Verifique se o MySQL está rodando:
   ```bash
   # Windows
   net start MySQL
   
   # Linux
   sudo systemctl status mysql
   ```

2. Verifique as credenciais em `core/settings.py`

3. Teste a conexão manualmente:
   ```python
   import mysql.connector
   conn = mysql.connector.connect(
       host='localhost',
       user='root',
       password='sua_senha'
   )
   ```

### Erro ao criar tabelas

Certifique-se de que o usuário MySQL tem permissões para criar bancos de dados e tabelas.

## Desenvolvimento

### Adicionar novas funcionalidades

1. Crie o model em `models/`
2. Crie o repository em `repositories/`
3. Crie o service em `services/`
4. Crie a view em `ui/views/`
5. Adicione a view na `main_window.py`

## Licença

Este projeto é de código aberto e está disponível para uso livre.

## Suporte

Para problemas ou dúvidas, verifique os logs do sistema ou entre em contato com o desenvolvedor.

