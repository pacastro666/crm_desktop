"""
View de listagem de tarefas
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLineEdit, QTableView, QLabel, QHeaderView, 
                               QComboBox, QDialog, QFileDialog, QCheckBox)
from PySide6.QtCore import Qt, QAbstractTableModel
from datetime import datetime, date
from services.tarefa_service import TarefaService
from services.cliente_service import ClienteService
from models.tarefa import Tarefa
from utils.formatters import Formatters
from utils.helpers import Helpers
from ui.views.tarefa_form import TarefaForm
from services.export_service import ExportService


class TarefasTableModel(QAbstractTableModel):
    """Model para tabela de tarefas"""
    
    def __init__(self, tarefas: list, cliente_service: ClienteService):
        super().__init__()
        self.tarefas = tarefas
        self.cliente_service = cliente_service
        self.headers = ['✓', 'Descrição', 'Cliente', 'Tipo', 'Data/Hora', 'Prioridade', 'Status']
    
    def rowCount(self, parent=None):
        return len(self.tarefas)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        tarefa = self.tarefas[index.row()]
        col = index.column()
        
        if col == 0:  # Checkbox
            if role == Qt.CheckStateRole:
                return Qt.Checked if tarefa.status == 'Concluída' else Qt.Unchecked
            elif role == Qt.DisplayRole:
                return ""
        elif role == Qt.DisplayRole:
            if col == 1:
                return tarefa.descricao
            elif col == 2:
                # Buscar nome do cliente
                cliente = self.cliente_service.buscar_cliente(tarefa.cliente_id)
                return cliente.nome if cliente else f"ID: {tarefa.cliente_id}"
            elif col == 3:
                return tarefa.tipo
            elif col == 4:
                return Formatters.formatar_data_hora(tarefa.data_hora) if tarefa.data_hora else ""
            elif col == 5:
                return tarefa.prioridade
            elif col == 6:
                return tarefa.status
        
        # Cores por prioridade
        if role == Qt.BackgroundRole:
            if col == 5:  # Coluna de prioridade
                if tarefa.prioridade == 'Alta':
                    return Qt.red
                elif tarefa.prioridade == 'Média':
                    return Qt.yellow
                elif tarefa.prioridade == 'Baixa':
                    return Qt.green
        
        # Tarefas atrasadas
        if role == Qt.ForegroundRole:
            if tarefa.status == 'Pendente' and tarefa.data_hora:
                if tarefa.data_hora < datetime.now():
                    return Qt.red
        
        return None
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 0:  # Checkbox
            flags |= Qt.ItemIsUserCheckable
        return flags
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.column() == 0 and role == Qt.CheckStateRole:
            # Não altera aqui, será tratado na view
            return True
        return False
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class TarefasView(QWidget):
    """Tela de listagem de tarefas"""
    
    def __init__(self, tarefa_service: TarefaService, cliente_service: ClienteService):
        super().__init__()
        self.tarefa_service = tarefa_service
        self.cliente_service = cliente_service
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Barra superior com filtros e botões
        top_layout = QVBoxLayout()
        
        # Filtros
        filtros_layout = QHBoxLayout()
        
        filtros_layout.addWidget(QLabel("Filtros:"))
        
        self.filtro_data = QComboBox()
        self.filtro_data.addItems(["Todas", "Hoje", "Esta Semana", "Atrasadas"])
        self.filtro_data.currentIndexChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("Data:"))
        filtros_layout.addWidget(self.filtro_data)
        
        self.filtro_status = QComboBox()
        self.filtro_status.addItem("Todos", "")
        self.filtro_status.addItem("Pendentes", "Pendente")
        self.filtro_status.addItem("Concluídas", "Concluída")
        self.filtro_status.currentIndexChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("Status:"))
        filtros_layout.addWidget(self.filtro_status)
        
        self.filtro_prioridade = QComboBox()
        self.filtro_prioridade.addItem("Todas", "")
        for prioridade in self.tarefa_service.PRIORIDADES:
            self.filtro_prioridade.addItem(prioridade, prioridade)
        self.filtro_prioridade.currentIndexChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("Prioridade:"))
        filtros_layout.addWidget(self.filtro_prioridade)
        
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("Buscar por descrição...")
        self.busca_input.setFixedWidth(250)
        self.busca_input.textChanged.connect(self.on_busca_changed)
        filtros_layout.addWidget(self.busca_input)
        
        filtros_layout.addStretch()
        
        self.btn_novo = QPushButton("➕ Nova Tarefa")
        self.btn_novo.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        self.btn_novo.clicked.connect(self.on_nova_tarefa_clicked)
        filtros_layout.addWidget(self.btn_novo)
        
        top_layout.addLayout(filtros_layout)
        layout.addLayout(top_layout)
        
        # Tabela
        self.tabela = QTableView()
        self.tabela.setSelectionBehavior(QTableView.SelectRows)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setStyleSheet("""
            QTableView {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
            QTableView::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
            }
        """)
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabela.clicked.connect(self.on_tabela_clicked)
        layout.addWidget(self.tabela)
        
        # Barra inferior com ações
        bottom_layout = QHBoxLayout()
        
        self.label_total = QLabel("Total: 0")
        bottom_layout.addWidget(self.label_total)
        
        bottom_layout.addStretch()
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.on_editar_clicked)
        bottom_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton("🗑 Excluir")
        self.btn_excluir.setStyleSheet("background-color: #ef4444; color: white; padding: 8px 15px; border-radius: 6px;")
        self.btn_excluir.clicked.connect(self.on_excluir_clicked)
        bottom_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(bottom_layout)
    
    def carregar_dados(self, termo_busca: str = "", filtro_data: str = "", 
                       filtro_status: str = "", filtro_prioridade: str = ""):
        """Carrega as tarefas na tabela"""
        if filtro_data == "Hoje":
            tarefas = self.tarefa_service.buscar_pendentes_hoje()
        elif filtro_data == "Atrasadas":
            tarefas = self.tarefa_service.buscar_atrasadas()
        elif filtro_status:
            tarefas = self.tarefa_service.buscar_por_status(filtro_status)
        else:
            tarefas = self.tarefa_service.listar_tarefas()
        
        # Filtrar por busca
        if termo_busca:
            termo_lower = termo_busca.lower()
            tarefas = [t for t in tarefas if termo_lower in t.descricao.lower()]
        
        # Filtrar por prioridade
        if filtro_prioridade:
            tarefas = [t for t in tarefas if t.prioridade == filtro_prioridade]
        
        model = TarefasTableModel(tarefas, self.cliente_service)
        self.tabela.setModel(model)
        self.label_total.setText(f"Total: {len(tarefas)}")
    
    def on_busca_changed(self, texto: str):
        """Callback quando o texto de busca muda"""
        self._aplicar_filtros()
    
    def on_filtro_changed(self):
        """Callback quando algum filtro muda"""
        self._aplicar_filtros()
    
    def _aplicar_filtros(self):
        """Aplica todos os filtros"""
        filtro_data = self.filtro_data.currentText()
        filtro_status = self.filtro_status.currentData()
        filtro_prioridade = self.filtro_prioridade.currentData()
        texto = self.busca_input.text()
        self.carregar_dados(texto, filtro_data, filtro_status, filtro_prioridade)
    
    def on_tabela_clicked(self, index):
        """Callback quando clica na tabela (para checkbox)"""
        if index.column() == 0:  # Coluna do checkbox
            model = self.tabela.model()
            tarefa = model.tarefas[index.row()]
            
            if tarefa.status == 'Pendente':
                # Marcar como concluída
                try:
                    sucesso = self.tarefa_service.marcar_concluida(tarefa.id)
                    if sucesso:
                        self.carregar_dados()  # Recarregar
                except Exception as e:
                    Helpers.mostrar_mensagem("Erro", f"Erro: {str(e)}", 'error', self)
    
    def on_nova_tarefa_clicked(self):
        """Callback para nova tarefa"""
        form = TarefaForm(self.tarefa_service, self.cliente_service, parent=self)
        if form.exec() == QDialog.Accepted:
            self.carregar_dados()
    
    def _obter_tarefa_selecionada(self) -> Tarefa:
        """Obtém a tarefa selecionada na tabela"""
        indexes = self.tabela.selectionModel().selectedRows()
        if not indexes:
            return None
        
        row = indexes[0].row()
        model = self.tabela.model()
        tarefa = model.tarefas[row]
        return self.tarefa_service.buscar_tarefa(tarefa.id)
    
    def on_editar_clicked(self):
        """Callback para editar"""
        tarefa = self._obter_tarefa_selecionada()
        if not tarefa:
            Helpers.mostrar_mensagem("Aviso", "Selecione uma tarefa para editar", 'warning', self)
            return
        
        form = TarefaForm(self.tarefa_service, self.cliente_service, tarefa, parent=self)
        if form.exec() == QDialog.Accepted:
            self.carregar_dados()
    
    def on_excluir_clicked(self):
        """Callback para excluir"""
        tarefa = self._obter_tarefa_selecionada()
        if not tarefa:
            Helpers.mostrar_mensagem("Aviso", "Selecione uma tarefa para excluir", 'warning', self)
            return
        
        if Helpers.confirmar_acao(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a tarefa '{tarefa.descricao}'?\n\nEsta ação não pode ser desfeita.",
            self
        ):
            try:
                sucesso = self.tarefa_service.excluir_tarefa(tarefa.id)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Tarefa excluída com sucesso", 'info', self)
                    self.carregar_dados()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao excluir tarefa", 'error', self)
            except Exception as e:
                Helpers.mostrar_mensagem("Erro", f"Erro ao excluir: {str(e)}", 'error', self)

