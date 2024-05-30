from datetime import datetime

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
