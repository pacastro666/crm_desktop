"""
Janela principal do sistema CRM
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QStackedWidget, QPushButton, QLineEdit, QLabel,
                               QListWidget, QListWidgetItem, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from core.settings import APP_NAME


class MainWindow(QMainWindow):
    """Janela principal do sistema"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Menu lateral
        self.sidebar = self._criar_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Área central com stacked widget
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Barra superior
        self._criar_barra_superior()
    
    def _criar_sidebar(self) -> QWidget:
        """Cria o menu lateral"""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #1f2937;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:checked {
                background-color: #2563eb;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        
        # Logo/Título
        title = QLabel(APP_NAME)
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Botões do menu
        self.btn_dashboard = QPushButton("📊 Dashboard")
        self.btn_clientes = QPushButton("👥 Clientes")
        self.btn_oportunidades = QPushButton("💼 Oportunidades")
        self.btn_tarefas = QPushButton("✓ Tarefas")
        self.btn_relatorios = QPushButton("📈 Relatórios")
        self.btn_configuracoes = QPushButton("⚙️ Configurações")
        
        # Tornar botões checkable
        for btn in [self.btn_dashboard, self.btn_clientes, self.btn_oportunidades,
                   self.btn_tarefas, self.btn_relatorios, self.btn_configuracoes]:
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return sidebar
    
    def _criar_barra_superior(self):
        """Cria a barra superior"""
        toolbar = self.addToolBar("Principal")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: white;
                border-bottom: 1px solid #e5e7eb;
                padding: 5px;
            }
        """)
        
        # Busca global
        self.busca_global = QLineEdit()
        self.busca_global.setPlaceholderText("Buscar clientes, oportunidades...")
        self.busca_global.setFixedWidth(300)
        toolbar.addWidget(QLabel("🔍"))
        toolbar.addWidget(self.busca_global)
        
        toolbar.addSeparator()
        
        # Notificações
        self.btn_notificacoes = QPushButton("🔔 Notificações")
        toolbar.addWidget(self.btn_notificacoes)
        
        toolbar.addSeparator()
        
        # Perfil
        self.btn_perfil = QPushButton("👤 Perfil")
        toolbar.addWidget(self.btn_perfil)
    
    def adicionar_view(self, widget: QWidget, nome: str):
        """Adiciona uma view ao stacked widget"""
        self.stacked_widget.addWidget(widget)
    
    def mostrar_view(self, index: int):
        """Mostra a view no índice especificado"""
        self.stacked_widget.setCurrentIndex(index)
        # Atualizar botões do menu
        buttons = [self.btn_dashboard, self.btn_clientes, self.btn_oportunidades,
                  self.btn_tarefas, self.btn_relatorios, self.btn_configuracoes]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)

