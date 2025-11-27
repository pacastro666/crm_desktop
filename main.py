"""
Ponto de entrada da aplicação CRM Desktop
"""
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from core.database import DatabaseManager
from core.migrations import Migrations
from core.settings import APP_NAME

# Importar repositories
from repositories.cliente_repository import ClienteRepository
from repositories.oportunidade_repository import OportunidadeRepository
from repositories.tarefa_repository import TarefaRepository
from repositories.interacao_repository import InteracaoRepository

# Importar services
from services.cliente_service import ClienteService
from services.oportunidade_service import OportunidadeService
from services.tarefa_service import TarefaService
from services.relatorio_service import RelatorioService

# Importar UI
from ui.main_window import MainWindow
from ui.views.dashboard_view import DashboardView
from ui.views.clientes_view import ClientesView
from ui.views.oportunidades_view import OportunidadesView
from ui.views.tarefas_view import TarefasView


def inicializar_banco():
    """Inicializa o banco de dados"""
    print("Conectando ao banco de dados...")
    
    # Criar pool de conexões
    if not DatabaseManager.create_connection_pool():
        print("ERRO: Não foi possível criar pool de conexões")
        return False
    
    # Testar conexão
    if not DatabaseManager.test_connection():
        print("ERRO: Não foi possível conectar ao banco de dados")
        print("Verifique as configurações em core/settings.py ou variáveis de ambiente:")
        print("  DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME")
        return False
    
    # Executar migrações (só se necessário)
    if not Migrations.run_migrations():
        print("ERRO: Falha ao executar migrações")
        return False
    
    print("Banco de dados pronto!")
    return True


def criar_services():
    """Cria e retorna os services"""
    # Repositories
    cliente_repo = ClienteRepository()
    oportunidade_repo = OportunidadeRepository()
    tarefa_repo = TarefaRepository()
    interacao_repo = InteracaoRepository()
    
    # Services
    cliente_service = ClienteService(cliente_repo, interacao_repo)
    oportunidade_service = OportunidadeService(oportunidade_repo, interacao_repo)
    tarefa_service = TarefaService(tarefa_repo, interacao_repo)
    relatorio_service = RelatorioService(cliente_repo, oportunidade_repo, tarefa_repo)
    
    return {
        'cliente_service': cliente_service,
        'oportunidade_service': oportunidade_service,
        'tarefa_service': tarefa_service,
        'relatorio_service': relatorio_service
    }


def main():
    """Função principal"""
    # Inicializar banco de dados
    if not inicializar_banco():
        print("\nERRO: Falha na inicialização do banco de dados")
        print("Certifique-se de que:")
        print("  1. O MySQL está instalado e rodando")
        print("  2. As credenciais estão corretas em core/settings.py")
        print("  3. O banco de dados existe ou pode ser criado")
        sys.exit(1)
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    # Criar services
    services = criar_services()
    
    # Criar janela principal
    window = MainWindow()
    
    # Criar e adicionar views
    dashboard_view = DashboardView(services['relatorio_service'])
    clientes_view = ClientesView(services['cliente_service'])
    oportunidades_view = OportunidadesView(services['oportunidade_service'], services['cliente_service'])
    tarefas_view = TarefasView(services['tarefa_service'], services['cliente_service'])
    
    window.adicionar_view(dashboard_view, "Dashboard")
    window.adicionar_view(clientes_view, "Clientes")
    window.adicionar_view(oportunidades_view, "Oportunidades")
    window.adicionar_view(tarefas_view, "Tarefas")
    
    # Conectar botões do menu
    window.btn_dashboard.clicked.connect(lambda: window.mostrar_view(0))
    window.btn_clientes.clicked.connect(lambda: window.mostrar_view(1))
    window.btn_oportunidades.clicked.connect(lambda: window.mostrar_view(2))
    window.btn_tarefas.clicked.connect(lambda: window.mostrar_view(3))
    
    # Mostrar janela
    window.show()
    
    # Executar aplicação
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

