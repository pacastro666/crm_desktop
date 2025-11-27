"""
Formulário de cadastro/edição de cliente
"""
from typing import Tuple
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QTextEdit, QComboBox, QPushButton,
                               QLabel, QGroupBox, QMessageBox, QWidget, QScrollArea)
from PySide6.QtCore import Qt
from models.cliente import Cliente
from services.cliente_service import ClienteService
from utils.validators import Validators
from utils.formatters import Formatters
from utils.helpers import Helpers


class ClienteForm(QDialog):
    """Formulário para criar/editar cliente"""
    
    def __init__(self, cliente_service: ClienteService, cliente: Cliente = None, parent=None):
        super().__init__(parent)
        self.cliente_service = cliente_service
        self.cliente = cliente
        self.is_editing = cliente is not None
        
        self.setWindowTitle("Editar Cliente" if self.is_editing else "Novo Cliente")
        self.setMinimumWidth(600)
        self.setup_ui()
        
        if self.is_editing:
            self.preencher_formulario()
    
    def setup_ui(self):
        """Configura a interface do formulário"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Scroll area para formulário longo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Dados básicos
        grupo_basico = QGroupBox("Dados Básicos")
        form_basico = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome completo *")
        form_basico.addRow("Nome *:", self.nome_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@exemplo.com")
        form_basico.addRow("Email:", self.email_input)
        
        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("(00) 00000-0000")
        form_basico.addRow("Telefone:", self.telefone_input)
        
        self.empresa_input = QLineEdit()
        self.empresa_input.setPlaceholderText("Nome da empresa")
        form_basico.addRow("Empresa:", self.empresa_input)
        
        self.cnpj_cpf_input = QLineEdit()
        self.cnpj_cpf_input.setPlaceholderText("000.000.000-00 ou 00.000.000/0000-00")
        form_basico.addRow("CNPJ/CPF:", self.cnpj_cpf_input)
        
        grupo_basico.setLayout(form_basico)
        form_layout.addWidget(grupo_basico)
        
        # Endereço
        grupo_endereco = QGroupBox("Endereço")
        form_endereco = QFormLayout()
        
        self.rua_input = QLineEdit()
        self.rua_input.setPlaceholderText("Nome da rua")
        form_endereco.addRow("Rua:", self.rua_input)
        
        endereco_numero_layout = QHBoxLayout()
        self.numero_input = QLineEdit()
        self.numero_input.setPlaceholderText("Número")
        self.numero_input.setFixedWidth(100)
        self.bairro_input = QLineEdit()
        self.bairro_input.setPlaceholderText("Bairro")
        endereco_numero_layout.addWidget(self.numero_input)
        endereco_numero_layout.addWidget(QLabel("Bairro:"))
        endereco_numero_layout.addWidget(self.bairro_input)
        form_endereco.addRow("Número:", endereco_numero_layout)
        
        endereco_cidade_layout = QHBoxLayout()
        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Cidade")
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(Helpers.estados_brasil())
        self.estado_combo.setEditable(False)
        self.estado_combo.setFixedWidth(80)
        endereco_cidade_layout.addWidget(self.cidade_input)
        endereco_cidade_layout.addWidget(QLabel("UF:"))
        endereco_cidade_layout.addWidget(self.estado_combo)
        form_endereco.addRow("Cidade:", endereco_cidade_layout)
        
        self.cep_input = QLineEdit()
        self.cep_input.setPlaceholderText("00000-000")
        form_endereco.addRow("CEP:", self.cep_input)
        
        grupo_endereco.setLayout(form_endereco)
        form_layout.addWidget(grupo_endereco)
        
        # Observações
        grupo_obs = QGroupBox("Observações")
        obs_layout = QVBoxLayout()
        self.observacoes_input = QTextEdit()
        self.observacoes_input.setPlaceholderText("Observações e notas sobre o cliente...")
        self.observacoes_input.setMaximumHeight(100)
        obs_layout.addWidget(self.observacoes_input)
        grupo_obs.setLayout(obs_layout)
        form_layout.addWidget(grupo_obs)
        
        form_layout.addStretch()
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
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
    
    def preencher_formulario(self):
        """Preenche o formulário com dados do cliente"""
        if not self.cliente:
            return
        
        self.nome_input.setText(self.cliente.nome)
        self.email_input.setText(self.cliente.email)
        self.telefone_input.setText(self.cliente.telefone)
        self.empresa_input.setText(self.cliente.empresa)
        self.cnpj_cpf_input.setText(self.cliente.cnpj_cpf)
        self.rua_input.setText(self.cliente.endereco_rua)
        self.numero_input.setText(self.cliente.endereco_numero)
        self.bairro_input.setText(self.cliente.endereco_bairro)
        self.cidade_input.setText(self.cliente.endereco_cidade)
        
        # Estado
        estado_index = self.estado_combo.findText(self.cliente.endereco_estado)
        if estado_index >= 0:
            self.estado_combo.setCurrentIndex(estado_index)
        
        self.cep_input.setText(self.cliente.endereco_cep)
        self.observacoes_input.setPlainText(self.cliente.observacoes)
    
    def validar_formulario(self) -> Tuple[bool, str]:
        """Valida os dados do formulário"""
        # Nome obrigatório
        nome = self.nome_input.text().strip()
        if not nome:
            return False, "Nome é obrigatório"
        
        # Email válido (se preenchido)
        email = self.email_input.text().strip()
        if email and not Validators.validar_email(email):
            return False, "Email inválido"
        
        # CPF/CNPJ válido (se preenchido)
        cnpj_cpf = self.cnpj_cpf_input.text().strip()
        if cnpj_cpf and not Validators.validar_cpf_cnpj(cnpj_cpf):
            return False, "CPF/CNPJ inválido"
        
        return True, ""
    
    def obter_cliente_do_formulario(self) -> Cliente:
        """Obtém os dados do formulário e retorna um objeto Cliente"""
        cliente = Cliente()
        
        if self.is_editing:
            cliente.id = self.cliente.id
        
        cliente.nome = self.nome_input.text().strip()
        cliente.email = self.email_input.text().strip()
        cliente.telefone = self.telefone_input.text().strip()
        cliente.empresa = self.empresa_input.text().strip()
        cliente.cnpj_cpf = self.cnpj_cpf_input.text().strip()
        cliente.endereco_rua = self.rua_input.text().strip()
        cliente.endereco_numero = self.numero_input.text().strip()
        cliente.endereco_bairro = self.bairro_input.text().strip()
        cliente.endereco_cidade = self.cidade_input.text().strip()
        cliente.endereco_estado = self.estado_combo.currentText()
        cliente.endereco_cep = self.cep_input.text().strip()
        cliente.observacoes = self.observacoes_input.toPlainText().strip()
        
        return cliente
    
    def on_salvar_clicked(self):
        """Callback para salvar cliente"""
        # Validar
        valido, mensagem_erro = self.validar_formulario()
        if not valido:
            Helpers.mostrar_mensagem("Validação", mensagem_erro, 'warning', self)
            return
        
        # Obter dados
        cliente = self.obter_cliente_do_formulario()
        
        try:
            if self.is_editing:
                # Atualizar
                sucesso = self.cliente_service.atualizar_cliente(cliente)
                if sucesso:
                    Helpers.mostrar_mensagem("Sucesso", "Cliente atualizado com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao atualizar cliente", 'error', self)
            else:
                # Criar
                cliente_id = self.cliente_service.criar_cliente(cliente)
                if cliente_id:
                    Helpers.mostrar_mensagem("Sucesso", "Cliente cadastrado com sucesso!", 'info', self)
                    self.accept()
                else:
                    Helpers.mostrar_mensagem("Erro", "Erro ao cadastrar cliente", 'error', self)
        except ValueError as e:
            Helpers.mostrar_mensagem("Validação", str(e), 'warning', self)
        except Exception as e:
            Helpers.mostrar_mensagem("Erro", f"Erro ao salvar: {str(e)}", 'error', self)

