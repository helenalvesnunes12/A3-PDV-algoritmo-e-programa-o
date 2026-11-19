import random

# ==========================================
# CONFIGURACOES PADRAO
# ==========================================

TAXA_IMPOSTO_PADRAO = 25.0
TAXA_COMISSAO_PADRAO = 5.0

# ==========================================
# LISTAS DO SISTEMA
# ==========================================

produtos = []
clientes = []
vendedores = []
vendas = []


# ==========================================
# GERACAO AUTOMATICA DE CODIGOS
# ==========================================

def gerar_codigo(lista, prefixo):

    codigos_existentes = {
        item["codigo"] for item in lista
    }

    while True:
        numero = random.randint(1000, 9999)
        codigo = f"{prefixo}{numero}"

        if codigo not in codigos_existentes:
            return codigo


def gerar_codigo_produto():
    return gerar_codigo(produtos, "P")


def gerar_codigo_cliente():
    return gerar_codigo(clientes, "C")


def gerar_codigo_vendedor():
    return gerar_codigo(vendedores, "V")


def cadastrar_produto(): # Feito por Douglas.
    # Função responsável por realizar o cadastro dos produtos, um produto precisa de um código, nome, valor e quantidade 
    # em estoque.
    
    print("\n--- CADASTRO DE PRODUTO ---")
    
    codigo = gerar_codigo_produto()
    print("Código gerado automaticamente:", codigo)

    nome = input("Digite o nome do produto: ")
    if nome == "":
        print("Erro: O nome do produto não pode ficar em branco!")
        return
    
    for produto in produtos:
        # For responsável por verificar a lista e informar se possui um código ou nome repetido.
        if produto["codigo"] == codigo:
            print("Erro: Já existe um produto cadastrado com esse código!")
            return
        if produto["nome"].lower() == nome.lower(): # .lower() Serve para deixar todo o texto em minúsculo, para comparar.
            print("Erro: Já existe um produto cadastrado com o nome", produto["nome"])
            return
    
    valor = float(input("Digite o valor unitário (R$): "))
    # If responsável por védica se o valor do produto e maior que zero.
    if valor <= 0:
        print("Erro: O valor do produto deve ser maior que zero!")
        return

    estoque = int(input("Digite a quantidade inicial em estoque: "))
    # If responsável por verificar se a quantidade do estoque e maior que zero.
    if estoque < 0:
        print("Erro: A quantidade em estoque não pode ser menor que zero!")
        return
    
    # Criação do dicionário do produto.
    novo_produto = {
        "codigo": codigo,
        "nome": nome,
        "valor": valor,
        "estoque": estoque,
        "taxa_imposto": TAXA_IMPOSTO_PADRAO,
        "taxa_comissao": TAXA_COMISSAO_PADRAO
    }
    
    produtos.append(novo_produto)
    print("Produto", nome, "cadastrado com sucesso.")

def listar_produtos(): # Feito por Douglas.
    print("\n--- CONSULTA DE ESTOQUE ---")
    # If responsável por por informar que não possui itens cadastrados.
    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    valor_total_estoque = 0 # Contador do valor bruto investido no estoque.
    
    #For responsável por percorrer a lista para cada produto cadastrado e mostrar o código, nome, preço, quantidade e o valor 
    # somado das unidades mais o valor bruto investido no estoque.
    for produto in produtos:
        valor_total_produto = produto["valor"] * produto["estoque"]

        print("Código:", produto["codigo"], "| Nome:", produto["nome"], "| Preço: R$", produto["valor"], "| Estoque:", produto["estoque"], "| Valor total: R$", f"{valor_total_produto:.2f}")

        valor_total_estoque += valor_total_produto # Soma o valor total das unidades como valor total bruto do estoque.

    print(f"\nValor bruto total do estoque: R$ {valor_total_estoque:.2f}")


# ==========================================
# CADASTRO DE CLIENTES
# ==========================================

def cadastrar_cliente():

    print("\n========== CADASTRO DE CLIENTE ==========")

    nome = input("Nome do cliente (obrigatorio): ").strip()

    if not nome:
        print("O nome e obrigatorio!")
        return

    if any(c["nome"].lower() == nome.lower() for c in clientes):
        print("Cliente ja cadastrado!")
        return

    telefone = input("Telefone (opcional, pressione Enter para pular): ").strip()

    codigo = gerar_codigo_cliente()

    novo_cliente = {
        "codigo": codigo,
        "nome": nome,
        "telefone": telefone if telefone else "Nao informado"
    }

    clientes.append(novo_cliente)

    print("\nCliente cadastrado com sucesso!")
    print("Codigo gerado:", codigo)


def listar_clientes():

    print("\n========== CONSULTA DE CLIENTES ==========")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    for cliente in clientes:

        print(
            "\nCodigo:", cliente["codigo"],
            "| Nome:", cliente["nome"],
            "| Telefone:", cliente["telefone"]
        )


# ==========================================
# CADASTRO DE VENDEDORES
# ==========================================

def cadastrar_vendedor():

    print("\n========== CADASTRO DE VENDEDOR ==========")

    nome = input("Nome do vendedor (obrigatorio): ").strip()

    if not nome:
        print("O nome e obrigatorio!")
        return

    if any(v["nome"].lower() == nome.lower() for v in vendedores):
        print("Vendedor ja cadastrado!")
        return

    telefone = input("Telefone (opcional, pressione Enter para pular): ").strip()

    codigo = gerar_codigo_vendedor()

    novo_vendedor = {
        "codigo": codigo,
        "nome": nome,
        "telefone": telefone if telefone else "Nao informado"
    }

    vendedores.append(novo_vendedor)

    print("\nVendedor cadastrado com sucesso!")
    print("Codigo gerado:", codigo)


