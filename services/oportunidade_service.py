"""
Service para Oportunidade - Regras de negócio
"""
from typing import List, Optional
from datetime import date
from models.oportunidade import Oportunidade
from models.interacao import Interacao
from repositories.oportunidade_repository import OportunidadeRepository
from repositories.interacao_repository import InteracaoRepository


class OportunidadeService:
    """Service com regras de negócio para Oportunidade"""
    
    ETAPAS = ['Lead', 'Qualificação', 'Proposta', 'Negociação', 'Fechado', 'Perdido']
    
    def __init__(self, oportunidade_repo: OportunidadeRepository, interacao_repo: InteracaoRepository):
        self.oportunidade_repo = oportunidade_repo
        self.interacao_repo = interacao_repo
    
    def criar_oportunidade(self, oportunidade: Oportunidade) -> int:
        """Cria uma nova oportunidade com validações"""
        if not oportunidade.titulo or not oportunidade.titulo.strip():
            raise ValueError("Título é obrigatório")
        
        if not oportunidade.cliente_id:
            raise ValueError("Cliente é obrigatório")
        
        if oportunidade.etapa not in self.ETAPAS:
            raise ValueError(f"Etapa inválida. Use uma das seguintes: {', '.join(self.ETAPAS)}")
        
        if oportunidade.valor < 0:
            raise ValueError("Valor não pode ser negativo")
        
        if not (0 <= oportunidade.probabilidade <= 100):
            raise ValueError("Probabilidade deve estar entre 0 e 100")
        
        if oportunidade.data_prevista_fechamento and oportunidade.data_prevista_fechamento < date.today():
            raise ValueError("Data prevista de fechamento não pode ser no passado")
        
        # Criar oportunidade
        oportunidade_id = self.oportunidade_repo.criar(oportunidade)
        
        # Registrar interação
        self.interacao_repo.criar(Interacao(
            cliente_id=oportunidade.cliente_id,
            tipo="oportunidade_criada",
            descricao=f"Oportunidade '{oportunidade.titulo}' foi criada na etapa {oportunidade.etapa}"
        ))
        
        return oportunidade_id
    
    def atualizar_oportunidade(self, oportunidade: Oportunidade) -> bool:
        """Atualiza uma oportunidade existente"""
        if not oportunidade.id:
            raise ValueError("ID da oportunidade é obrigatório")
        
        if not oportunidade.titulo or not oportunidade.titulo.strip():
            raise ValueError("Título é obrigatório")
        
        if oportunidade.etapa not in self.ETAPAS:
            raise ValueError(f"Etapa inválida")
        
        if oportunidade.valor < 0:
            raise ValueError("Valor não pode ser negativo")
        
        # Buscar oportunidade antiga para comparar etapa
        oportunidade_antiga = self.oportunidade_repo.buscar_por_id(oportunidade.id)
        etapa_anterior = oportunidade_antiga.etapa if oportunidade_antiga else None
        
        # Atualizar oportunidade
        sucesso = self.oportunidade_repo.atualizar(oportunidade)
        
        if sucesso and etapa_anterior and oportunidade.etapa != etapa_anterior:
            # Registrar interação de mudança de etapa
            self.interacao_repo.criar(Interacao(
                cliente_id=oportunidade.cliente_id,
                tipo="oportunidade_etapa_alterada",
                descricao=f"Oportunidade '{oportunidade.titulo}' mudou de {etapa_anterior} para {oportunidade.etapa}"
            ))
        
        return sucesso
    
    def buscar_oportunidade(self, id: int) -> Optional[Oportunidade]:
        """Busca uma oportunidade por ID"""
        return self.oportunidade_repo.buscar_por_id(id)
    
    def listar_oportunidades(self) -> List[Oportunidade]:
        """Lista todas as oportunidades"""
        return self.oportunidade_repo.listar_todos()
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Oportunidade]:
        """Busca oportunidades de um cliente"""
        return self.oportunidade_repo.buscar_por_cliente(cliente_id)
    
    def buscar_por_etapa(self, etapa: str) -> List[Oportunidade]:
        """Busca oportunidades por etapa"""
        return self.oportunidade_repo.buscar_por_etapa(etapa)
    
    def mover_etapa(self, id: int, nova_etapa: str) -> bool:
        """Move uma oportunidade para outra etapa"""
        if nova_etapa not in self.ETAPAS:
            raise ValueError(f"Etapa inválida")
        
        oportunidade = self.oportunidade_repo.buscar_por_id(id)
        if not oportunidade:
            return False
        
        etapa_anterior = oportunidade.etapa
        sucesso = self.oportunidade_repo.atualizar_etapa(id, nova_etapa)
        
        if sucesso:
            self.interacao_repo.criar(Interacao(
                cliente_id=oportunidade.cliente_id,
                tipo="oportunidade_etapa_alterada",
                descricao=f"Oportunidade '{oportunidade.titulo}' mudou de {etapa_anterior} para {nova_etapa}"
            ))
        
        return sucesso
    
    def excluir_oportunidade(self, id: int) -> bool:
        """Exclui uma oportunidade"""
        return self.oportunidade_repo.excluir(id)
    
    def calcular_valor_total_negociacao(self) -> float:
        """Calcula o valor total em negociação (oportunidades não fechadas/perdidas)"""
        oportunidades = self.oportunidade_repo.listar_todos()
        total = sum(
            op.valor * (op.probabilidade / 100)
            for op in oportunidades
            if op.etapa not in ['Fechado', 'Perdido']
        )
        return total
    
    def calcular_taxa_conversao(self) -> float:
        """Calcula a taxa de conversão (Fechado / Total)"""
        todas = self.oportunidade_repo.listar_todos()
        if not todas:
            return 0.0
        
        fechadas = sum(1 for op in todas if op.etapa == 'Fechado')
        return (fechadas / len(todas)) * 100

