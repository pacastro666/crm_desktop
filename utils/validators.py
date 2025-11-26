"""
Validações diversas (email, CPF, CNPJ, telefone)
"""
import re


class Validators:
    """Classe com métodos de validação"""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida CPF usando algoritmo de dígitos verificadores"""
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = 11 - (soma % 11)
        if digito1 >= 10:
            digito1 = 0
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = 11 - (soma % 11)
        if digito2 >= 10:
            digito2 = 0
        
        # Verifica se os dígitos calculados correspondem aos informados
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Valida CNPJ usando algoritmo de dígitos verificadores"""
        # Remove caracteres não numéricos
        cnpj = re.sub(r'\D', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcula primeiro dígito verificador
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        digito1 = 11 - (soma % 11)
        if digito1 >= 10:
            digito1 = 0
        
        # Calcula segundo dígito verificador
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        digito2 = 11 - (soma % 11)
        if digito2 >= 10:
            digito2 = 0
        
        # Verifica se os dígitos calculados correspondem aos informados
        return int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2
    
    @staticmethod
    def validar_cpf_cnpj(documento: str) -> bool:
        """Valida CPF ou CNPJ"""
        documento = re.sub(r'\D', '', documento)
        if len(documento) == 11:
            return Validators.validar_cpf(documento)
        elif len(documento) == 14:
            return Validators.validar_cnpj(documento)
        return False
    
    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida formato de telefone (aceita vários formatos)"""
        if not telefone:
            return False
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'\D', '', telefone)
        # Aceita telefones com 10 ou 11 dígitos (fixo ou celular)
        return len(telefone_limpo) in [10, 11]
    
    @staticmethod
    def validar_cep(cep: str) -> bool:
        """Valida formato de CEP"""
        if not cep:
            return False
        cep_limpo = re.sub(r'\D', '', cep)
        return len(cep_limpo) == 8

