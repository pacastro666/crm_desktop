"""
View do Dashboard
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QScrollArea)
from PySide6.QtCore import Qt
from services.relatorio_service import RelatorioService
from utils.formatters import Formatters


class DashboardView(QWidget):
    """Tela de dashboard com métricas"""
    
    def __init__(self, relatorio_service: RelatorioService):
        super().__init__()
        self.relatorio_service = relatorio_service
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("Dashboard")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937;")
        layout.addWidget(titulo)
        
        # Cards de métricas
        self.metricas_layout = QHBoxLayout()
        layout.addLayout(self.metricas_layout)
        
        # Área de conteúdo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Gráfico de oportunidades por etapa
        self.label_oportunidades = QLabel("Oportunidades por Etapa")
        self.label_oportunidades.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        content_layout.addWidget(self.label_oportunidades)
        
        self.frame_oportunidades = QFrame()
        self.frame_oportunidades.setStyleSheet("background: white; border-radius: 8px; padding: 15px;")
        content_layout.addWidget(self.frame_oportunidades)
        
        # Próximas tarefas
        self.label_tarefas = QLabel("Próximas Tarefas")
        self.label_tarefas.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        content_layout.addWidget(self.label_tarefas)
        
        self.frame_tarefas = QFrame()
        self.frame_tarefas.setStyleSheet("background: white; border-radius: 8px; padding: 15px;")
        content_layout.addWidget(self.frame_tarefas)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def criar_card_metrica(self, titulo: str, valor: str, cor: str = "#2563eb") -> QFrame:
        """Cria um card de métrica"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 8px;
                padding: 20px;
                border-left: 4px solid {cor};
            }}
        """)
        card.setFixedHeight(120)
        
        layout = QVBoxLayout(card)
        
        label_titulo = QLabel(titulo)
        label_titulo.setStyleSheet("color: #6b7280; font-size: 14px;")
        layout.addWidget(label_titulo)
        
        label_valor = QLabel(valor)
        label_valor.setStyleSheet("color: #1f2937; font-size: 28px; font-weight: bold;")
        layout.addWidget(label_valor)
        
        layout.addStretch()
        
        return card
    
    def carregar_dados(self):
        """Carrega os dados do dashboard"""
        # Limpar métricas existentes
        while self.metricas_layout.count():
            item = self.metricas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Total de clientes
        total_clientes = self.relatorio_service.total_clientes()
        card_clientes = self.criar_card_metrica("Total de Clientes", str(total_clientes), "#2563eb")
        self.metricas_layout.addWidget(card_clientes)
        
        # Oportunidades abertas
        op_abertas = self.relatorio_service.total_oportunidades_abertas()
        card_oportunidades = self.criar_card_metrica("Oportunidades Abertas", str(op_abertas), "#10b981")
        self.metricas_layout.addWidget(card_oportunidades)
        
        # Valor em negociação
        valor_neg = self.relatorio_service.valor_total_negociacao()
        card_valor = self.criar_card_metrica("Valor em Negociação", Formatters.formatar_moeda(valor_neg), "#f59e0b")
        self.metricas_layout.addWidget(card_valor)
        
        # Tarefas pendentes hoje
        tarefas_hoje = self.relatorio_service.total_tarefas_pendentes_hoje()
        card_tarefas = self.criar_card_metrica("Tarefas Hoje", str(tarefas_hoje), "#ef4444")
        self.metricas_layout.addWidget(card_tarefas)
        
        # Oportunidades por etapa
        self._atualizar_oportunidades_etapa()
    
    def _atualizar_oportunidades_etapa(self):
        """Atualiza o gráfico de oportunidades por etapa"""
        layout = QVBoxLayout(self.frame_oportunidades)
        # Limpar layout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        oportunidades_por_etapa = self.relatorio_service.oportunidades_por_etapa()
        
        if not oportunidades_por_etapa:
            label = QLabel("Nenhuma oportunidade cadastrada")
            label.setStyleSheet("color: #6b7280;")
            layout.addWidget(label)
        else:
            for etapa, quantidade in oportunidades_por_etapa.items():
                linha = QHBoxLayout()
                
                label_etapa = QLabel(etapa)
                label_etapa.setStyleSheet("font-weight: bold; min-width: 120px;")
                linha.addWidget(label_etapa)
                
                # Barra de progresso simples
                barra = QFrame()
                barra.setStyleSheet(f"""
                    QFrame {{
                        background: #e5e7eb;
                        border-radius: 4px;
                        min-height: 20px;
                    }}
                """)
                barra.setFixedWidth(quantidade * 20)  # Escala simples
                linha.addWidget(barra)
                
                label_qtd = QLabel(str(quantidade))
                linha.addWidget(label_qtd)
                
                layout.addLayout(linha)

