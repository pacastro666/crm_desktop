"""
Formulário de cadastro/edição de oportunidade
"""
from typing import Tuple
from datetime import date, datetime
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QTextEdit, QComboBox, QPushButton,
                               QLabel, QGroupBox, QDateEdit, QDoubleSpinBox, QSpinBox)
from PySide6.QtCore import Qt, QDate
from models.oportunidade import Oportunidade
from services.oportunidade_service import OportunidadeService
from services.cliente_service import ClienteService
from utils.helpers import Helpers


class OportunidadeForm(QDialog):
    """Formulário para criar/editar oportunidade"""
    
    def __init__(self, oportunidade_service: OportunidadeService, 
                 cliente_service: ClienteService,
                 oportunidade: Oportunidade = None, parent=None):
        super().__init__(parent)
        self.oportunidade_service = oportunidade_service
        self.cliente_service = cliente_service
        self.oportunidade = oportunidade
        self.is_editing = oportunidade is not None
        
        self.setWindowTitle("Editar Oportunidade" if self.is_editing else "Nova Oportunidade")
        self.setMinimumWidth(600)
        self.setup_ui()
        
        if self.is_editing:
            self.preencher_formulario()
    
    def setup_ui(self):
        """Configura a interface do formulário"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título da oportunidade *")
        form_layout.addRow("Título *:", self.titulo_input)
        
        # Cliente
        self.cliente_combo = QComboBox()
        self.cliente_combo.setEditable(True)
        self.cliente_combo.setInsertPolicy(QComboBox.NoInsert)
        self._carregar_clientes()
        form_layout.addRow("Cliente *:", self.cliente_combo)
        
        # Etapa
        self.etapa_combo = QComboBox()
        self.etapa_combo.addItems(self.oportunidade_service.ETAPAS)
        form_layout.addRow("Etapa *:", self.etapa_combo)
        
        # Valor e Probabilidade
        valores_layout = QHBoxLayout()
        self.valor_input = QDoubleSpinBox()
        self.valor_input.setPrefix("R$ ")
        self.valor_input.setMaximum(999999999.99)
        self.valor_input.setDecimals(2)
        valores_layout.addWidget(self.valor_input)
        
        valores_layout.addWidget(QLabel("Probabilidade:"))
        self.probabilidade_input = QSpinBox()
        self.probabilidade_input.setSuffix("%")
        self.probabilidade_input.setRange(0, 100)
        self.probabilidade_input.setValue(0)
        valores_layout.addWidget(self.probabilidade_input)
        
        form_layout.addRow("Valor:", valores_layout)
        
        # Data prevista de fechamento
        self.data_fechamento_input = QDateEdit()
        self.data_fechamento_input.setCalendarPopup(True)
        self.data_fechamento_input.setDate(QDate.currentDate())
        form_layout.addRow("Data Prevista Fechamento:", self.data_fechamento_input)
        
        # Responsável
        self.responsavel_input = QLineEdit()
        self.responsavel_input.setPlaceholderText("Nome do responsável")
        form_layout.addRow("Responsável:", self.responsavel_input)
        
        # Observações
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setPlaceholderText("Observações sobre a oportunidade...")
        self.observacoes_input.setMaximumHeight(100)
        form_layout.addRow("Observações:", self.observacoes_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        buttons_layout.addWidget(self.btn_cancelar)
        
        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.setStyleSheet("""
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
        self.btn_salvar.clicked.connect(self.on_salvar_clicked)
        buttons_layout.addWidget(self.btn_salvar)
        
        layout.addLayout(buttons_layout)
    
    def _carregar_clientes(self):
        """Carrega clientes no combo"""
        clientes = self.cliente_service.listar_clientes()
        self.cliente_combo.clear()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente.nome, cliente.id)
    
    def preencher_formulario(self):
        """Preenche o formulário com dados da oportunidade"""
        if not self.oportunidade:
            return
        
        self.titulo_input.setText(self.oportunidade.titulo)
        
        # Cliente
        cliente_index = self.cliente_combo.findData(self.oportunidade.cliente_id)
        if cliente_index >= 0:
            self.cliente_combo.setCurrentIndex(cliente_index)
        
        # Etapa
        etapa_index = self.etapa_combo.findText(self.oportunidade.etapa)
        if etapa_index >= 0:
            self.etapa_combo.setCurrentIndex(etapa_index)
        
        self.valor_input.setValue(self.oportunidade.valor)
        self.probabilidade_input.setValue(self.oportunidade.probabilidade)
        
        if self.oportunidade.data_prevista_fechamento:
            qdate = QDate(
                self.oportunidade.data_prevista_fechamento.year,
                self.oportunidade.data_prevista_fechamento.month,
                self.oportunidade.data_prevista_fechamento.day
            )
            self.data_fechamento_input.setDate(qdate)
        
        self.responsavel_input.setText(self.oportunidade.responsavel)
        self.observacoes_input.setPlainText(self.oportunidade.observacoes)
    
    def validar_formulario(self) -> Tuple[bool, str]:
        """Valida os dados do formulário"""
        # Título obrigatório
        titulo = self.titulo_input.text().strip()
        if not titulo:
            return False, "Título é obrigatório"
        
        # Cliente obrigatório
        cliente_id = self.cliente_combo.currentData()
        if not cliente_id:
            return False, "Cliente é obrigatório"
        
        # Data não pode ser no passado
        data_fechamento = self.data_fechamento_input.date().toPython()
        if data_fechamento < date.today():
            return False, "Data prevista de fechamento não pode ser no passado"
        
        return True, ""
    
    def obter_oportunidade_do_formulario(self) -> Oportunidade:
        """Obtém os dados do formulário e retorna um objeto Oportunidade"""
        oportunidade = Oportunidade()
        
        if self.is_editing:
            oportunidade.id = self.oportunidade.id
        
        oportunidade.titulo = self.titulo_input.text().strip()
        oportunidade.cliente_id = self.cliente_combo.currentData()
        oportunidade.etapa = self.etapa_combo.currentText()
        oportunidade.valor = self.valor_input.value()
        oportunidade.probabilidade = self.probabilidade_input.value()
        
        qdate = self.data_fechamento_input.date()
        oportunidade.data_prevista_fechamento = date(qdate.year(), qdate.month(), qdate.day())
        
        oportunidade.responsavel = self.responsavel_input.text().strip()
        oportunidade.observacoes = self.observacoes_input.toPlainText().strip()
        
        return oportunidade
    
    def on_salvar_clicked(self):
        """Callback para salvar oportunidade"""
        # Validar
        valido, mensagem_erro = self.validar_formulario()
        if not valido:
            Helpers.mostrar_mensagem("Validação", mensagem_erro, 'warning', self)
            return
        
        # Obter dados
        oportunidade = self.obter_oportunidade_do_formulario()
        
        try:
            if self.is_editing:
                # Atualizar
                sucesso = self.oportunidade_service.atualizar_oportunidade(oportunidade)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Oportunidade atualizada com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao atualizar oportunidade", 'error', self)
            else:
                # Criar
                oportunidade_id = self.oportunidade_service.criar_oportunidade(oportunidade)
                if oportunidade_id:
                    Helpers.mostrar_mensagem("Sucesso", "Oportunidade cadastrada com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao cadastrar oportunidade", 'error', self)
        except ValueError as e:
            Helpers.mostrar_mensagem("Validação", str(e), 'warning', self)
        except Exception as e:
            Helpers.mostrar_mensagem("Erro", f"Erro ao salvar: {str(e)}", 'error', self)

