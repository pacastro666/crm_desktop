"""
Service para geração de relatórios
"""
from typing import List, Dict
from datetime import datetime, date, timedelta
from repositories.cliente_repository import ClienteRepository
from repositories.oportunidade_repository import OportunidadeRepository
from repositories.tarefa_repository import TarefaRepository
from core.database import DatabaseManager


class RelatorioService:
    """Service para geração de relatórios e métricas"""
    
    def __init__(self, cliente_repo: ClienteRepository, 
                 oportunidade_repo: OportunidadeRepository,
                 tarefa_repo: TarefaRepository):
        self.cliente_repo = cliente_repo
        self.oportunidade_repo = oportunidade_repo
        self.tarefa_repo = tarefa_repo
    
    def total_clientes(self) -> int:
        """Retorna o total de clientes"""
        return len(self.cliente_repo.listar_todos())
    
    def total_oportunidades_abertas(self) -> int:
        """Retorna o total de oportunidades abertas (não fechadas/perdidas)"""
        todas = self.oportunidade_repo.listar_todos()
        return sum(1 for op in todas if op.etapa not in ['Fechado', 'Perdido'])
    
    def valor_total_negociacao(self) -> float:
        """Retorna o valor total em negociação"""
        oportunidades = self.oportunidade_repo.listar_todos()
        total = sum(
            op.valor * (op.probabilidade / 100)
            for op in oportunidades
            if op.etapa not in ['Fechado', 'Perdido']
        )
        return total
    
    def total_tarefas_pendentes_hoje(self) -> int:
        """Retorna o total de tarefas pendentes de hoje"""
        return len(self.tarefa_repo.buscar_pendentes_hoje())
    
    def oportunidades_por_etapa(self) -> Dict[str, int]:
        """Retorna contagem de oportunidades por etapa"""
        todas = self.oportunidade_repo.listar_todos()
        etapas = {}
        for op in todas:
            etapas[op.etapa] = etapas.get(op.etapa, 0) + 1
        return etapas
    
    def vendas_por_periodo(self, data_inicio: date, data_fim: date) -> List[Dict]:
        """Retorna vendas (oportunidades fechadas) por período"""
        query = """
            SELECT DATE(criado_em) as data, SUM(valor) as total
            FROM oportunidades
            WHERE etapa = 'Fechado'
            AND DATE(criado_em) BETWEEN %s AND %s
            GROUP BY DATE(criado_em)
            ORDER BY data
        """
        try:
            result = DatabaseManager.execute_query(
                query, (data_inicio, data_fim), fetch=True
            )
            return result
        except Exception as e:
            print(f"Erro ao buscar vendas por período: {e}")
            return []
    
    def tarefas_concluidas_vs_pendentes(self) -> Dict[str, int]:
        """Retorna contagem de tarefas concluídas vs pendentes"""
        todas = self.tarefa_repo.listar_todos()
        concluidas = sum(1 for t in todas if t.status == 'Concluída')
        pendentes = sum(1 for t in todas if t.status == 'Pendente')
        return {
            'concluidas': concluidas,
            'pendentes': pendentes,
            'total': len(todas)
        }
    
    def taxa_conversao(self) -> float:
        """Calcula taxa de conversão"""
        todas = self.oportunidade_repo.listar_todos()
        if not todas:
            return 0.0
        fechadas = sum(1 for op in todas if op.etapa == 'Fechado')
        return (fechadas / len(todas)) * 100