def listar_vendedores():

    print("\n========== CONSULTA DE VENDEDORES ==========")

    if not vendedores:
        print("Nenhum vendedor cadastrado.")
        return

    for vendedor in vendedores:

        print(
            "\nCodigo:", vendedor["codigo"],
            "| Nome:", vendedor["nome"],
            "| Telefone:", vendedor["telefone"]
        )


# ==========================================
# REGISTRO DE VENDAS
# ==========================================

def registrar_venda():

    print("\n========== REGISTRO DE VENDA ==========")

    if not produtos or not clientes or not vendedores:
        print("Cadastre pelo menos um produto, cliente e vendedor!")
        return

    listar_produtos()

    codigo_produto = input(
        "\nCodigo do produto: "
    ).strip().upper()

    produto = next(
        (p for p in produtos if p["codigo"] == codigo_produto),
        None
    )

    if produto is None:
        print("Produto nao encontrado!")
        return

    try:
        quantidade = int(input("Quantidade vendida: "))
    except ValueError:
        print("Quantidade invalida!")
        return

    if quantidade <= 0:
        print("Quantidade deve ser maior que zero!")
        return

    if quantidade > produto["estoque"]:
        print("Estoque insuficiente!")
        return

    listar_clientes()

    codigo_cliente = input(
        "\nCodigo do cliente: "
    ).strip().upper()

    cliente = next(
        (c for c in clientes if c["codigo"] == codigo_cliente),
        None
    )

    if cliente is None:
        print("Cliente nao encontrado!")
        return

    listar_vendedores()

    codigo_vendedor = input(
        "\nCodigo do vendedor: "
    ).strip().upper()

    vendedor = next(
        (v for v in vendedores if v["codigo"] == codigo_vendedor),
        None
    )

    if vendedor is None:
        print("Vendedor nao encontrado!")
        return

    # CALCULOS

    valor_unitario = produto["valor"]

    taxa_imposto = produto["taxa_imposto"]
    taxa_comissao = produto["taxa_comissao"]

    subtotal = valor_unitario * quantidade

    imposto = subtotal * (taxa_imposto / 100)

    comissao = subtotal * (taxa_comissao / 100)

    total = subtotal + imposto

    # DESCONTO DO ESTOQUE

    produto["estoque"] -= quantidade

    # REGISTRO

    nova_venda = {

        "codigo": len(vendas) + 1,

        "produto": produto["nome"],
        "codigo_produto": produto["codigo"],

        "cliente": cliente["nome"],
        "vendedor": vendedor["nome"],

        "quantidade": quantidade,

        "valor_unitario": valor_unitario,

        "subtotal": round(subtotal, 2),
        "imposto": round(imposto, 2),
        "taxa_imposto": taxa_imposto,

        "total": round(total, 2),

        "comissao": round(comissao, 2),
        "taxa_comissao": taxa_comissao
    }

    vendas.append(nova_venda)

    # COMPROVANTE

    print("\n========== VENDA REALIZADA ==========")

    print("Codigo da venda:", nova_venda["codigo"])
    print("Produto:", produto["nome"])
    print("Cliente:", cliente["nome"])
    print("Vendedor:", vendedor["nome"])
    print("Quantidade:", quantidade)

    print(f"\nValor unitario: R$ {valor_unitario:.2f}")
    print(f"Subtotal: R$ {subtotal:.2f}")

    print("-------------------------------------")

    print(f"Imposto ({taxa_imposto}%): R$ {imposto:.2f}")
    print(f"TOTAL DA VENDA: R$ {total:.2f}")

    print("-------------------------------------")

    print(f"Comissao ({taxa_comissao}%): R$ {comissao:.2f}")

    print("-------------------------------------")

    print("Estoque restante:", produto["estoque"])

    print("=====================================")


# ==========================================
# CONSULTA DE VENDAS
# ==========================================

def listar_vendas():

    print("\n========== HISTORICO DE VENDAS ==========")

    if not vendas:
        print("Nenhuma venda realizada.")
        return

    for venda in vendas:

        print("\n-----------------------------------------")

        print("Codigo:", venda["codigo"])
        print("Produto:", venda["produto"])
        print("Cliente:", venda["cliente"])
        print("Vendedor:", venda["vendedor"])
        print("Quantidade:", venda["quantidade"])

        print(f"Subtotal: R$ {venda['subtotal']:.2f}")

        print(
            f"Imposto ({venda['taxa_imposto']}%): "
            f"R$ {venda['imposto']:.2f}"
        )

        print(f"Total: R$ {venda['total']:.2f}")

        print(
            f"Comissao ({venda['taxa_comissao']}%): "
            f"R$ {venda['comissao']:.2f}"
        )

    print("\n=========================================")


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_estoque():

    while True:

        print("\n========== SISTEMA DE VENDAS ==========")

        print("1. Cadastrar Produtos")
        print("2. Consultar Estoque")
        print("3. Cadastrar Cliente")
        print("4. Consultar Clientes")
        print("5. Cadastrar Vendedor")
        print("6. Consultar Vendedores")
        print("7. Registrar Venda")
        print("8. Consultar Vendas")
        print("9. Fechar Sistema")

        print("=======================================")

        opcao = input("Escolha uma opcao: ").strip()

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
            registrar_venda()

        elif opcao == "8":
            listar_vendas()

        elif opcao == "9":
            print("\nEncerrando o sistema...")
            print("Obrigado por utilizar o sistema!")
            break

        else:
            print("Opcao invalida! Escolha entre 1 e 9.")


# ==========================================
# INICIAR SISTEMA
# ==========================================

if __name__ == "__main__":
    menu_estoque()
