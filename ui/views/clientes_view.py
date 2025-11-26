"""
View de listagem de clientes
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLineEdit, QTableView, QLabel, QHeaderView)
from PySide6.QtCore import Qt, QAbstractTableModel
from services.cliente_service import ClienteService
from models.cliente import Cliente
from utils.formatters import Formatters


class ClientesTableModel(QAbstractTableModel):
    """Model para tabela de clientes"""
    
    def __init__(self, clientes: list):
        super().__init__()
        self.clientes = clientes
        self.headers = ['ID', 'Nome', 'Email', 'Telefone', 'Empresa', 'Cidade', 'Data Cadastro']
    
    def rowCount(self, parent=None):
        return len(self.clientes)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            cliente = self.clientes[index.row()]
            col = index.column()
            
            if col == 0:
                return cliente.id
            elif col == 1:
                return cliente.nome
            elif col == 2:
                return cliente.email
            elif col == 3:
                return Formatters.formatar_telefone(cliente.telefone)
            elif col == 4:
                return cliente.empresa
            elif col == 5:
                return cliente.endereco_cidade
            elif col == 6:
                return Formatters.formatar_data(cliente.criado_em) if cliente.criado_em else ""
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class ClientesView(QWidget):
    """Tela de listagem de clientes"""
    
    def __init__(self, cliente_service: ClienteService):
        super().__init__()
        self.cliente_service = cliente_service
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Barra superior com busca e botões
        top_layout = QHBoxLayout()
        
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("Buscar por nome, email, empresa ou cidade...")
        self.busca_input.setFixedWidth(400)
        self.busca_input.textChanged.connect(self.on_busca_changed)
        top_layout.addWidget(self.busca_input)
        
        top_layout.addStretch()
        
        self.btn_exportar = QPushButton("📥 Exportar CSV")
        self.btn_exportar.clicked.connect(self.on_exportar_clicked)
        top_layout.addWidget(self.btn_exportar)
        
        self.btn_novo = QPushButton("➕ Novo Cliente")
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
        self.btn_novo.clicked.connect(self.on_novo_cliente_clicked)
        top_layout.addWidget(self.btn_novo)
        
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
        layout.addWidget(self.tabela)
        
        # Barra inferior com ações
        bottom_layout = QHBoxLayout()
        
        self.label_total = QLabel("Total: 0")
        bottom_layout.addWidget(self.label_total)
        
        bottom_layout.addStretch()
        
        self.btn_ver = QPushButton("👁 Ver Detalhes")
        self.btn_ver.clicked.connect(self.on_ver_clicked)
        bottom_layout.addWidget(self.btn_ver)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.on_editar_clicked)
        bottom_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton("🗑 Excluir")
        self.btn_excluir.setStyleSheet("background-color: #ef4444; color: white; padding: 8px 15px; border-radius: 6px;")
        self.btn_excluir.clicked.connect(self.on_excluir_clicked)
        bottom_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(bottom_layout)
    
    def carregar_dados(self, termo_busca: str = ""):
        """Carrega os clientes na tabela"""
        if termo_busca:
            clientes = self.cliente_service.buscar_clientes(termo_busca)
        else:
            clientes = self.cliente_service.listar_clientes()
        
        model = ClientesTableModel(clientes)
        self.tabela.setModel(model)
        self.label_total.setText(f"Total: {len(clientes)}")
    
    def on_busca_changed(self, texto: str):
        """Callback quando o texto de busca muda"""
        self.carregar_dados(texto)
    
    def on_novo_cliente_clicked(self):
        """Callback para novo cliente"""
        # Será implementado com o formulário
        pass
    
    def on_exportar_clicked(self):
        """Callback para exportar"""
        # Será implementado
        pass
    
    def on_ver_clicked(self):
        """Callback para ver detalhes"""
        # Será implementado
        pass
    
    def on_editar_clicked(self):
        """Callback para editar"""
        # Será implementado
        pass
    
    def on_excluir_clicked(self):
        """Callback para excluir"""
        # Será implementado
        pass

