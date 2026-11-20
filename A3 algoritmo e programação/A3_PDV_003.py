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

# ==========================================
# CONTROLE DE ESTOQUE / Feito por Douglas
# ==========================================

def cadastrar_produto():
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

def listar_produtos(): 
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
    
def remover_produto_estoque():
    print("\n--- REMOVER PRODUTO DO ESTOQUE ---")

    # If responsável por verificar se existe algum produto cadastrado.
    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    codigo = input("Digite o código do produto: ").upper()

    # For responsável por percorrer a lista e verificar se o código informado pertence a algum produto.
    for produto in produtos:
        if produto["codigo"] == codigo:
            break
    else:
        print("Erro: Produto não encontrado!")
        return

    print("\nProduto:", produto["nome"])
    print("Quantidade disponível:", produto["estoque"])

    quantidade = int(input("Digite a quantidade que deseja remover: "))

    # If responsável por verificar se a quantidade informada é maior que o estoque disponível.
    if quantidade > produto["estoque"]:
        print("Erro: A quantidade informada é maior que o estoque disponível!")
        return

    # If responsável por verificar se a quantidade informada é maior que zero.
    if quantidade <= 0:
        print("Erro: A quantidade deve ser maior que zero!")
        return

    # Subtrai a quantidade informada do estoque atual do produto.
    produto["estoque"] -= quantidade

    print("\nProduto removido do estoque com sucesso!")
    print("Produto:", produto["nome"])
    print("Quantidade removida:", quantidade)
    print("Estoque restante:", produto["estoque"])

def adicionar_produto_estoque(): 
    print("\n--- ADICIONAR PRODUTO AO ESTOQUE ---")

    # If responsável por verificar se existe algum produto cadastrado.
    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    # Input responsável por receber o código do produto que será atualizado.
    codigo = input("Digite o código do produto: ")

    # For responsável por percorrer a lista e verificar se o código informado pertence a algum produto.
    for produto in produtos:
        if produto["codigo"] == codigo:
            break
    else:
        print("Erro: Produto não encontrado!")
        return

    print("\nProduto:", produto["nome"])
    print("Quantidade disponível:", produto["estoque"])

    quantidade = int(input("Digite a quantidade que deseja adicionar: "))

    # If responsável por verificar se a quantidade informada é maior que zero.
    if quantidade <= 0:
        print("Erro: A quantidade deve ser maior que zero!")
        return

    # Soma a quantidade informada ao estoque atual do produto.
    produto["estoque"] += quantidade

    print("\nProduto adicionado ao estoque com sucesso!")
    print("Produto:", produto["nome"])
    print("Quantidade adicionada:", quantidade)
    print("Estoque atual:", produto["estoque"])

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

    # CARRINHO DE COMPRAS
    carrinho = []

    while True:

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
            continue

        try:
            quantidade = int(input("Quantidade desejada: "))
        except ValueError:
            print("Quantidade invalida!")
            continue

        if quantidade <= 0:
            print("Quantidade deve ser maior que zero!")
            continue

        # VERIFICA SE O PRODUTO JA ESTA NO CARRINHO
        item = next(
            (p for p in carrinho if p["codigo_produto"] == codigo_produto),
            None
        )

        quantidade_carrinho = 0

        if item is not None:
            quantidade_carrinho = item["quantidade"]

        if quantidade + quantidade_carrinho > produto["estoque"]:
            print("Estoque insuficiente!")
            continue

        # ADICIONA OU ATUALIZA O PRODUTO NO CARRINHO
        if item is not None:
            item["quantidade"] += quantidade
        else:
            carrinho.append({
                "produto": produto,
                "codigo_produto": produto["codigo"],
                "nome": produto["nome"],
                "valor_unitario": produto["valor"],
                "quantidade": quantidade,
                "taxa_imposto": produto["taxa_imposto"],
                "taxa_comissao": produto["taxa_comissao"]
            })

        print("Produto adicionado ao carrinho!")

        continuar = input(
            "\nDeseja adicionar outro produto? (S/N): "
        ).strip().upper()

        if continuar != "S":
            break

    if not carrinho:
        print("Carrinho vazio!")
        return

    # RESUMO DO CARRINHO
    print("\n========== RESUMO DO CARRINHO ==========")

    subtotal_geral = 0
    imposto_geral = 0
    comissao_geral = 0

    for item in carrinho:

        subtotal = item["valor_unitario"] * item["quantidade"]
        imposto = subtotal * (item["taxa_imposto"] / 100)
        comissao = subtotal * (item["taxa_comissao"] / 100)

        item["subtotal"] = round(subtotal, 2)
        item["imposto"] = round(imposto, 2)
        item["comissao"] = round(comissao, 2)
        item["total"] = round(subtotal + imposto, 2)

        subtotal_geral += subtotal
        imposto_geral += imposto
        comissao_geral += comissao

        print(f"\nProduto: {item['nome']}")
        print(f"Quantidade: {item['quantidade']}")
        print(f"Valor unitario: R$ {item['valor_unitario']:.2f}")
        print(f"Subtotal: R$ {item['subtotal']:.2f}")
        print(f"Imposto: R$ {item['imposto']:.2f}")

    total_geral = subtotal_geral + imposto_geral

    print("\n-----------------------------------")
    print(f"Subtotal geral: R$ {subtotal_geral:.2f}")
    print(f"Imposto: R$ {imposto_geral:.2f}")
    print(f"Total da compra: R$ {total_geral:.2f}")

    # CONFIRMACAO DA COMPRA
    confirmar = input(
        "\nDeseja confirmar a compra? (S/N): "
    ).strip().upper()

    if confirmar != "S":
        print("Compra cancelada! Carrinho mantido durante esta operacao.")
        return

    # IDENTIFICACAO DO CLIENTE
    listar_clientes()

    codigo_cliente = input(
        "\nCodigo do cliente: "
    ).strip().upper()

    cliente = next(
        (c for c in clientes if c["codigo"] == codigo_cliente),
        None
    )

    if cliente is None:
        print("Cliente nao encontrado! Venda cancelada.")
        return

    # IDENTIFICACAO DO VENDEDOR
    listar_vendedores()

    codigo_vendedor = input(
        "\nCodigo do vendedor: "
    ).strip().upper()

    vendedor = next(
        (v for v in vendedores if v["codigo"] == codigo_vendedor),
        None
    )

    if vendedor is None:
        print("Vendedor nao encontrado! Venda cancelada.")
        return

    # DESCONTO DO ESTOQUE
    for item in carrinho:
        item["produto"]["estoque"] -= item["quantidade"]

    # REGISTRO DA VENDA
    nova_venda = {
        "codigo": len(vendas) + 1,
        "cliente": cliente["nome"],
        "vendedor": vendedor["nome"],
        "itens": carrinho,
        "subtotal": round(subtotal_geral, 2),
        "imposto": round(imposto_geral, 2),
        "total": round(total_geral, 2),
        "comissao": round(comissao_geral, 2)
    }

    vendas.append(nova_venda)

    print("\n========== VENDA FINALIZADA ==========")
    print(f"Cliente: {cliente['nome']}")
    print(f"Vendedor: {vendedor['nome']}")
    print(f"Total: R$ {total_geral:.2f}")
    print(f"Comissao: R$ {comissao_geral:.2f}")
    print("Estoque atualizado com sucesso!")



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
# MENU ESTOQUE
# ==========================================


