"""
Service para exportação de dados
"""
import csv
from typing import List
from pathlib import Path
from datetime import datetime
from models.cliente import Cliente
from models.oportunidade import Oportunidade
from models.tarefa import Tarefa


class ExportService:
    """Service para exportação de dados para CSV/Excel"""
    
    @staticmethod
    def exportar_clientes_csv(clientes: List[Cliente], caminho: str) -> bool:
        """Exporta lista de clientes para CSV"""
        try:
            with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                # Cabeçalho
                writer.writerow([
                    'ID', 'Nome', 'Email', 'Telefone', 'Empresa', 'CNPJ/CPF',
                    'Rua', 'Número', 'Bairro', 'Cidade', 'Estado', 'CEP',
                    'Observações', 'Criado em', 'Atualizado em'
                ])
                # Dados
                for cliente in clientes:
                    writer.writerow([
                        cliente.id, cliente.nome, cliente.email, cliente.telefone,
                        cliente.empresa, cliente.cnpj_cpf, cliente.endereco_rua,
                        cliente.endereco_numero, cliente.endereco_bairro,
                        cliente.endereco_cidade, cliente.endereco_estado,
                        cliente.endereco_cep, cliente.observacoes,
                        cliente.criado_em, cliente.atualizado_em
                    ])
            return True
        except Exception as e:
            print(f"Erro ao exportar clientes: {e}")
            return False
    
    @staticmethod
    def exportar_oportunidades_csv(oportunidades: List[Oportunidade], caminho: str) -> bool:
        """Exporta lista de oportunidades para CSV"""
        try:
            with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                # Cabeçalho
                writer.writerow([
                    'ID', 'Cliente ID', 'Título', 'Etapa', 'Valor', 'Probabilidade',
                    'Data Prevista Fechamento', 'Responsável', 'Observações',
                    'Criado em', 'Atualizado em'
                ])
                # Dados
                for op in oportunidades:
                    writer.writerow([
                        op.id, op.cliente_id, op.titulo, op.etapa, op.valor,
                        op.probabilidade, op.data_prevista_fechamento,
                        op.responsavel, op.observacoes, op.criado_em, op.atualizado_em
                    ])
            return True
        except Exception as e:
            print(f"Erro ao exportar oportunidades: {e}")
            return False
    
    @staticmethod
    def exportar_tarefas_csv(tarefas: List[Tarefa], caminho: str) -> bool:
        """Exporta lista de tarefas para CSV"""
        try:
            with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                # Cabeçalho
                writer.writerow([
                    'ID', 'Cliente ID', 'Descrição', 'Tipo', 'Data/Hora',
                    'Status', 'Prioridade', 'Observações', 'Criado em', 'Concluída em'
                ])
                # Dados
                for tarefa in tarefas:
                    writer.writerow([
                        tarefa.id, tarefa.cliente_id, tarefa.descricao,
                        tarefa.tipo, tarefa.data_hora, tarefa.status,
                        tarefa.prioridade, tarefa.observacoes,
                        tarefa.criado_em, tarefa.concluida_em
                    ])
            return True
        except Exception as e:
            print(f"Erro ao exportar tarefas: {e}")
            return False
    
    @staticmethod
    def gerar_nome_arquivo_export(tipo: str) -> str:
        """Gera nome de arquivo para exportação com timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{tipo}_{timestamp}.csv"

