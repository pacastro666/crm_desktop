"""
View do Dashboard - Versão Melhorada
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QScrollArea, QGridLayout, QProgressBar)
from PySide6.QtCore import Qt, QSize
from datetime import datetime, timedelta, date
from services.relatorio_service import RelatorioService
from services.tarefa_service import TarefaService
from services.oportunidade_service import OportunidadeService
from services.cliente_service import ClienteService
from utils.formatters import Formatters


class DashboardView(QWidget):
    """Tela de dashboard com métricas melhoradas"""
    
    def __init__(self, relatorio_service: RelatorioService, 
                 tarefa_service: TarefaService = None,
                 oportunidade_service: OportunidadeService = None,
                 cliente_service: ClienteService = None):
        super().__init__()
        self.relatorio_service = relatorio_service
        self.tarefa_service = tarefa_service
        self.oportunidade_service = oportunidade_service
        self.cliente_service = cliente_service
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("📊 Dashboard")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #1f2937; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Cards de métricas em grid
        self.metricas_grid = QGridLayout()
        self.metricas_grid.setSpacing(15)
        layout.addLayout(self.metricas_grid)
        
        # Área de conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Layout em duas colunas
        colunas_layout = QHBoxLayout()
        colunas_layout.setSpacing(20)
        
        # Coluna esquerda
        coluna_esquerda = QVBoxLayout()
        coluna_esquerda.setSpacing(15)
        
        # Gráfico de oportunidades por etapa
        self.frame_oportunidades = self._criar_secao("💼 Oportunidades por Etapa")
        coluna_esquerda.addWidget(self.frame_oportunidades)
        
        # Taxa de conversão
        self.frame_conversao = self._criar_secao("📈 Taxa de Conversão")
        coluna_esquerda.addWidget(self.frame_conversao)
        
        colunas_layout.addLayout(coluna_esquerda, 1)
        
        # Coluna direita
        coluna_direita = QVBoxLayout()
        coluna_direita.setSpacing(15)
        
        # Próximas tarefas
        self.frame_tarefas = self._criar_secao("✓ Próximas Tarefas")
        coluna_direita.addWidget(self.frame_tarefas)
        
        # Oportunidades próximas do fechamento
        self.frame_oportunidades_proximas = self._criar_secao("🎯 Oportunidades Próximas")
        coluna_direita.addWidget(self.frame_oportunidades_proximas)
        
        colunas_layout.addLayout(coluna_direita, 1)
        
        content_layout.addLayout(colunas_layout)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def _criar_secao(self, titulo: str) -> QFrame:
        """Cria uma seção com título"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #1f2937;")
        layout.addWidget(label_titulo)
        
        return frame
    
    def criar_card_metrica(self, titulo: str, valor: str, cor: str = "#2563eb", 
                          icone: str = "", subtitulo: str = "") -> QFrame:
        """Cria um card de métrica melhorado"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 12px;
                padding: 20px;
                border-left: 5px solid {cor};
                border: 1px solid #e5e7eb;
            }}
        """)
        card.setMinimumHeight(130)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Título e ícone
        titulo_layout = QHBoxLayout()
        
        if icone:
            label_icone = QLabel(icone)
            label_icone.setStyleSheet("font-size: 24px;")
            titulo_layout.addWidget(label_icone)
        
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("color: #6b7280; font-size: 14px; font-weight: 500;")
        titulo_layout.addWidget(label_titulo)
        titulo_layout.addStretch()
        
        layout.addLayout(titulo_layout)
        
        # Valor
        label_valor = QLabel(valor)
        label_valor.setStyleSheet(f"color: {cor}; font-size: 32px; font-weight: bold;")
        layout.addWidget(label_valor)
        
        # Subtítulo
        if subtitulo:
            label_subtitulo = QLabel(subtitulo)
            label_subtitulo.setStyleSheet("color: #9ca3af; font-size: 12px;")
            layout.addWidget(label_subtitulo)
        
        layout.addStretch()
        
        return card
    
    def carregar_dados(self):
        """Carrega os dados do dashboard"""
        # Limpar métricas existentes
        while self.metricas_grid.count():
            item = self.metricas_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Total de clientes
        total_clientes = self.relatorio_service.total_clientes()
        card_clientes = self.criar_card_metrica(
            "Total de Clientes", 
            str(total_clientes), 
            "#2563eb",
            "👥"
        )
        self.metricas_grid.addWidget(card_clientes, 0, 0)
        
        # Oportunidades abertas
        op_abertas = self.relatorio_service.total_oportunidades_abertas()
        card_oportunidades = self.criar_card_metrica(
            "Oportunidades Abertas", 
            str(op_abertas), 
            "#10b981",
            "💼"
        )
        self.metricas_grid.addWidget(card_oportunidades, 0, 1)
        
        # Valor em negociação
        valor_neg = self.relatorio_service.valor_total_negociacao()
        card_valor = self.criar_card_metrica(
            "Valor em Negociação", 
            Formatters.formatar_moeda(valor_neg), 
            "#f59e0b",
            "💰"
        )
        self.metricas_grid.addWidget(card_valor, 0, 2)
        
        # Tarefas pendentes hoje
        tarefas_hoje = self.relatorio_service.total_tarefas_pendentes_hoje()
        tarefas_atrasadas = len(self.tarefa_service.buscar_atrasadas()) if self.tarefa_service else 0
        subtitulo_tarefas = f"{tarefas_atrasadas} atrasadas" if tarefas_atrasadas > 0 else "Todas em dia"
        card_tarefas = self.criar_card_metrica(
            "Tarefas Hoje", 
            str(tarefas_hoje), 
            "#ef4444",
            "✓",
            subtitulo_tarefas
        )
        self.metricas_grid.addWidget(card_tarefas, 0, 3)
        
        # Taxa de conversão
        taxa = self.relatorio_service.taxa_conversao()
        card_taxa = self.criar_card_metrica(
            "Taxa de Conversão",
            f"{taxa:.1f}%",
            "#8b5cf6",
            "📊"
        )
        self.metricas_grid.addWidget(card_taxa, 1, 0)
        
        # Total de oportunidades
        todas_op = len(self.oportunidade_service.listar_oportunidades()) if self.oportunidade_service else 0
        fechadas = sum(1 for op in self.oportunidade_service.listar_oportunidades() if op.etapa == 'Fechado') if self.oportunidade_service else 0
        card_total_op = self.criar_card_metrica(
            "Total Oportunidades",
            str(todas_op),
            "#06b6d4",
            "📈",
            f"{fechadas} fechadas"
        )
        self.metricas_grid.addWidget(card_total_op, 1, 1)
        
        # Tarefas concluídas vs pendentes
        tarefas_stats = self.relatorio_service.tarefas_concluidas_vs_pendentes()
        card_tarefas_stats = self.criar_card_metrica(
            "Tarefas",
            f"{tarefas_stats['concluidas']}/{tarefas_stats['total']}",
            "#14b8a6",
            "✓",
            f"{tarefas_stats['pendentes']} pendentes"
        )
        self.metricas_grid.addWidget(card_tarefas_stats, 1, 2)
        
        # Valor total fechado
        if self.oportunidade_service:
            todas = self.oportunidade_service.listar_oportunidades()
            valor_fechado = sum(op.valor for op in todas if op.etapa == 'Fechado')
            card_fechado = self.criar_card_metrica(
                "Valor Fechado",
                Formatters.formatar_moeda(valor_fechado),
                "#22c55e",
                "✅"
            )
            self.metricas_grid.addWidget(card_fechado, 1, 3)
        
        # Atualizar seções
        self._atualizar_oportunidades_etapa()
        self._atualizar_taxa_conversao()
        self._atualizar_proximas_tarefas()
        self._atualizar_oportunidades_proximas()
    
    def _atualizar_oportunidades_etapa(self):
        """Atualiza o gráfico de oportunidades por etapa"""
        layout = self.frame_oportunidades.layout()
        # Limpar layout (exceto título)
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._limpar_layout(item.layout())
        
        oportunidades_por_etapa = self.relatorio_service.oportunidades_por_etapa()
        
        if not oportunidades_por_etapa:
            label = QLabel("Nenhuma oportunidade cadastrada")
            label.setStyleSheet("color: #6b7280; padding: 20px;")
            layout.addWidget(label)
        else:
            # Ordenar por ordem do funil
            ordem_etapas = ["Lead", "Qualificação", "Proposta", "Negociação", "Fechado", "Perdido"]
            cores = {
                "Lead": "#3b82f6",
                "Qualificação": "#10b981",
                "Proposta": "#f59e0b",
                "Negociação": "#8b5cf6",
                "Fechado": "#22c55e",
                "Perdido": "#ef4444"
            }
            
            max_valor = max(oportunidades_por_etapa.values()) if oportunidades_por_etapa.values() else 1
            
            for etapa in ordem_etapas:
                if etapa not in oportunidades_por_etapa:
                    continue
                
                quantidade = oportunidades_por_etapa[etapa]
                cor = cores.get(etapa, "#6b7280")
                
                linha = QHBoxLayout()
                linha.setSpacing(10)
                
                # Label da etapa
                label_etapa = QLabel(etapa)
                label_etapa.setStyleSheet(f"font-weight: bold; min-width: 120px; color: {cor};")
                linha.addWidget(label_etapa)
                
                # Barra de progresso
                progress = QProgressBar()
                progress.setMaximum(max_valor)
                progress.setValue(quantidade)
                progress.setTextVisible(False)
                progress.setStyleSheet(f"""
                    QProgressBar {{
                        border: none;
                        border-radius: 6px;
                        background: #e5e7eb;
                        height: 25px;
                    }}
                    QProgressBar::chunk {{
                        background: {cor};
                        border-radius: 6px;
                    }}
                """)
                linha.addWidget(progress, 1)
                
                # Label quantidade
                label_qtd = QLabel(str(quantidade))
                label_qtd.setStyleSheet(f"font-weight: bold; min-width: 40px; color: {cor}; font-size: 14px;")
                label_qtd.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                linha.addWidget(label_qtd)
                
                layout.addLayout(linha)
    
    def _atualizar_taxa_conversao(self):
        """Atualiza a seção de taxa de conversão"""
        layout = self.frame_conversao.layout()
        # Limpar layout (exceto título)
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        
        taxa = self.relatorio_service.taxa_conversao()
        
        # Gráfico circular simples (barra de progresso)
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(int(taxa))
        progress.setFormat(f"{taxa:.1f}%")
        progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background: #e5e7eb;
                height: 40px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #22c55e);
                border-radius: 8px;
            }
        """)
        layout.addWidget(progress)
        
        # Informações adicionais
        if self.oportunidade_service:
            todas = self.oportunidade_service.listar_oportunidades()
            fechadas = sum(1 for op in todas if op.etapa == 'Fechado')
            perdidas = sum(1 for op in todas if op.etapa == 'Perdido')
            
            info = QLabel(f"Fechadas: {fechadas} | Perdidas: {perdidas} | Total: {len(todas)}")
            info.setStyleSheet("color: #6b7280; font-size: 12px; margin-top: 10px;")
            layout.addWidget(info)
    
    def _atualizar_proximas_tarefas(self):
        """Atualiza a lista de próximas tarefas"""
        layout = self.frame_tarefas.layout()
        # Limpar layout (exceto título)
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.tarefa_service:
            label = QLabel("Serviço de tarefas não disponível")
            label.setStyleSheet("color: #6b7280;")
            layout.addWidget(label)
            return
        
        # Buscar próximas tarefas (próximos 5 dias)
        todas = self.tarefa_service.listar_tarefas()
        hoje = datetime.now().date()
        proximas = [
            t for t in todas
            if t.status == 'Pendente' and t.data_hora and
            t.data_hora.date() >= hoje and
            t.data_hora.date() <= (hoje + timedelta(days=5))
        ]
        proximas.sort(key=lambda x: x.data_hora if x.data_hora else datetime.max)
        proximas = proximas[:5]  # Limitar a 5
        
        if not proximas:
            label = QLabel("Nenhuma tarefa nos próximos 5 dias")
            label.setStyleSheet("color: #6b7280; padding: 10px;")
            layout.addWidget(label)
        else:
            for tarefa in proximas:
                item = self._criar_item_tarefa(tarefa)
                layout.addWidget(item)
    
    def _criar_item_tarefa(self, tarefa) -> QFrame:
        """Cria um item de tarefa para a lista"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #f9fafb;
                border-radius: 8px;
                padding: 12px;
                border-left: 3px solid #3b82f6;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        # Descrição
        label_desc = QLabel(tarefa.descricao)
        label_desc.setStyleSheet("font-weight: bold; color: #1f2937;")
        layout.addWidget(label_desc)
        
        # Informações
        info_layout = QHBoxLayout()
        
        # Data/Hora
        if tarefa.data_hora:
            data_str = Formatters.formatar_data_hora(tarefa.data_hora)
            label_data = QLabel(f"📅 {data_str}")
            label_data.setStyleSheet("color: #6b7280; font-size: 12px;")
            info_layout.addWidget(label_data)
        
        info_layout.addStretch()
        
        # Prioridade
        cores_prioridade = {"Alta": "#ef4444", "Média": "#f59e0b", "Baixa": "#10b981"}
        cor = cores_prioridade.get(tarefa.prioridade, "#6b7280")
        label_prioridade = QLabel(tarefa.prioridade)
        label_prioridade.setStyleSheet(f"color: {cor}; font-weight: bold; font-size: 11px; padding: 2px 8px; background: {cor}20; border-radius: 4px;")
        info_layout.addWidget(label_prioridade)
        
        layout.addLayout(info_layout)
        
        return frame
    
    def _atualizar_oportunidades_proximas(self):
        """Atualiza a lista de oportunidades próximas do fechamento"""
        layout = self.frame_oportunidades_proximas.layout()
        # Limpar layout (exceto título)
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.oportunidade_service or not self.cliente_service:
            label = QLabel("Serviços não disponíveis")
            label.setStyleSheet("color: #6b7280;")
            layout.addWidget(label)
            return
        
        # Buscar oportunidades em negociação com alta probabilidade
        todas = self.oportunidade_service.listar_oportunidades()
        proximas = [
            op for op in todas
            if op.etapa in ["Negociação", "Proposta"] and
            op.probabilidade >= 70 and
            op.data_prevista_fechamento and
            op.data_prevista_fechamento >= date.today()
        ]
        proximas.sort(key=lambda x: (x.data_prevista_fechamento, -x.probabilidade))
        proximas = proximas[:5]  # Limitar a 5
        
        if not proximas:
            label = QLabel("Nenhuma oportunidade próxima do fechamento")
            label.setStyleSheet("color: #6b7280; padding: 10px;")
            layout.addWidget(label)
        else:
            for op in proximas:
                item = self._criar_item_oportunidade(op)
                layout.addWidget(item)
    
    def _criar_item_oportunidade(self, oportunidade) -> QFrame:
        """Cria um item de oportunidade para a lista"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #f9fafb;
                border-radius: 8px;
                padding: 12px;
                border-left: 3px solid #f59e0b;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        # Título
        label_titulo = QLabel(oportunidade.titulo)
        label_titulo.setStyleSheet("font-weight: bold; color: #1f2937;")
        layout.addWidget(label_titulo)
        
        # Informações
        info_layout = QHBoxLayout()
        
        # Valor
        label_valor = QLabel(f"💰 {Formatters.formatar_moeda(oportunidade.valor)}")
        label_valor.setStyleSheet("color: #6b7280; font-size: 12px;")
        info_layout.addWidget(label_valor)
        
        info_layout.addStretch()
        
        # Probabilidade
        label_prob = QLabel(f"{oportunidade.probabilidade}%")
        label_prob.setStyleSheet("color: #f59e0b; font-weight: bold; font-size: 12px;")
        info_layout.addWidget(label_prob)
        
        layout.addLayout(info_layout)
        
        # Data
        if oportunidade.data_prevista_fechamento:
            data_str = Formatters.formatar_data(oportunidade.data_prevista_fechamento)
            label_data = QLabel(f"📅 {data_str}")
            label_data.setStyleSheet("color: #6b7280; font-size: 11px;")
            layout.addWidget(label_data)
        
        return frame
    
    def _limpar_layout(self, layout):
        """Limpa um layout recursivamente"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._limpar_layout(item.layout())
