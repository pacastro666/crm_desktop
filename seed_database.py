"""
Script para popular o banco de dados com dados de exemplo
"""
import random
from datetime import datetime, date, timedelta
from core.database import DatabaseManager
from core.migrations import Migrations
from models.cliente import Cliente
from models.oportunidade import Oportunidade
from models.tarefa import Tarefa
from services.cliente_service import ClienteService
from services.oportunidade_service import OportunidadeService
from services.tarefa_service import TarefaService
from repositories.cliente_repository import ClienteRepository
from repositories.oportunidade_repository import OportunidadeRepository
from repositories.tarefa_repository import TarefaRepository
from repositories.interacao_repository import InteracaoRepository

# Dados para geração aleatória
NOMES = [
    "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Souza",
    "Juliana Ferreira", "Roberto Alves", "Fernanda Lima", "Ricardo Martins", "Patricia Rocha",
    "Marcos Pereira", "Camila Rodrigues", "Bruno Carvalho", "Larissa Gomes", "Felipe Araújo",
    "Amanda Ribeiro", "Thiago Barbosa", "Beatriz Nunes", "Gustavo Moreira", "Isabela Castro",
    "Rafael Dias", "Mariana Cardoso", "Lucas Freitas", "Gabriela Azevedo", "Diego Correia",
    "Renata Mendes", "André Teixeira", "Vanessa Monteiro", "Rodrigo Ramos", "Tatiana Lopes",
    "Eduardo Moura", "Priscila Farias", "Henrique Barros", "Daniela Cunha", "Vinicius Pires",
    "Juliana Machado", "Leandro Rezende", "Bianca Melo", "Fábio Coelho", "Carla Xavier",
    "Alexandre Nascimento", "Natália Tavares", "Igor Sampaio", "Leticia Guimarães", "Paulo Henrique",
    "Renata Duarte", "Marcelo Vasconcelos", "Sabrina Andrade", "Leonardo Campos", "Adriana Brito"
]

EMPRESAS = [
    "Tech Solutions", "Inovação Digital", "Global Corp", "Mega Sistemas", "SoftTech",
    "Data Analytics", "Cloud Services", "Smart Business", "Future Tech", "Digital Solutions",
    "Info Systems", "Net Solutions", "Prime Tech", "Elite Software", "Advanced Systems",
    "Tech Innovations", "Digital Works", "Smart Solutions", "Pro Systems", "Next Gen Tech",
    "Alpha Technologies", "Beta Solutions", "Gamma Systems", "Delta Tech", "Omega Digital",
    "Prime Solutions", "Elite Corp", "Premium Tech", "Master Systems", "Ultra Solutions"
]

CIDADES_ESTADOS = [
    ("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Belo Horizonte", "MG"),
    ("Brasília", "DF"), ("Salvador", "BA"), ("Curitiba", "PR"), ("Porto Alegre", "RS"),
    ("Recife", "PE"), ("Fortaleza", "CE"), ("Manaus", "AM"), ("Belém", "PA"),
    ("Goiânia", "GO"), ("Campinas", "SP"), ("São Luís", "MA"), ("Maceió", "AL"),
    ("Natal", "RN"), ("João Pessoa", "PB"), ("Aracaju", "SE"), ("Florianópolis", "SC"),
    ("Vitória", "ES"), ("Cuiabá", "MT"), ("Campo Grande", "MS"), ("Teresina", "PI")
]

BAIRROS = [
    "Centro", "Jardim das Flores", "Vila Nova", "Parque Industrial", "Alto da Boa Vista",
    "Bela Vista", "Jardim América", "Vila Mariana", "Moema", "Itaim Bibi",
    "Pinheiros", "Vila Madalena", "Barra da Tijuca", "Copacabana", "Ipanema",
    "Leblon", "Botafogo", "Flamengo", "Tijuca", "Barra Funda"
]

TIPOS_TAREFA = ["Ligação", "Email", "Reunião", "WhatsApp", "Visita", "Outro"]
PRIORIDADES = ["Baixa", "Média", "Alta"]
ETAPAS = ["Lead", "Qualificação", "Proposta", "Negociação", "Fechado", "Perdido"]


def gerar_telefone():
    """Gera um telefone aleatório"""
    ddd = random.randint(11, 99)
    numero = random.randint(900000000, 999999999)
    return f"({ddd}) {numero // 10000}-{numero % 10000:04d}"


def gerar_email(nome):
    """Gera email baseado no nome"""
    # Remove acentos e caracteres especiais
    nome_limpo = nome.lower()
    nome_limpo = nome_limpo.replace(" ", ".")
    nome_limpo = nome_limpo.replace("ã", "a").replace("á", "a").replace("â", "a").replace("à", "a")
    nome_limpo = nome_limpo.replace("é", "e").replace("ê", "e")
    nome_limpo = nome_limpo.replace("í", "i")
    nome_limpo = nome_limpo.replace("ó", "o").replace("ô", "o").replace("õ", "o")
    nome_limpo = nome_limpo.replace("ú", "u").replace("ü", "u")
    nome_limpo = nome_limpo.replace("ç", "c")
    # Remove qualquer caractere que não seja letra, número ou ponto
    nome_limpo = ''.join(c for c in nome_limpo if c.isalnum() or c == '.')
    dominios = ["gmail.com", "hotmail.com", "yahoo.com.br", "outlook.com", "empresa.com.br"]
    return f"{nome_limpo}@{random.choice(dominios)}"


