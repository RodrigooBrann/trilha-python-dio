import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import textwrap
from rich import print
from rich.table import Table
from rich.panel import Panel


def depositar():
    try:
        valor = float(entry_valor.get())
        if valor > 0:
            global saldo, extrato
            saldo, extrato = depositar_logica(saldo, valor, extrato)
            atualizar_extrato_label()
            entry_valor.delete(0, tk.END)
            messagebox.showinfo("Depósito", "Depósito realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um valor positivo.")
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número válido.")


def sacar():
    try:
        valor = float(entry_valor.get())
        if valor > 0:
            global saldo, extrato, numero_saques
            saldo, extrato = sacar_logica(
                saldo,
                valor,
                extrato,
                limite,
                numero_saques,
                LIMITE_SAQUES,
            )
            atualizar_extrato_label()
            entry_valor.delete(0, tk.END)
            messagebox.showinfo("Saque", "Saque realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um valor positivo.")
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número válido.")


def exibir_extrato():
    def fechar_janela():
        janela_extrato.destroy()

    janela_extrato = tk.Toplevel(root)
    janela_extrato.title("Extrato")
    janela_extrato.geometry("400x300")

    extrato_text = tk.Text(janela_extrato, wrap=tk.WORD)
    extrato_text.pack(expand=True, fill="both")
    extrato_text.insert(tk.END, extrato)
    extrato_text.config(state=tk.DISABLED)

    button_fechar = tk.Button(janela_extrato, text="Fechar", command=fechar_janela)
    button_fechar.pack()


def criar_usuario():
    def salvar_usuario():
        try:
            cpf = entry_cpf.get()
            nome = entry_nome.get()
            data_nascimento = entry_data_nascimento.get()
            endereco = entry_endereco.get()
            if not (cpf and nome and data_nascimento and endereco):
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            global usuarios
            criar_usuario_logica(usuarios)
            janela_usuario.destroy()
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")

    janela_usuario = tk.Toplevel(root)
    janela_usuario.title("Criar Usuário")

    label_cpf = tk.Label(janela_usuario, text="CPF:")
    label_cpf.grid(row=0, column=0, padx=5, pady=5)

    entry_cpf = tk.Entry(janela_usuario)
    entry_cpf.grid(row=0, column=1, padx=5, pady=5)

    label_nome = tk.Label(janela_usuario, text="Nome:")
    label_nome.grid(row=1, column=0, padx=5, pady=5)

    entry_nome = tk.Entry(janela_usuario)
    entry_nome.grid(row=1, column=1, padx=5, pady=5)

    label_data_nascimento = tk.Label(janela_usuario, text="Data de Nascimento:")
    label_data_nascimento.grid(row=2, column=0, padx=5, pady=5)

    entry_data_nascimento = tk.Entry(janela_usuario)
    entry_data_nascimento.grid(row=2, column=1, padx=5, pady=5)

    label_endereco = tk.Label(janela_usuario, text="Endereço:")
    label_endereco.grid(row=3, column=0, padx=5, pady=5)

    entry_endereco = tk.Entry(janela_usuario)
    entry_endereco.grid(row=3, column=1, padx=5, pady=5)

    button_salvar = tk.Button(janela_usuario, text="Salvar", command=salvar_usuario)
    button_salvar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


def criar_conta():
    def salvar_conta():
        try:
            cpf = entry_cpf_conta.get()
            if not cpf:
                messagebox.showerror("Erro", "Preencha o CPF do usuário.")
                return
            global usuarios, contas
            conta = criar_conta_logica(AGENCIA, len(contas) + 1, usuarios)
            if conta:
                contas.append(conta)
                janela_conta.destroy()
                messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar conta: {e}")

    janela_conta = tk.Toplevel(root)
    janela_conta.title("Criar Conta")

    label_cpf_conta = tk.Label(janela_conta, text="CPF do Usuário:")
    label_cpf_conta.grid(row=0, column=0, padx=5, pady=5)

    entry_cpf_conta = tk.Entry(janela_conta)
    entry_cpf_conta.grid(row=0, column=1, padx=5, pady=5)

    button_salvar_conta = tk.Button(janela_conta, text="Salvar", command=salvar_conta)
    button_salvar_conta.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def listar_contas():
    listar_contas_logica(contas)


def atualizar_extrato_label():
    label_extrato.config(text=f"Extrato:\n{extrato}\nSaldo: R$ {saldo:.2f}")


def depositar_logica(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(Panel(f"=== Depósito realizado com sucesso! ===", expand=False))
    else:
        print(Panel("@@@ Operação falhou! O valor informado é inválido. @@@", expand=False, style="bold red"))
    return saldo, extrato


def sacar_logica(saldo, valor, extrato, limite, numero_saques, limite_saques):
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


def exibir_extrato_logica(saldo, /, *, extrato):
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


def criar_usuario_logica(usuarios):
    cpf = entry_cpf.get()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Panel("@@@ Já existe usuário com esse CPF! @@@", expand=False, style="bold red"))
        return

    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    endereco = entry_endereco.get()

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(Panel("=== Usuário criado com sucesso! ===", expand=False))


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta_logica(agencia, numero_conta, usuarios):
    cpf = entry_cpf_conta.get()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Panel("=== Conta criada com sucesso! ===", expand=False))
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(Panel("@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@", expand=False, style="bold red"))


def listar_contas_logica(contas):
    table = Table(title="Contas")
    table.add_column("Agência", style="cyan", no_wrap=True)
    table.add_column("Conta", style="cyan", no_wrap=True)
    table.add_column("Titular", style="cyan", no_wrap=True)

    for conta in contas:
        table.add_row(conta['agencia'], conta['numero_conta'], conta['usuario']['nome'])

    print(table)


# Inicialização do Tkinter
root = tk.Tk()
root.title("Banco Python")

# Variáveis globais
LIMITE_SAQUES = 3
AGENCIA = "0001"
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []
contas = []

# Frame para o menu
menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# Botões do menu
button_depositar = tk.Button(menu_frame, text="Depositar", command=depositar, width=10)
button_depositar.pack(side=tk.LEFT, padx=5)

button_sacar = tk.Button(menu_frame, text="Sacar", command=sacar, width=10)
button_sacar.pack(side=tk.LEFT, padx=5)

button_extrato = tk.Button(menu_frame, text="Extrato", command=exibir_extrato, width=10)
button_extrato.pack(side=tk.LEFT, padx=5)

button_criar_usuario = tk.Button(menu_frame, text="Novo Usuário", command=criar_usuario, width=10)
button_criar_usuario.pack(side=tk.LEFT, padx=5)

button_criar_conta = tk.Button(menu_frame, text="Nova Conta", command=criar_conta, width=10)
button_criar_conta.pack(side=tk.LEFT, padx=5)

button_listar_contas = tk.Button(menu_frame, text="Listar Contas", command=listar_contas, width=10)
button_listar_contas.pack(side=tk.LEFT, padx=5)

# Frame para o valor
valor_frame = tk.Frame(root)
valor_frame.pack(pady=10)

label_valor = tk.Label(valor_frame, text="Valor:")
label_valor.pack(side=tk.LEFT)

entry_valor = tk.Entry(valor_frame)
entry_valor.pack(side=tk.LEFT, padx=5)

# Frame para o extrato
extrato_frame = tk.Frame(root)
extrato_frame.pack(pady=10)

label_extrato = tk.Label(extrato_frame, text="Extrato:\nSaldo: R$ 0.00")
label_extrato.pack()

# Atualiza o extrato inicialmente
atualizar_extrato_label()

root.mainloop()
