"""
Funções auxiliares gerais
"""
from typing import List, Optional
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt


class Helpers:
    """Classe com funções auxiliares"""
    
    @staticmethod
    def mostrar_mensagem(titulo: str, mensagem: str, tipo: str = 'info', parent=None):
        """Mostra uma mensagem ao usuário"""
        msg = QMessageBox(parent)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        
        if tipo == 'info':
            msg.setIcon(QMessageBox.Information)
        elif tipo == 'warning':
            msg.setIcon(QMessageBox.Warning)
        elif tipo == 'error':
            msg.setIcon(QMessageBox.Critical)
        elif tipo == 'question':
            msg.setIcon(QMessageBox.Question)
        
        msg.exec()
    
    @staticmethod
    def confirmar_acao(titulo: str, mensagem: str, parent=None) -> bool:
        """Mostra diálogo de confirmação"""
        msg = QMessageBox(parent)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        resposta = msg.exec()
        return resposta == QMessageBox.Yes
    
    @staticmethod
    def estados_brasil() -> List[str]:
        """Retorna lista de estados brasileiros"""
        return [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
    
    @staticmethod
    def limpar_string(texto: str) -> str:
        """Remove espaços extras e caracteres especiais"""
        if not texto:
            return ""
        return ' '.join(texto.split())
    
    @staticmethod
    def truncar_texto(texto: str, max_length: int = 50) -> str:
        """Trunca texto se exceder o tamanho máximo"""
        if not texto:
            return ""
        if len(texto) <= max_length:
            return texto
        return texto[:max_length - 3] + "..."