def gerar_cpf_valido():
    """Gera um CPF válido"""
    # Gera 9 dígitos aleatórios
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    # Calcula primeiro dígito verificador
    soma = sum(cpf[i] * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    cpf.append(digito1)
    
    # Calcula segundo dígito verificador
    soma = sum(cpf[i] * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    cpf.append(digito2)
    
    return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"


def gerar_cnpj_valido():
    """Gera um CNPJ válido"""
    # Gera 12 dígitos aleatórios
    cnpj = [random.randint(0, 9) for _ in range(12)]
    
    # Calcula primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(cnpj[i] * pesos1[i] for i in range(12))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    cnpj.append(digito1)
    
    # Calcula segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(cnpj[i] * pesos2[i] for i in range(13))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    cnpj.append(digito2)
    
    return f"{cnpj[0]}{cnpj[1]}.{cnpj[2]}{cnpj[3]}{cnpj[4]}.{cnpj[5]}{cnpj[6]}{cnpj[7]}/{cnpj[8]}{cnpj[9]}{cnpj[10]}{cnpj[11]}-{cnpj[12]}{cnpj[13]}"


def gerar_cnpj_cpf():
    """Gera CPF ou CNPJ válido"""
    if random.random() < 0.7:  # 70% CPF
        return gerar_cpf_valido()
    else:  # 30% CNPJ
        return gerar_cnpj_valido()


def gerar_cep():
    """Gera CEP aleatório"""
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"


def inicializar_banco():
    """Inicializa o banco de dados"""
    print("Inicializando banco de dados...")
    
    if not DatabaseManager.create_connection_pool():
        print("ERRO: Não foi possível criar pool de conexões")
        return False
    
    if not DatabaseManager.test_connection():
        print("ERRO: Não foi possível conectar ao banco de dados")
        return False
    
    if not Migrations.run_migrations():
        print("ERRO: Falha ao executar migrações")
        return False
    
    return True


def popular_dados():
    """Popula o banco com dados de exemplo"""
    print("\n=== Populando banco de dados com dados de exemplo ===\n")
    
    # Inicializar banco
    if not inicializar_banco():
        return
    
    # Criar repositories e services
    cliente_repo = ClienteRepository()
    oportunidade_repo = OportunidadeRepository()
    tarefa_repo = TarefaRepository()
    interacao_repo = InteracaoRepository()
    
    cliente_service = ClienteService(cliente_repo, interacao_repo)
    oportunidade_service = OportunidadeService(oportunidade_repo, interacao_repo)
    tarefa_service = TarefaService(tarefa_repo, interacao_repo)
    
    # Gerar clientes (40 clientes)
    print("Criando 40 clientes...")
    clientes_ids = []
    
    for i in range(40):
        nome = random.choice(NOMES)
        cidade, estado = random.choice(CIDADES_ESTADOS)
        
        cliente = Cliente(
            nome=nome,
            email=gerar_email(nome),
            telefone=gerar_telefone(),
            empresa=random.choice(EMPRESAS),
            cnpj_cpf=gerar_cnpj_cpf(),
            endereco_rua=f"Rua {random.choice(['das Flores', 'Principal', 'Comercial', 'Industrial', 'Central'])}",
            endereco_numero=str(random.randint(10, 9999)),
            endereco_bairro=random.choice(BAIRROS),
            endereco_cidade=cidade,
            endereco_estado=estado,
            endereco_cep=gerar_cep(),
            observacoes=f"Cliente gerado automaticamente - {random.choice(['Potencial', 'Ativo', 'Inativo', 'VIP'])}"
        )
        
        try:
            cliente_id = cliente_service.criar_cliente(cliente)
            clientes_ids.append(cliente_id)
            if (i + 1) % 10 == 0:
                print(f"  [OK] {i + 1} clientes criados...")
        except Exception as e:
            print(f"  [ERRO] Erro ao criar cliente {i + 1}: {e}")
    
    print(f"[OK] {len(clientes_ids)} clientes criados com sucesso!\n")
    
    # Gerar oportunidades (35 oportunidades)
    print("Criando 35 oportunidades...")
    oportunidades_criadas = 0
    
    # Distribuição de etapas (mais abertas, menos fechadas/perdidas)
    etapas_distribuidas = (
        ["Lead"] * 10 + 
        ["Qualificação"] * 8 + 
        ["Proposta"] * 7 + 
        ["Negociação"] * 6 + 
        ["Fechado"] * 3 + 
        ["Perdido"] * 1
    )
    random.shuffle(etapas_distribuidas)
    
    for i in range(35):
        cliente_id = random.choice(clientes_ids)
        etapa = etapas_distribuidas[i] if i < len(etapas_distribuidas) else random.choice(["Lead", "Qualificação", "Proposta", "Negociação"])
        
        # Valor baseado na etapa
        if etapa == "Fechado":
            valor_base = random.randint(5000, 100000)
        elif etapa == "Perdido":
            valor_base = random.randint(1000, 20000)
        else:
            valor_base = random.randint(2000, 50000)
        
        # Probabilidade baseada na etapa
        probabilidades = {
            "Lead": (10, 30),
            "Qualificação": (30, 50),
            "Proposta": (50, 70),
            "Negociação": (70, 90),
            "Fechado": (100, 100),
            "Perdido": (0, 0)
        }
        prob_min, prob_max = probabilidades[etapa]
        probabilidade = random.randint(prob_min, prob_max)
        
        # Data prevista - sempre futuro para passar na validação
        # Para oportunidades fechadas/perdidas, usar data recente mas futura
        if etapa in ["Fechado", "Perdido"]:
            # Usar data de hoje ou futuro próximo (para passar validação)
            dias = random.randint(0, 30)
        else:
            dias = random.randint(1, 90)  # Futuro
        
        data_fechamento = date.today() + timedelta(days=dias)
        
        oportunidade = Oportunidade(
            cliente_id=cliente_id,
            titulo=f"Oportunidade {random.choice(['Venda', 'Contrato', 'Projeto', 'Serviço'])} - {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])}",
            etapa=etapa,
            valor=valor_base,
            probabilidade=probabilidade,
            data_prevista_fechamento=data_fechamento,
            responsavel=random.choice(NOMES),
            observacoes=f"Oportunidade gerada automaticamente - {random.choice(['Alta prioridade', 'Média prioridade', 'Baixa prioridade'])}"
        )
        
        try:
            oportunidade_id = oportunidade_service.criar_oportunidade(oportunidade)
            oportunidades_criadas += 1
            if oportunidades_criadas % 10 == 0:
                print(f"  [OK] {oportunidades_criadas} oportunidades criadas...")
        except Exception as e:
            print(f"  [ERRO] Erro ao criar oportunidade {i + 1}: {e}")
    
    print(f"[OK] {oportunidades_criadas} oportunidades criadas com sucesso!\n")
    
    # Gerar tarefas (25 tarefas)
    print("Criando 25 tarefas...")
    tarefas_criadas = 0
    
    for i in range(25):
        cliente_id = random.choice(clientes_ids)
        tipo = random.choice(TIPOS_TAREFA)
        prioridade = random.choice(PRIORIDADES)
        
        # Data/hora (algumas no passado, algumas no futuro)
        if random.random() < 0.3:  # 30% atrasadas
            dias = random.randint(-30, -1)
            status = "Pendente"
        elif random.random() < 0.5:  # 20% concluídas
            dias = random.randint(-60, -1)
            status = "Concluída"
        else:  # 50% futuras
            dias = random.randint(1, 30)
            status = "Pendente"
        
        data_tarefa = datetime.now() + timedelta(days=dias)
        hora = random.randint(8, 18)
        minuto = random.choice([0, 15, 30, 45])
        data_tarefa = data_tarefa.replace(hour=hora, minute=minuto)
        
        tarefa = Tarefa(
            cliente_id=cliente_id,
            descricao=f"{tipo} com cliente - {random.choice(['Follow-up', 'Apresentação', 'Negociação', 'Suporte', 'Reunião'])}",
            tipo=tipo,
            data_hora=data_tarefa,
            status=status,
            prioridade=prioridade,
            observacoes=f"Tarefa gerada automaticamente - {random.choice(['Urgente', 'Importante', 'Rotina'])}"
        )
        
        try:
            tarefa_id = tarefa_service.criar_tarefa(tarefa)
            tarefas_criadas += 1
            if tarefas_criadas % 10 == 0:
                print(f"  [OK] {tarefas_criadas} tarefas criadas...")
        except Exception as e:
            print(f"  [ERRO] Erro ao criar tarefa {i + 1}: {e}")
    
    print(f"[OK] {tarefas_criadas} tarefas criadas com sucesso!\n")
    
    # Resumo
    total = len(clientes_ids) + oportunidades_criadas + tarefas_criadas
    print("=" * 50)
    print("RESUMO DA POPULAÇÃO:")
    print(f"  • Clientes: {len(clientes_ids)}")
    print(f"  • Oportunidades: {oportunidades_criadas}")
    print(f"  • Tarefas: {tarefas_criadas}")
    print(f"  • TOTAL: {total} registros")
    print("=" * 50)
    print("\n[OK] Banco de dados populado com sucesso!")


if __name__ == "__main__":
    try:
        popular_dados()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n\nERRO: {e}")
        import traceback
        traceback.print_exc()

