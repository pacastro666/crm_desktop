"""
Service para Tarefa - Regras de negócio
"""
from typing import List, Optional
from datetime import datetime
from models.tarefa import Tarefa
from models.interacao import Interacao
from repositories.tarefa_repository import TarefaRepository
from repositories.interacao_repository import InteracaoRepository


class TarefaService:
    """Service com regras de negócio para Tarefa"""
    
    TIPOS = ['Ligação', 'Email', 'Reunião', 'WhatsApp', 'Visita', 'Outro']
    STATUS = ['Pendente', 'Concluída']
    PRIORIDADES = ['Baixa', 'Média', 'Alta']
    
    def __init__(self, tarefa_repo: TarefaRepository, interacao_repo: InteracaoRepository):
        self.tarefa_repo = tarefa_repo
        self.interacao_repo = interacao_repo
    
    def criar_tarefa(self, tarefa: Tarefa) -> int:
        """Cria uma nova tarefa com validações"""
        if not tarefa.descricao or not tarefa.descricao.strip():
            raise ValueError("Descrição é obrigatória")
        
        if not tarefa.cliente_id:
            raise ValueError("Cliente é obrigatório")
        
        if not tarefa.data_hora:
            raise ValueError("Data e hora são obrigatórias")
        
        if tarefa.tipo not in self.TIPOS:
            raise ValueError(f"Tipo inválido")
        
        if tarefa.prioridade not in self.PRIORIDADES:
            raise ValueError(f"Prioridade inválida")
        
        # Criar tarefa
        tarefa_id = self.tarefa_repo.criar(tarefa)
        
        # Registrar interação
        self.interacao_repo.criar(Interacao(
            cliente_id=tarefa.cliente_id,
            tipo="tarefa_criada",
            descricao=f"Tarefa '{tarefa.descricao}' foi criada"
        ))
        
        return tarefa_id
    
    def atualizar_tarefa(self, tarefa: Tarefa) -> bool:
        """Atualiza uma tarefa existente"""
        if not tarefa.id:
            raise ValueError("ID da tarefa é obrigatório")
        
        if not tarefa.descricao or not tarefa.descricao.strip():
            raise ValueError("Descrição é obrigatória")
        
        return self.tarefa_repo.atualizar(tarefa)
    
    def buscar_tarefa(self, id: int) -> Optional[Tarefa]:
        """Busca uma tarefa por ID"""
        return self.tarefa_repo.buscar_por_id(id)
    
    def listar_tarefas(self) -> List[Tarefa]:
        """Lista todas as tarefas"""
        return self.tarefa_repo.listar_todos()
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Tarefa]:
        """Busca tarefas de um cliente"""
        return self.tarefa_repo.buscar_por_cliente(cliente_id)
    
    def buscar_pendentes_hoje(self) -> List[Tarefa]:
        """Busca tarefas pendentes de hoje"""
        return self.tarefa_repo.buscar_pendentes_hoje()
    
    def buscar_atrasadas(self) -> List[Tarefa]:
        """Busca tarefas atrasadas"""
        return self.tarefa_repo.buscar_atrasadas()
    
    def buscar_por_status(self, status: str) -> List[Tarefa]:
        """Busca tarefas por status"""
        return self.tarefa_repo.buscar_por_status(status)
    
    def marcar_concluida(self, id: int) -> bool:
        """Marca uma tarefa como concluída"""
        tarefa = self.tarefa_repo.buscar_por_id(id)
        if not tarefa:
            return False
        
        sucesso = self.tarefa_repo.marcar_concluida(id)
        
        if sucesso:
            # Registrar interação
            self.interacao_repo.criar(Interacao(
                cliente_id=tarefa.cliente_id,
                tipo="tarefa_concluida",
                descricao=f"Tarefa '{tarefa.descricao}' foi concluída"
            ))
        
        return sucesso
    
    def excluir_tarefa(self, id: int) -> bool:
        """Exclui uma tarefa"""
        return self.tarefa_repo.excluir(id)

