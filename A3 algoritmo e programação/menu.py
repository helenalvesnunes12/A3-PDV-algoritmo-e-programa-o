from datetime import datetime

produtos = []  # Lista onde são armazenados os produtos como dicionário.


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


# ---------------------------------------------------------------
# RELATÓRIOS
# Cada função monta o relatório como uma lista de linhas de texto,
# assim ele pode ser exibido na tela e também salvo em arquivo.
# ---------------------------------------------------------------
LINHA = "=" * 60


def montar_relatorio_produtos():
    linhas = ["RELATÓRIO DE PRODUTOS", LINHA]

    if not produtos:
        linhas.append("Nenhum produto cadastrado.")
        return linhas

    total_unidades = 0
    valor_total = 0.0

    for p in produtos:
        subtotal = p["valor"] * p["estoque"]
        total_unidades += p["estoque"]
        valor_total += subtotal
        linhas.append(
            f"Cód: {p['codigo']} | {p['nome']} | "
            f"Preço: R$ {p['valor']:.2f} | Estoque: {p['estoque']} | "
            f"Subtotal: R$ {subtotal:.2f}"
        )

    sem_estoque = [p["nome"] for p in produtos if p["estoque"] == 0]
    mais_caro = max(produtos, key=lambda p: p["valor"])

    linhas.append(LINHA)
    linhas.append(f"Total de produtos cadastrados: {len(produtos)}")
    linhas.append(f"Total de unidades em estoque: {total_unidades}")
    linhas.append(f"Valor total em estoque: R$ {valor_total:.2f}")
    linhas.append(f"Produto mais caro: {mais_caro['nome']} (R$ {mais_caro['valor']:.2f})")
    if sem_estoque:
        linhas.append("Produtos sem estoque: " + ", ".join(sem_estoque))
    else:
        linhas.append("Produtos sem estoque: nenhum")

    return linhas


def montar_relatorio_pessoas(titulo, lista):
    """Relatório genérico para clientes e vendedores."""
    linhas = [titulo, LINHA]

    if not lista:
        linhas.append("Nenhum registro cadastrado.")
        return linhas

    for pessoa in sorted(lista, key=lambda x: x["nome"].lower()):
        linhas.append(
            f"Cód: {pessoa['codigo']} | {pessoa['nome']} | Tel: {pessoa['telefone']}"
        )

    linhas.append(LINHA)
    linhas.append(f"Total de registros: {len(lista)}")
    return linhas


def montar_relatorio_geral():
    valor_total = sum(p["valor"] * p["estoque"] for p in produtos)
    unidades = sum(p["estoque"] for p in produtos)

    return [
        "RELATÓRIO GERAL DO SISTEMA",
        LINHA,
        f"Produtos cadastrados: {len(produtos)}",
        f"Unidades em estoque: {unidades}",
        f"Valor total em estoque: R$ {valor_total:.2f}",
        f"Clientes cadastrados: {len(clientes)}",
        f"Vendedores cadastrados: {len(vendedores)}",
    ]


def exibir_e_salvar_relatorio(linhas):
    agora = datetime.now()
    cabecalho = [f"Gerado em: {agora.strftime('%d/%m/%Y %H:%M:%S')}", ""]
    conteudo = cabecalho + linhas

    print()
    for linha in conteudo:
        print(linha)

    salvar = input("\nDeseja salvar o relatório em arquivo .txt? (s/n): ").strip().lower()
    if salvar == "s":
        nome_arquivo = "relatorio_" + agora.strftime("%Y%m%d_%H%M%S") + ".txt"
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("\n".join(conteudo))
            print("Relatório salvo em:", nome_arquivo)
        except OSError:
            print("Erro: Não foi possível salvar o arquivo!")


def menu_relatorios():
    while True:
        print("\n=== GERAR RELATÓRIO ===")
        print("1. Relatório de Produtos / Estoque")
        print("2. Relatório de Clientes")
        print("3. Relatório de Vendedores")
        print("4. Relatório Geral")
        print("5. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_e_salvar_relatorio(montar_relatorio_produtos())

        elif opcao == "2":
            exibir_e_salvar_relatorio(
                montar_relatorio_pessoas("RELATÓRIO DE CLIENTES", clientes))

        elif opcao == "3":
            exibir_e_salvar_relatorio(
                montar_relatorio_pessoas("RELATÓRIO DE VENDEDORES", vendedores))

        elif opcao == "4":
            exibir_e_salvar_relatorio(montar_relatorio_geral())

        elif opcao == "5":
            break

        else:
            print("Opção inválida! Escolha entre 1 e 5.")


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
        print("7. Gerar Relatório")
        print("8. Sair")

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
            menu_relatorios()

        elif opcao == "8":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Escolha entre 1 e 8.")


# Inicia o menu principal
menu_estoque()