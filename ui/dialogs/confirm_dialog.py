"""
Diálogo de confirmação
"""
from PySide6.QtWidgets import QMessageBox
from utils.helpers import Helpers


def confirmar_exclusao(titulo: str, mensagem: str, parent=None) -> bool:
    """Mostra diálogo de confirmação de exclusão"""
    return Helpers.confirmar_acao(titulo, mensagem, parent)

