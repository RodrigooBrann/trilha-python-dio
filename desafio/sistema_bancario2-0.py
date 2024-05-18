import textwrap
from rich import print
from rich.table import Table
from rich.panel import Panel


def menu():
    menu = """\n
    |================= MENU =================|
    |[1]\tDepositar                        |
    |[2]\tSacar                            |
    |[3]\tExtrato                          |
    |[4]\tNova conta                       |
    |[5]\tListar contas                    |
    |[6]\tNovo usuário                     |
    |[0]\tSair                             |
    |========================================|
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(Panel(f"=== Depósito realizado com sucesso! ===", expand=False))
    else:
        print(Panel("@@@ Operação falhou! O valor informado é inválido. @@@", expand=False, style="bold red"))

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(Panel("@@@ Operação falhou! Você não tem saldo suficiente. @@@", expand=False, style="bold red"))

    elif excedeu_limite:
        print(Panel("@@@ Operação falhou! O valor do saque excede o limite. @@@", expand=False, style="bold red"))

    elif excedeu_saques:
        print(Panel("@@@ Operação falhou! Número máximo de saques excedido. @@@", expand=False, style="bold red"))

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(Panel("=== Saque realizado com sucesso! ===", expand=False))

    else:
        print(Panel("@@@ Operação falhou! O valor informado é inválido. @@@", expand=False, style="bold red"))

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    table = Table(title="EXTRATO")
    table.add_column("Descrição", style="cyan", no_wrap=True)
    table.add_column("Valor", justify="right", style="magenta")

    if not extrato:
        table.add_row("Não foram realizadas movimentações.", "")
    else:
        for linha in extrato.splitlines():
            table.add_row(linha.split(":\t")[0].strip(), linha.split(":\t")[1].strip())

    table.add_row("Saldo", f"R$ {saldo:.2f}")
    print(table)


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Panel("@@@ Já existe usuário com esse CPF! @@@", expand=False, style="bold red"))
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(Panel("=== Usuário criado com sucesso! ===", expand=False))


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Panel("=== Conta criada com sucesso! ===", expand=False))
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(Panel("@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@", expand=False, style="bold red"))


def listar_contas(contas):
    table = Table(title="Contas")
    table.add_column("Agência", style="cyan", no_wrap=True)
    table.add_column("Conta", style="cyan", no_wrap=True)
    table.add_column("Titular", style="cyan", no_wrap=True)

    for conta in contas:
        table.add_row(conta['agencia'], conta['numero_conta'], conta['usuario']['nome'])

    print(table)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print(Panel("Operação inválida, por favor selecione novamente a operação desejada.", expand=False, style="bold red"))


main()
