from classes import ContaCorrente, Deposito, PessoaFisica, Saque

# Funções auxiliares
def validar_usuario(lista, cpf_desejado):
    for pessoa in lista:
        if pessoa.cpf == cpf_desejado:
            return pessoa
    print("Usuário não encontrado, retornando ao menu!")
    return None

def listar_contas(contas):
    if not contas:
        print("Não há contas cadastradas.")
    else:
        for conta in contas:
            print(conta)

# Sistema bancário
def criar_usuario():
    cpf = input("Digite seu CPF (apenas números): ")
    nome = input("Digite seu nome: ")
    data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
    endereco = input("Digite seu endereço: ")
    novo_usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")

def criar_conta():
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = validar_usuario(usuarios, cpf)
    if usuario:
        if any(conta.cliente.cpf == cpf for conta in contas):
            print("Usuário já possui uma conta!")
        else:
            numero_conta = len(contas) + 1
            nova_conta = ContaCorrente(numero_conta, usuario)
            usuario.adicionar_conta(nova_conta)
            contas.append(nova_conta)
            print("Conta criada com sucesso!")

def depositar():
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = validar_usuario(usuarios, cpf)
    if usuario:
        valor = float(input("Qual valor que deseja depositar?: "))
        conta = usuario.contas[0]
        Deposito(valor).registrar(conta)

def sacar():
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = validar_usuario(usuarios, cpf)
    if usuario:
        valor = float(input("Qual valor que deseja sacar?: "))
        conta = usuario.contas[0]
        Saque(valor).registrar(conta)

def extrato():
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = validar_usuario(usuarios, cpf)
    if usuario:
        conta = usuario.contas[0]
        print("\n=== Extrato ===")
        for transacao in conta.historico.transacoes:
            print(f"{transacao['data']} - {transacao['tipo']} - R${transacao['valor']:.2f}")
        print(f"Saldo atual: R${conta.saldo:.2f}")

def menu():
    while True:
        opcao = input("\n[D] Depositar\n[S] Sacar\n[U] Criar Usuário\n[C] Criar Conta\n[L] Listar Contas\n[E] Extrato\n[Q] Sair\nSelecione a opção desejada: ").upper()
        if opcao == "D":
            depositar()
        elif opcao == "S":
            sacar()
        elif opcao == "U":
            criar_usuario()
        elif opcao == "C":
            criar_conta()
        elif opcao == "L":
            listar_contas(contas)
        elif opcao == "E":
            extrato()
        elif opcao == "Q":
            print("Obrigado por usar nosso sistema bancário. Até logo!")
            break
        else:
            print("Opção inválida! Por favor, selecione novamente a opção desejada.")

# Lista de usuários e contas
usuarios = []
contas = []

# Inicia o programa
menu()