def menu_estoque():

    while True:

        print("\n========== CONTROLE DE ESTOQUE ==========")

        print("1. Cadastrar Produto")
        print("2. Adicionar Produto ao Estoque")
        print("3. Remover Produto do Estoque")
        print("4. Verificar Estoque")
        print("5. Voltar ao Menu Principal")

        print("=========================================")

        opcao = input("Escolha uma opcao: ").strip()

        match opcao:

            case "1":
                cadastrar_produto()

            case "2":
                adicionar_produto_estoque()

            case "3":
                remover_produto_estoque()

            case "4":
                listar_produtos()

            case "5":
                print("\nVoltando ao menu principal...")
                break

            case _:
                print("Opcao invalida! Escolha entre 1 e 5.")

# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    while True:

        print("\n========== SISTEMA DE VENDAS ==========")

        print("1. Controle de Estoque")
        print("2. Cadastrar Cliente")
        print("3. Consultar Clientes")
        print("4. Cadastrar Vendedor")
        print("5. Consultar Vendedores")
        print("6. Registrar Venda")
        print("7. Consultar Vendas")
        print("8. Fechar Sistema")

        print("=======================================")

        opcao = input("Escolha uma opcao: ").strip()

        match opcao:

            case "1":
                menu_estoque()

            case "2":
                cadastrar_cliente()

            case "3":
                listar_clientes()

            case "4":
                cadastrar_vendedor()

            case "5":
                listar_vendedores()

            case "6":
                registrar_venda()

            case "7":
                listar_vendas()

            case "8":
                print("\nEncerrando o sistema...")
                print("Obrigado por utilizar o sistema!")
                break

            case _:
                print("Opcao invalida! Escolha entre 1 e 8.")

# ==========================================
# INICIAR SISTEMA
# ==========================================

if __name__ == "__main__":
    menu_principal()