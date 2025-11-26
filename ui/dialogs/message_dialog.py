"""
Diálogos de mensagem
"""
from utils.helpers import Helpers


def mostrar_sucesso(mensagem: str, parent=None):
    """Mostra mensagem de sucesso"""
    Helpers.mostrar_mensagem("Sucesso", mensagem, 'info', parent)


def mostrar_erro(mensagem: str, parent=None):
    """Mostra mensagem de erro"""
    Helpers.mostrar_mensagem("Erro", mensagem, 'error', parent)


def mostrar_aviso(mensagem: str, parent=None):
    """Mostra mensagem de aviso"""
    Helpers.mostrar_mensagem("Aviso", mensagem, 'warning', parent)

