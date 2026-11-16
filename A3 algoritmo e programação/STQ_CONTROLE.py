
produtos = [] # Lista onde são armazenados os produtos como dicionário.

def cadastrar_produto():
    print("\n--- CADASTRO DE PRODUTO ---")

    codigo = int(input("Digite o código do produto: "))
    if codigo <= 0:
        print("Erro: O código do produto deve ser maior que zero!")
        return

    nome = input("Digite o nome do produto: ")
    if nome == "":
        print("Erro: O nome do produto não pode ficar em branco!")
        return

    for produto in produtos:
        if produto["codigo"] == codigo:
            print("Erro: Já existe um produto cadastrado com esse código!")
            return
        if produto["nome"].lower() == nome.lower():
            print("Erro: Já existe um produto cadastrado com o nome", produto["nome"])
            return

    valor = float(input("Digite o valor unitário (R$): "))
    if valor <= 0:
        print("Erro: O valor do produto deve ser maior que zero!")
        return

    estoque = int(input("Digite a quantidade inicial em estoque: "))
    if estoque < 0:
        print("Erro: A quantidade em estoque não pode ser menor que zero!")
        return

    novo_produto = {
        "codigo": codigo,
        "nome": nome,
        "valor": valor,
        "estoque": estoque
    }

    produtos.append(novo_produto)
    print("Sucesso! Produto", nome, "cadastrado com sucesso.")


def listar_produtos():
    print("\n--- CONSULTA DE ESTOQUE ---")

    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    for produto in produtos:
        print("Código:", produto["codigo"], "| Nome:", produto["nome"], "| Preço: R$", produto["valor"], "| Estoque:", produto["estoque"])


# Listas de clientes e vendedores
clientes = []
vendedores = []


def cadastrar_cliente():
    print("\n--- CADASTRO DE CLIENTE ---")

    try:
        codigo = int(input("Digite o código do cliente: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro!")
        return

    if codigo <= 0:
        print("Erro: O código do cliente deve ser maior que zero!")
        return

    nome = input("Digite o nome do cliente: ").strip()

    if nome == "":
        print("Erro: O nome não pode ficar em branco!")
        return

    for cliente in clientes:
        if cliente["codigo"] == codigo:
            print("Erro: Já existe um cliente com esse código!")
            return

        if cliente["nome"].lower() == nome.lower():
            print("Erro: Esse cliente já está cadastrado!")
            return

    telefone = input("Digite o telefone do cliente: ").strip()

    if telefone == "":
        print("Erro: O telefone não pode ficar em branco!")
        return

    novo_cliente = {
        "codigo": codigo,
        "nome": nome,
        "telefone": telefone
    }

    clientes.append(novo_cliente)

    print("Sucesso! Cliente", nome, "cadastrado com sucesso.")


def listar_clientes():
    print("\n--- CONSULTA DE CLIENTES ---")

    if not clientes:
        print("Nenhum cliente cadastrado no momento.")
        return

    for cliente in clientes:
        print("Código:", cliente["codigo"], "| Nome:", cliente["nome"], "| Telefone:", cliente["telefone"])


def cadastrar_vendedor():
    print("\n--- CADASTRO DE VENDEDOR ---")

    try:
        codigo = int(input("Digite o código do vendedor: "))
    except ValueError:
        print("Erro: O código deve ser um número inteiro!")
        return

    if codigo <= 0:
        print("Erro: O código do vendedor deve ser maior que zero!")
        return

    nome = input("Digite o nome do vendedor: ").strip()

    if nome == "":
        print("Erro: O nome não pode ficar em branco!")
        return

    for vendedor in vendedores:
        if vendedor["codigo"] == codigo:
            print("Erro: Já existe um vendedor com esse código!")
            return

        if vendedor["nome"].lower() == nome.lower():
            print("Erro: Esse vendedor já está cadastrado!")
            return

    telefone = input("Digite o telefone do vendedor: ").strip()

    if telefone == "":
        print("Erro: O telefone não pode ficar em branco!")
        return

    novo_vendedor = {
        "codigo": codigo,
        "nome": nome,
        "telefone": telefone
    }

    vendedores.append(novo_vendedor)

    print("Sucesso! Vendedor", nome, "cadastrado com sucesso.")


def listar_vendedores():
    print("\n--- CONSULTA DE VENDEDORES ---")

    if not vendedores:
        print("Nenhum vendedor cadastrado no momento.")
        return

    for vendedor in vendedores:
        print("Código:", vendedor["codigo"], "| Nome:", vendedor["nome"], "| Telefone:", vendedor["telefone"])


# MENU PRINCIPAL
def menu_estoque():
    while True:
        print("\n=== SISTEMA DE CADASTRO ===")
        print("1. Cadastrar Produto")
        print("2. Consultar Estoque")
        print("3. Cadastrar Cliente")
        print("4. Consultar Clientes")
        print("5. Cadastrar Vendedor")
        print("6. Consultar Vendedores")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            cadastrar_cliente()

        elif opcao == "4":
            listar_clientes()

        elif opcao == "5":
            cadastrar_vendedor()

        elif opcao == "6":
            listar_vendedores()

        elif opcao == "7":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Escolha entre 1 e 7.")


# Inicia o menu principal
menu_estoque()
