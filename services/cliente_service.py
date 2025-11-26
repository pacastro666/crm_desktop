"""
Service para Cliente - Regras de negócio
"""
from typing import List, Optional
from models.cliente import Cliente
from models.interacao import Interacao
from repositories.cliente_repository import ClienteRepository
from repositories.interacao_repository import InteracaoRepository
from utils.validators import Validators


class ClienteService:
    """Service com regras de negócio para Cliente"""
    
    def __init__(self, cliente_repo: ClienteRepository, interacao_repo: InteracaoRepository):
        self.cliente_repo = cliente_repo
        self.interacao_repo = interacao_repo
    
    def criar_cliente(self, cliente: Cliente) -> int:
        """Cria um novo cliente com validações"""
        # Validações
        if not cliente.nome or not cliente.nome.strip():
            raise ValueError("Nome é obrigatório")
        
        if cliente.email and not Validators.validar_email(cliente.email):
            raise ValueError("Email inválido")
        
        if cliente.cnpj_cpf:
            if not Validators.validar_cpf_cnpj(cliente.cnpj_cpf):
                raise ValueError("CPF/CNPJ inválido")
        
        # Criar cliente
        cliente_id = self.cliente_repo.criar(cliente)
        
        # Registrar interação
        self.interacao_repo.criar(Interacao(
            cliente_id=cliente_id,
            tipo="cliente_criado",
            descricao=f"Cliente {cliente.nome} foi cadastrado"
        ))
        
        return cliente_id
    
    def atualizar_cliente(self, cliente: Cliente) -> bool:
        """Atualiza um cliente existente com validações"""
        if not cliente.id:
            raise ValueError("ID do cliente é obrigatório para atualização")
        
        if not cliente.nome or not cliente.nome.strip():
            raise ValueError("Nome é obrigatório")
        
        if cliente.email and not Validators.validar_email(cliente.email):
            raise ValueError("Email inválido")
        
        if cliente.cnpj_cpf and not Validators.validar_cpf_cnpj(cliente.cnpj_cpf):
            raise ValueError("CPF/CNPJ inválido")
        
        # Atualizar cliente
        sucesso = self.cliente_repo.atualizar(cliente)
        
        if sucesso:
            # Registrar interação
            self.interacao_repo.criar(Interacao(
                cliente_id=cliente.id,
                tipo="cliente_editado",
                descricao=f"Cliente {cliente.nome} foi atualizado"
            ))
        
        return sucesso
    
    def buscar_cliente(self, id: int) -> Optional[Cliente]:
        """Busca um cliente por ID"""
        return self.cliente_repo.buscar_por_id(id)
    
    def listar_clientes(self) -> List[Cliente]:
        """Lista todos os clientes"""
        return self.cliente_repo.listar_todos()
    
    def buscar_clientes(self, termo: str) -> List[Cliente]:
        """Busca clientes por termo"""
        return self.cliente_repo.buscar(termo)
    
    def excluir_cliente(self, id: int) -> bool:
        """Exclui um cliente"""
        cliente = self.cliente_repo.buscar_por_id(id)
        if not cliente:
            return False
        
        sucesso = self.cliente_repo.excluir(id)
        
        if sucesso:
            # Registrar interação
            self.interacao_repo.criar(Interacao(
                cliente_id=id,
                tipo="cliente_excluido",
                descricao=f"Cliente {cliente.nome} foi excluído"
            ))
        
        return sucesso

