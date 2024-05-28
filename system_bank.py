saldo = 0
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato = []

while True:
    option = input("""
    
    [D] = Depositar
    [S] = Sacar
    [E] = Extrato
    [Q] = Sair
    
    """).strip().upper()[0]

    # Opção para realizar Deposito
    if option == "D":
        valor = float(input('Qual valor que deseja depositar?: '))
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: +R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print('Não é permitido depositar valores negativos ou zero!')

    elif option == "S":
        valor = float(input('Qual valor que deseja sacar?: '))
        if numero_saques >= LIMITE_SAQUES:
            print(f'Quantidade de {LIMITE_SAQUES} saques permitidos foi excedida!')
        elif valor > saldo:
            print('Saldo insuficiente!')
        elif valor > limite:
            print(f'O valor do saque excede o limite de R${limite:.2f}!')
        elif valor <= 0:
            print('Não é permitido sacar valores negativos ou zero!')
        else:
            saldo -= valor
            numero_saques += 1
            extrato.append(f"Saque: -R${valor:.2f}")
            print(f"Saque de R${valor:.2f} realizado com sucesso!")

    elif option == "E":
        print("\n====== Extrato ======")
        for item in extrato:
            print("Não foram realizadas movimentações." if not extrato else item)
        print(f"\nSaldo atual: R${saldo:.2f}")
        print("====================")

    elif option == "Q":
        print("Obrigado por usar nosso sistema bancário. Até logo!")
        break

    else:
        print(f"Opção '{option}' é inválida! Por favor, selecione novamente a opção desejada.")
