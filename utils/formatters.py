"""
Formatação de dados (datas, moeda, telefone, CPF/CNPJ)
"""
from datetime import datetime, date
from typing import Optional


class Formatters:
    """Classe com métodos de formatação"""
    
    @staticmethod
    def formatar_moeda(valor: float) -> str:
        """Formata valor como moeda brasileira"""
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @staticmethod
    def formatar_telefone(telefone: str) -> str:
        """Formata telefone para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"""
        if not telefone:
            return ""
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, telefone))
        
        if len(numeros) == 10:  # Telefone fixo
            return f"({numeros[0:2]}) {numeros[2:6]}-{numeros[6:]}"
        elif len(numeros) == 11:  # Celular
            return f"({numeros[0:2]}) {numeros[2:7]}-{numeros[7:]}"
        else:
            return telefone
    
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata CPF para XXX.XXX.XXX-XX"""
        if not cpf:
            return ""
        numeros = ''.join(filter(str.isdigit, cpf))
        if len(numeros) == 11:
            return f"{numeros[0:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        return cpf
    
    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formata CNPJ para XX.XXX.XXX/XXXX-XX"""
        if not cnpj:
            return ""
        numeros = ''.join(filter(str.isdigit, cnpj))
        if len(numeros) == 14:
            return f"{numeros[0:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
        return cnpj
    
    @staticmethod
    def formatar_cep(cep: str) -> str:
        """Formata CEP para XXXXX-XXX"""
        if not cep:
            return ""
        numeros = ''.join(filter(str.isdigit, cep))
        if len(numeros) == 8:
            return f"{numeros[0:5]}-{numeros[5:]}"
        return cep
    
    @staticmethod
    def formatar_data(data: Optional[date]) -> str:
        """Formata data para DD/MM/YYYY"""
        if not data:
            return ""
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, '%Y-%m-%d').date()
            except:
                return data
        return data.strftime('%d/%m/%Y')
    
    @staticmethod
    def formatar_data_hora(data_hora: Optional[datetime]) -> str:
        """Formata data e hora para DD/MM/YYYY HH:MM"""
        if not data_hora:
            return ""
        if isinstance(data_hora, str):
            try:
                data_hora = datetime.fromisoformat(data_hora.replace('Z', '+00:00'))
            except:
                return data_hora
        return data_hora.strftime('%d/%m/%Y %H:%M')
    
    @staticmethod
    def parse_data(data_str: str) -> Optional[date]:
        """Converte string de data para objeto date"""
        if not data_str:
            return None
        try:
            # Tenta vários formatos
            for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                try:
                    return datetime.strptime(data_str, fmt).date()
                except:
                    continue
            return None
        except:
            return None
    
    @staticmethod
    def parse_data_hora(data_hora_str: str) -> Optional[datetime]:
        """Converte string de data/hora para objeto datetime"""
        if not data_hora_str:
            return None
        try:
            # Tenta vários formatos
            for fmt in ['%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']:
                try:
                    return datetime.strptime(data_hora_str, fmt)
                except:
                    continue
            return None
        except:
            return None

