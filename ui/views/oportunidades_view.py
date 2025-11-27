"""
View de listagem de oportunidades
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLineEdit, QTableView, QLabel, QHeaderView, 
                               QComboBox, QDialog, QFileDialog)
from PySide6.QtCore import Qt, QAbstractTableModel, QDate
from datetime import date
from services.oportunidade_service import OportunidadeService
from services.cliente_service import ClienteService
from models.oportunidade import Oportunidade
from utils.formatters import Formatters
from utils.helpers import Helpers
from ui.views.oportunidade_form import OportunidadeForm
from services.export_service import ExportService


class OportunidadesTableModel(QAbstractTableModel):
    """Model para tabela de oportunidades"""
    
    def __init__(self, oportunidades: list, cliente_service: ClienteService):
        super().__init__()
        self.oportunidades = oportunidades
        self.cliente_service = cliente_service
        self.headers = ['ID', 'Título', 'Cliente', 'Etapa', 'Valor', 'Probabilidade', 'Data Prevista', 'Responsável']
    
    def rowCount(self, parent=None):
        return len(self.oportunidades)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            oportunidade = self.oportunidades[index.row()]
            col = index.column()
            
            if col == 0:
                return oportunidade.id
            elif col == 1:
                return oportunidade.titulo
            elif col == 2:
                # Buscar nome do cliente
                cliente = self.cliente_service.buscar_cliente(oportunidade.cliente_id)
                return cliente.nome if cliente else f"ID: {oportunidade.cliente_id}"
            elif col == 3:
                return oportunidade.etapa
            elif col == 4:
                return Formatters.formatar_moeda(oportunidade.valor)
            elif col == 5:
                return f"{oportunidade.probabilidade}%"
            elif col == 6:
                return Formatters.formatar_data(oportunidade.data_prevista_fechamento) if oportunidade.data_prevista_fechamento else ""
            elif col == 7:
                return oportunidade.responsavel
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class OportunidadesView(QWidget):
    """Tela de listagem de oportunidades"""
    
    def __init__(self, oportunidade_service: OportunidadeService, cliente_service: ClienteService):
        super().__init__()
        self.oportunidade_service = oportunidade_service
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
        
        self.filtro_etapa = QComboBox()
        self.filtro_etapa.addItem("Todas as etapas", "")
        for etapa in self.oportunidade_service.ETAPAS:
            self.filtro_etapa.addItem(etapa, etapa)
        self.filtro_etapa.currentIndexChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("Etapa:"))
        filtros_layout.addWidget(self.filtro_etapa)
        
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("Buscar por título ou cliente...")
        self.busca_input.setFixedWidth(300)
        self.busca_input.textChanged.connect(self.on_busca_changed)
        filtros_layout.addWidget(self.busca_input)
        
        filtros_layout.addStretch()
        
        self.btn_exportar = QPushButton("📥 Exportar CSV")
        self.btn_exportar.clicked.connect(self.on_exportar_clicked)
        filtros_layout.addWidget(self.btn_exportar)
        
        self.btn_novo = QPushButton("➕ Nova Oportunidade")
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
        self.btn_novo.clicked.connect(self.on_nova_oportunidade_clicked)
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
        layout.addWidget(self.tabela)
        
        # Barra inferior com ações
        bottom_layout = QHBoxLayout()
        
        self.label_total = QLabel("Total: 0")
        bottom_layout.addWidget(self.label_total)
        
        bottom_layout.addStretch()
        
        self.btn_mover_etapa = QPushButton("➡️ Mover Etapa")
        self.btn_mover_etapa.clicked.connect(self.on_mover_etapa_clicked)
        bottom_layout.addWidget(self.btn_mover_etapa)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.on_editar_clicked)
        bottom_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton("🗑 Excluir")
        self.btn_excluir.setStyleSheet("background-color: #ef4444; color: white; padding: 8px 15px; border-radius: 6px;")
        self.btn_excluir.clicked.connect(self.on_excluir_clicked)
        bottom_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(bottom_layout)
    
    def carregar_dados(self, termo_busca: str = "", etapa: str = ""):
        """Carrega as oportunidades na tabela"""
        if etapa:
            oportunidades = self.oportunidade_service.buscar_por_etapa(etapa)
        else:
            oportunidades = self.oportunidade_service.listar_oportunidades()
        
        # Filtrar por busca se houver termo
        if termo_busca:
            termo_lower = termo_busca.lower()
            oportunidades = [
                op for op in oportunidades
                if termo_lower in op.titulo.lower() or 
                (op.responsavel and termo_lower in op.responsavel.lower())
            ]
        
        model = OportunidadesTableModel(oportunidades, self.cliente_service)
        self.tabela.setModel(model)
        self.label_total.setText(f"Total: {len(oportunidades)}")
    
    def on_busca_changed(self, texto: str):
        """Callback quando o texto de busca muda"""
        etapa = self.filtro_etapa.currentData()
        self.carregar_dados(texto, etapa)
    
    def on_filtro_changed(self):
        """Callback quando o filtro de etapa muda"""
        etapa = self.filtro_etapa.currentData()
        texto = self.busca_input.text()
        self.carregar_dados(texto, etapa)
    
    def on_nova_oportunidade_clicked(self):
        """Callback para nova oportunidade"""
        form = OportunidadeForm(self.oportunidade_service, self.cliente_service, parent=self)
        if form.exec() == QDialog.Accepted:
            self.carregar_dados()
    
    def on_exportar_clicked(self):
        """Callback para exportar"""
        oportunidades = self.oportunidade_service.listar_oportunidades()
        
        if not oportunidades:
            Helpers.mostrar_mensagem("Aviso", "Não há oportunidades para exportar", 'warning', self)
            return
        
        arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Oportunidades",
            ExportService.gerar_nome_arquivo_export("oportunidades"),
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if arquivo:
            sucesso = ExportService.exportar_oportunidades_csv(oportunidades, arquivo)
            if sucesso:
                Helpers.mostrar_mensagem("Sucesso", f"Oportunidades exportadas para:\n{arquivo}", 'info', self)
            else:
                Helpers.mostrar_mensagem("Erro", "Erro ao exportar oportunidades", 'error', self)
    
    def _obter_oportunidade_selecionada(self) -> Oportunidade:
        """Obtém a oportunidade selecionada na tabela"""
        indexes = self.tabela.selectionModel().selectedRows()
        if not indexes:
            return None
        
        row = indexes[0].row()
        model = self.tabela.model()
        oportunidade_id = model.data(model.index(row, 0), Qt.DisplayRole)
        return self.oportunidade_service.buscar_oportunidade(oportunidade_id)
    
    def on_mover_etapa_clicked(self):
        """Callback para mover etapa"""
        oportunidade = self._obter_oportunidade_selecionada()
        if not oportunidade:
            Helpers.mostrar_mensagem("Aviso", "Selecione uma oportunidade", 'warning', self)
            return
        
        # Diálogo simples para escolher nova etapa
        from PySide6.QtWidgets import QInputDialog
        etapas = self.oportunidade_service.ETAPAS
        etapa_atual_index = etapas.index(oportunidade.etapa) if oportunidade.etapa in etapas else 0
        
        nova_etapa, ok = QInputDialog.getItem(
            self,
            "Mover Etapa",
            f"Selecione a nova etapa para '{oportunidade.titulo}':",
            etapas,
            etapa_atual_index,
            False
        )
        
        if ok and nova_etapa:
            try:
                sucesso = self.oportunidade_service.mover_etapa(oportunidade.id, nova_etapa)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Etapa atualizada com sucesso", 'info', self)
                    self.carregar_dados()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao atualizar etapa", 'error', self)
            except Exception as e:
                Helpers.mostrar_mensagem("Erro", f"Erro: {str(e)}", 'error', self)
    
    def on_editar_clicked(self):
        """Callback para editar"""
        oportunidade = self._obter_oportunidade_selecionada()
        if not oportunidade:
            Helpers.mostrar_mensagem("Aviso", "Selecione uma oportunidade para editar", 'warning', self)
            return
        
        form = OportunidadeForm(self.oportunidade_service, self.cliente_service, oportunidade, parent=self)
        if form.exec() == QDialog.Accepted:
            self.carregar_dados()
    
    def on_excluir_clicked(self):
        """Callback para excluir"""
        oportunidade = self._obter_oportunidade_selecionada()
        if not oportunidade:
            Helpers.mostrar_mensagem("Aviso", "Selecione uma oportunidade para excluir", 'warning', self)
            return
        
        if Helpers.confirmar_acao(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a oportunidade '{oportunidade.titulo}'?\n\nEsta ação não pode ser desfeita.",
            self
        ):
            try:
                sucesso = self.oportunidade_service.excluir_oportunidade(oportunidade.id)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Oportunidade excluída com sucesso", 'info', self)
                    self.carregar_dados()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao excluir oportunidade", 'error', self)
            except Exception as e:
                Helpers.mostrar_mensagem("Erro", f"Erro ao excluir: {str(e)}", 'error', self)

