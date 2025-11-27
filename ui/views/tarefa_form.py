"""
Formulário de cadastro/edição de tarefa
"""
from typing import Tuple
from datetime import datetime, date
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QTextEdit, QComboBox, QPushButton,
                               QLabel, QDateEdit, QTimeEdit)
from PySide6.QtCore import Qt, QDate, QTime
from models.tarefa import Tarefa
from services.tarefa_service import TarefaService
from services.cliente_service import ClienteService
from utils.helpers import Helpers


class TarefaForm(QDialog):
    """Formulário para criar/editar tarefa"""
    
    def __init__(self, tarefa_service: TarefaService,
                 cliente_service: ClienteService,
                 tarefa: Tarefa = None, parent=None):
        super().__init__(parent)
        self.tarefa_service = tarefa_service
        self.cliente_service = cliente_service
        self.tarefa = tarefa
        self.is_editing = tarefa is not None
        
        self.setWindowTitle("Editar Tarefa" if self.is_editing else "Nova Tarefa")
        self.setMinimumWidth(550)
        self.setup_ui()
        
        if self.is_editing:
            self.preencher_formulario()
    
    def setup_ui(self):
        """Configura a interface do formulário"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # Descrição
        self.descricao_input = QLineEdit()
        self.descricao_input.setPlaceholderText("Descrição da tarefa *")
        form_layout.addRow("Descrição *:", self.descricao_input)
        
        # Cliente
        self.cliente_combo = QComboBox()
        self.cliente_combo.setEditable(True)
        self.cliente_combo.setInsertPolicy(QComboBox.NoInsert)
        self._carregar_clientes()
        form_layout.addRow("Cliente *:", self.cliente_combo)
        
        # Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(self.tarefa_service.TIPOS)
        form_layout.addRow("Tipo *:", self.tipo_combo)
        
        # Data e Hora
        data_hora_layout = QHBoxLayout()
        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        data_hora_layout.addWidget(self.data_input)
        
        data_hora_layout.addWidget(QLabel("Hora:"))
        self.hora_input = QTimeEdit()
        self.hora_input.setTime(QTime.currentTime())
        data_hora_layout.addWidget(self.hora_input)
        
        form_layout.addRow("Data *:", data_hora_layout)
        
        # Prioridade
        self.prioridade_combo = QComboBox()
        self.prioridade_combo.addItems(self.tarefa_service.PRIORIDADES)
        self.prioridade_combo.setCurrentText("Média")
        form_layout.addRow("Prioridade:", self.prioridade_combo)
        
        # Status (só se estiver editando)
        if self.is_editing:
            self.status_combo = QComboBox()
            self.status_combo.addItems(self.tarefa_service.STATUS)
            form_layout.addRow("Status:", self.status_combo)
        
        # Observações
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setPlaceholderText("Observações sobre a tarefa...")
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
        """Preenche o formulário com dados da tarefa"""
        if not self.tarefa:
            return
        
        self.descricao_input.setText(self.tarefa.descricao)
        
        # Cliente
        cliente_index = self.cliente_combo.findData(self.tarefa.cliente_id)
        if cliente_index >= 0:
            self.cliente_combo.setCurrentIndex(cliente_index)
        
        # Tipo
        tipo_index = self.tipo_combo.findText(self.tarefa.tipo)
        if tipo_index >= 0:
            self.tipo_combo.setCurrentIndex(tipo_index)
        
        # Data e Hora
        if self.tarefa.data_hora:
            qdate = QDate(
                self.tarefa.data_hora.year,
                self.tarefa.data_hora.month,
                self.tarefa.data_hora.day
            )
            self.data_input.setDate(qdate)
            
            qtime = QTime(
                self.tarefa.data_hora.hour,
                self.tarefa.data_hora.minute
            )
            self.hora_input.setTime(qtime)
        
        # Prioridade
        prioridade_index = self.prioridade_combo.findText(self.tarefa.prioridade)
        if prioridade_index >= 0:
            self.prioridade_combo.setCurrentIndex(prioridade_index)
        
        # Status
        if self.is_editing and hasattr(self, 'status_combo'):
            status_index = self.status_combo.findText(self.tarefa.status)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
        
        self.observacoes_input.setPlainText(self.tarefa.observacoes)
    
    def validar_formulario(self) -> Tuple[bool, str]:
        """Valida os dados do formulário"""
        # Descrição obrigatória
        descricao = self.descricao_input.text().strip()
        if not descricao:
            return False, "Descrição é obrigatória"
        
        # Cliente obrigatório
        cliente_id = self.cliente_combo.currentData()
        if not cliente_id:
            return False, "Cliente é obrigatório"
        
        return True, ""
    
    def obter_tarefa_do_formulario(self) -> Tarefa:
        """Obtém os dados do formulário e retorna um objeto Tarefa"""
        tarefa = Tarefa()
        
        if self.is_editing:
            tarefa.id = self.tarefa.id
        
        tarefa.descricao = self.descricao_input.text().strip()
        tarefa.cliente_id = self.cliente_combo.currentData()
        tarefa.tipo = self.tipo_combo.currentText()
        
        # Combinar data e hora
        qdate = self.data_input.date()
        qtime = self.hora_input.time()
        from PySide6.QtCore import QTime
        # Converter QTime para time do Python
        if isinstance(qtime, QTime):
            from datetime import time
            py_time = time(qtime.hour(), qtime.minute(), qtime.second())
        else:
            py_time = qtime
        
        tarefa.data_hora = datetime.combine(
            date(qdate.year(), qdate.month(), qdate.day()),
            py_time
        )
        
        tarefa.prioridade = self.prioridade_combo.currentText()
        
        if self.is_editing and hasattr(self, 'status_combo'):
            tarefa.status = self.status_combo.currentText()
        else:
            tarefa.status = "Pendente"
        
        tarefa.observacoes = self.observacoes_input.toPlainText().strip()
        
        return tarefa
    
    def on_salvar_clicked(self):
        """Callback para salvar tarefa"""
        # Validar
        valido, mensagem_erro = self.validar_formulario()
        if not valido:
            Helpers.mostrar_mensagem("Validação", mensagem_erro, 'warning', self)
            return
        
        # Obter dados
        tarefa = self.obter_tarefa_do_formulario()
        
        try:
            if self.is_editing:
                # Atualizar
                sucesso = self.tarefa_service.atualizar_tarefa(tarefa)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Tarefa atualizada com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao atualizar tarefa", 'error', self)
            else:
                # Criar
                tarefa_id = self.tarefa_service.criar_tarefa(tarefa)
                if tarefa_id:
                    Helpers.mostrar_mensagem("Sucesso", "Tarefa cadastrada com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao cadastrar tarefa", 'error', self)
        except ValueError as e:
            Helpers.mostrar_mensagem("Validação", str(e), 'warning', self)
        except Exception as e:
            Helpers.mostrar_mensagem("Erro", f"Erro ao salvar: {str(e)}", 'error', self)

