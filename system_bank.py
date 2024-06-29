from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

saldo = 0
limite = 500
AGENCIA = "0001"
numero_saques = 0
LIMITE_SAQUES = 3
cpfs = []
extrato = []
usuarios = []
contas = []

GREEN = '\033[32m'  # Verde
RED = '\033[31m'    # Vermelho
YELLOW = '\033[33m'  # Amarelo
BOLD = '\033[1m'    # Negrito
RESET = '\033[0m'   # Reseta a formatação

def validar_usuario(lista, cpf_desejado):
    for pessoa in lista:
        if pessoa['CPF'] == cpf_desejado: return pessoa
    print(f"{RED}Usuário não encontrado, retornando ao menu!{RESET}")
    return None

def validar_conta(cpf):
    for conta in contas:
        if conta['usuario_cpf'] == cpf: return True

def listar_contas(contas):
    if not contas: 
        return print(f"{YELLOW}Não há contas cadastradas.{RESET}")
    lista = [f"Agência: {conta['agencia']}\nC/C: {conta['numero_conta']}\nTitular: {conta['usuario']}" for conta in contas]
    return print(f"{'='*15} Lista de Contas {'='*16}\n{"\n\n".join(lista)}\n{'='*50}")

def criar_conta(agencia):
    user = validar_usuario(usuarios, int(input("Digite seu CPF (apenas números): ")))
    if user:
        if validar_conta(user['CPF']):
            print(f"{YELLOW}Usuário já possui uma conta!{RESET}")
        else:
            print(f"{GREEN}Conta criada com sucesso!!!{RESET}")
            return contas.append({"agencia": agencia, "numero_conta": user['ID'], "usuario": user['Nome'], "usuario_cpf": user['CPF']})

def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append(f"{BOLD}Depósito realizado:{RESET}{' '*20}{datetime.now().strftime('%d %b %Y').upper()}\n{GREEN}+R${valor:.2f}{RESET}\n")
        print(f"{GREEN}Depósito de R${valor:.2f} realizado com sucesso!{RESET}")
    else:
        print(f"{RED}Não é permitido depositar valores negativos ou zero!{RESET}")

def criar_usuario():
    CPF = int(input("Digite seu CPF (apenas números): "))

    if CPF in cpfs:
        criar_usuario() if input(f'{RED}Usuário já cadastro!{RESET}\nTentar novamente?: S/N') == 'S' else menu()
    cpfs.append(CPF)

    usuarios.append({
        "ID": len(usuarios) + 1,
        "Nome" : str(input("Digite seu nome: ")),
        "CPF": CPF,
        "Data Nascimento": str(input("Digite sua data de nascimento (25/12/1995): ")),
        "Endereço": str(input("Digite seu endereço ex:(logradouro, número - bairro - cidade/sigla estado): "))
    })
    print(f"{GREEN}Usuário criado com sucesso!!!{RESET}")

def sacar(valor):
    global numero_saques, LIMITE_SAQUES, saldo, limite 

    if numero_saques >= LIMITE_SAQUES:
        print(f'{RED}Quantidade de {LIMITE_SAQUES} saques permitidos foi excedida!{RESET}')
    elif valor > saldo:
        print(f'{RED}Saldo insuficiente!{RESET}')
    elif valor > limite:
        print(f'{RED}O valor do saque excede o limite de R${limite:.2f}!{RESET}')
    elif valor <= 0:
        print(f'{RED}Não é permitido sacar valores negativos ou zero!{RESET}')
    else:
        saldo -= valor
        numero_saques += 1
        extrato.append(f"{BOLD}Saque realizado:{RESET}{' '*23}{datetime.now().strftime('%d %b %Y').upper()}\n{RED}-R${valor:.2f}{RESET}\n")
        print(f"{GREEN}Saque de R${valor:.2f} realizado com sucesso!{RESET}")

def Extrato():
    print(f"\n{'='*20} Extrato {'='*21}\n")
    if not extrato:
        print(f"{YELLOW}Não foram realizadas movimentações.{RESET}")
    else:
        for item in extrato: print(item)
    print(f"\n{BOLD}Saldo atual:{RESET} R${saldo:.2f}\n{'='*50}")

def menu():
    option = input("""
    [D] = Depositar
    [S] = Sacar
    [U] = Criar Usuário
    [L] = Listar Contas
    [C] = Criar Conta       
    [E] = Extrato
    [Q] = Sair
    
    Selecione a opção desejada: """)
    return option.strip().upper()[0]

def Programa():
    while True:
        option = menu()

        if option == "D":
            depositar(float(input('Qual valor que deseja depositar?: ')))

        elif option == "S":
            sacar(float(input('Qual valor que deseja sacar?: ')))

        elif option == "E":
            Extrato()

        elif option == "L":
            listar_contas(contas)

        elif option == "U":
            criar_usuario()

        elif option == "C":
            criar_conta(AGENCIA)

        elif option == "Q":
            print(f"{BOLD}Obrigado por usar nosso sistema bancário. Até logo!{RESET}")
            break

        else:
            print(f"{RED}Opção '{option}' é inválida! Por favor, selecione novamente a opção desejada.{RESET}")

Programa() 



class Cliente:
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereço):
        super().__init__(endereço)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques > self.limite_saque
        
        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saque:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        
        return False
        
    def __str__(self):
        return f"""
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
        """
    
class Historico():
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
        )
    
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        