import random
from datetime import date, datetime  # [NOVO] Importa as ferramentas de data usadas na data da venda e nos relatórios por período.

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
        "data": date.today(),  # [NOVO] Guarda a data em que a venda foi realizada.
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

    # [NOVO] Imprime o recibo da venda com a data e os valores individuais de cada produto.
    emitir_recibo(nova_venda)



# ==========================================
# CONSULTA DE VENDAS E RELATORIOS
# ==========================================

# [NOVO] Função que valida o texto digitado (DD/MM/AAAA) e o converte em data, sem usar try/except.
# Devolve a data se for válida ou None se for inválida.
def converter_data(texto):

    partes = texto.split("/")  # Separa o texto pelas barras: dia, mês e ano.

    # If responsável por verificar se o texto tem exatamente 3 partes (dia/mês/ano).
    if len(partes) != 3:
        return None

    dia, mes, ano = partes

    # If responsável por verificar se dia, mês e ano são números e têm o tamanho correto (DD, MM e AAAA).
    if not (dia.isdecimal() and mes.isdecimal() and ano.isdecimal()):
        return None
    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        return None

    dia = int(dia)
    mes = int(mes)
    ano = int(ano)

    # If responsável por verificar se o ano e o mês existem.
    if ano < 1 or mes < 1 or mes > 12:
        return None

    # Verifica se o ano é bissexto (fevereiro tem 29 dias nesses anos).
    bissexto = (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0

    # Quantidade de dias de cada mês (janeiro a dezembro).
    dias_do_mes = [31, 29 if bissexto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # If responsável por verificar se o dia existe dentro do mês (ex: não existe 31/02).
    if dia < 1 or dia > dias_do_mes[mes - 1]:
        return None

    return date(ano, mes, dia)  # Data válida.


# [NOVO] Função responsável por pedir ao usuário a data inicial e a data final do relatório.
def pedir_periodo():
    # Pede data inicial e final (Enter = sem limite). Retorna (inicio, fim) ou None se invalido.

    print("\nInforme o periodo (formato DD/MM/AAAA). Enter para nao limitar.")

    txt_ini = input("Data inicial: ").strip()  # Texto digitado para a data inicial.
    txt_fim = input("Data final: ").strip()    # Texto digitado para a data final.

    # Se o campo ficar vazio, usa a menor data possível (sem limite inicial).
    inicio = date.min
    # Se o campo ficar vazio, usa a maior data possível (sem limite final).
    fim = date.max

    # If responsável por validar a data inicial, apenas se ela foi digitada.
    if txt_ini != "":
        inicio = converter_data(txt_ini)
        if inicio is None:
            print("Data invalida! Use o formato DD/MM/AAAA.")
            return None

    # If responsável por validar a data final, apenas se ela foi digitada.
    if txt_fim != "":
        fim = converter_data(txt_fim)
        if fim is None:
            print("Data invalida! Use o formato DD/MM/AAAA.")
            return None

    # If responsável por verificar se a data inicial é maior que a final.
    if inicio > fim:
        print("A data inicial nao pode ser maior que a data final!")
        return None

    # Devolve o período escolhido para o relatório que chamou a função.
    return inicio, fim


# [NOVO] Função que filtra e devolve somente as vendas feitas dentro do período informado.
def vendas_do_periodo(inicio, fim):
    # List comprehension: percorre todas as vendas e mantém só as que estão entre a data inicial e a final.
    return [v for v in vendas if inicio <= v["data"] <= fim]


# [NOVO] Função que monta o texto do período para ser mostrado nos relatórios (ex: 01/11/2026 a 20/11/2026).
def texto_periodo(inicio, fim):
    # Se não houve data inicial informada, mostra "inicio" no lugar da data.
    ini_txt = inicio.strftime("%d/%m/%Y") if inicio != date.min else "inicio"
    # Se não houve data final informada, mostra "hoje" no lugar da data.
    fim_txt = fim.strftime("%d/%m/%Y") if fim != date.max else "hoje"
    return f"{ini_txt} a {fim_txt}"


# [ALTERADO] Função reescrita: antes usava campos que não existem (produto e quantidade) e quebrava.
# Agora percorre a lista de itens de cada venda e mostra o total geral no final.
def listar_vendas():
    # Consulta todas as vendas, sem filtrar datas, com o total geral no final.

    print("\n========== HISTORICO DE VENDAS ==========")

    # If responsável por informar que não possui vendas realizadas.
    if not vendas:
        print("Nenhuma venda realizada.")
        return

    total_geral = 0  # [NOVO] Contador do valor total de todas as vendas.

    # For responsável por percorrer todas as vendas e mostrar os dados de cada uma.
    for venda in vendas:

        print("\n-----------------------------------------")
        # [NOVO] Mostra o número da venda e a data em que ela foi feita.
        print("Venda:", venda["codigo"], "| Data:", venda["data"].strftime("%d/%m/%Y"))
        print("Cliente:", venda["cliente"])
        print("Vendedor:", venda["vendedor"])

        # [NOVO] For que percorre cada produto (item) comprado nessa venda.
        for item in venda["itens"]:
            print(
                f"  - {item['nome']} | Qtd: {item['quantidade']} "
                f"| Unitario: R$ {item['valor_unitario']:.2f} "
                f"| Subtotal: R$ {item['subtotal']:.2f}"
            )

        print(f"Subtotal: R$ {venda['subtotal']:.2f}")
        print(f"Imposto: R$ {venda['imposto']:.2f}")           # [NOVO] Imposto total da venda.
        print(f"Total da venda: R$ {venda['total']:.2f}")      # [NOVO] Total individual da venda.
        print(f"Comissao: R$ {venda['comissao']:.2f}")         # [NOVO] Comissão total da venda.

        total_geral += venda["total"]  # [NOVO] Soma o total da venda ao total geral.

    print("\n=========================================")
    print(f"Quantidade de vendas: {len(vendas)}")        # [NOVO] Quantidade de vendas realizadas.
    print(f"TOTAL DE VENDAS: R$ {total_geral:.2f}")      # [NOVO] Valor somado de todas as vendas.


# [NOVO] Relatório que mostra todas as vendas de um período com os totais no final.
def relatorio_por_periodo():

    print("\n========== RELATORIO POR PERIODO ==========")

    periodo = pedir_periodo()  # Pede o período ao usuário.
    # If responsável por cancelar o relatório se o período digitado for inválido.
    if periodo is None:
        return

    inicio, fim = periodo  # Separa a data inicial e a final.
    lista = vendas_do_periodo(inicio, fim)  # Pega apenas as vendas do período.

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    # If responsável por informar que não há vendas no período.
    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    # Contadores dos valores somados do período.
    subtotal = imposto = total = comissao = 0

    # For responsável por mostrar cada venda do período.
    for venda in lista:
        print(
            f"\nVenda {venda['codigo']} | {venda['data'].strftime('%d/%m/%Y')} "
            f"| Cliente: {venda['cliente']} | Vendedor: {venda['vendedor']}"
        )
        print(
            f"  Subtotal: R$ {venda['subtotal']:.2f} | Imposto: R$ {venda['imposto']:.2f} "
            f"| Total: R$ {venda['total']:.2f} | Comissao: R$ {venda['comissao']:.2f}"
        )

        # Soma os valores da venda aos contadores do período.
        subtotal += venda["subtotal"]
        imposto += venda["imposto"]
        total += venda["total"]
        comissao += venda["comissao"]

    print("\n-----------------------------------------")
    print(f"Vendas no periodo: {len(lista)}")
    print(f"Subtotal: R$ {subtotal:.2f}")
    print(f"Impostos: R$ {imposto:.2f}")
    print(f"Comissoes: R$ {comissao:.2f}")
    print(f"TOTAL VENDIDO: R$ {total:.2f}")


# [NOVO] Relatório que consolida (soma) a quantidade vendida de cada produto no período.
def relatorio_produtos_vendidos():

    print("\n========== PRODUTOS VENDIDOS ==========")

    periodo = pedir_periodo()  # Pede o período ao usuário.
    # If responsável por cancelar o relatório se o período digitado for inválido.
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)  # Pega apenas as vendas do período.

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    # If responsável por informar que não há vendas no período.
    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    # Consolida por produto
    consolidado = {}  # Dicionário que guarda a quantidade e o valor somado de cada produto.

    # For responsável por percorrer as vendas do período e depois os itens de cada venda.
    for venda in lista:
        for item in venda["itens"]:
            cod = item["codigo_produto"]  # Código do produto, usado como chave do dicionário.

            # If responsável por criar o produto no dicionário na primeira vez que ele aparece.
            if cod not in consolidado:
                consolidado[cod] = {"nome": item["nome"], "quantidade": 0, "subtotal": 0}

            # Soma a quantidade e o valor do item ao total do produto.
            consolidado[cod]["quantidade"] += item["quantidade"]
            consolidado[cod]["subtotal"] += item["subtotal"]

    total_unidades = 0  # Contador do total de unidades vendidas.
    total_valor = 0     # Contador do valor total vendido (sem imposto).

    # For responsável por mostrar cada produto já consolidado.
    for cod, dados in consolidado.items():
        print(
            f"Codigo: {cod} | Produto: {dados['nome']} "
            f"| Qtd vendida: {dados['quantidade']} "
            f"| Valor: R$ {dados['subtotal']:.2f}"
        )
        total_unidades += dados["quantidade"]
        total_valor += dados["subtotal"]

    print("\n-----------------------------------------")
    print(f"Total de unidades vendidas: {total_unidades}")
    print(f"Valor total dos produtos (sem imposto): R$ {total_valor:.2f}")


# [NOVO] Relatório com o total de cada venda, o total geral e o ticket médio do período.
def relatorio_total_vendas():

    print("\n========== TOTAL DE VENDAS ==========")

    periodo = pedir_periodo()  # Pede o período ao usuário.
    # If responsável por cancelar o relatório se o período digitado for inválido.
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)  # Pega apenas as vendas do período.

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    # If responsável por informar que não há vendas no período.
    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    # Soma o total de todas as vendas do período.
    total = sum(v["total"] for v in lista)

    # For responsável por mostrar o total individual de cada venda.
    for venda in lista:
        print(
            f"Venda {venda['codigo']} | {venda['data'].strftime('%d/%m/%Y')} "
            f"| Total: R$ {venda['total']:.2f}"
        )

    print("\n-----------------------------------------")
    print(f"Quantidade de vendas: {len(lista)}")
    print(f"TOTAL DE VENDAS: R$ {total:.2f}")
    # Ticket médio = valor total dividido pela quantidade de vendas.
    print(f"Ticket medio: R$ {total / len(lista):.2f}")


# [NOVO] Relatório que soma os impostos das vendas de um período.
def relatorio_imposto_periodo():

    print("\n========== IMPOSTO POR PERIODO ==========")

    periodo = pedir_periodo()  # Pede o período ao usuário.
    # If responsável por cancelar o relatório se o período digitado for inválido.
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)  # Pega apenas as vendas do período.

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    # If responsável por informar que não há vendas no período.
    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    total_imposto = 0  # Contador do imposto somado do período.

    # For responsável por mostrar o imposto de cada venda e somá-lo ao total.
    for venda in lista:
        print(
            f"Venda {venda['codigo']} | {venda['data'].strftime('%d/%m/%Y')} " #.strftime transforma uma data em texto
            f"| Subtotal: R$ {venda['subtotal']:.2f} "
            f"| Imposto: R$ {venda['imposto']:.2f}"
        )
        total_imposto += venda["imposto"]

    print("\n-----------------------------------------")
    print(f"TOTAL DE IMPOSTOS NO PERIODO: R$ {total_imposto:.2f}")


# [NOVO] Relatório que mostra o total de comissão agrupado por vendedor.
def relatorio_comissao_vendedor():

    print("\n========== COMISSAO POR VENDEDOR ==========")

    periodo = pedir_periodo()  # Pede o período ao usuário.
    # If responsável por cancelar o relatório se o período digitado for inválido.
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)  # Pega apenas as vendas do período.

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    # If responsável por informar que não há vendas no período.
    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    # Agrupa por vendedor
    por_vendedor = {}  # Dicionário que guarda as vendas, o total e a comissão de cada vendedor.

    # For responsável por percorrer as vendas e somar os valores de cada vendedor.
    for venda in lista:
        nome = venda["vendedor"]  # Nome do vendedor, usado como chave do dicionário.

        # If responsável por criar o vendedor no dicionário na primeira vez que ele aparece.
        if nome not in por_vendedor:
            por_vendedor[nome] = {"vendas": 0, "total": 0, "comissao": 0}

        por_vendedor[nome]["vendas"] += 1                      # Conta mais uma venda para o vendedor.
        por_vendedor[nome]["total"] += venda["total"]          # Soma o total vendido.
        por_vendedor[nome]["comissao"] += venda["comissao"]    # Soma a comissão do vendedor.

    total_comissao = 0  # Contador da comissão somada de todos os vendedores.

    # For responsável por mostrar o resultado de cada vendedor.
    for nome, dados in por_vendedor.items():
        print(
            f"Vendedor: {nome} | Vendas: {dados['vendas']} "
            f"| Total vendido: R$ {dados['total']:.2f} "
            f"| Comissao: R$ {dados['comissao']:.2f}"
        )
        total_comissao += dados["comissao"]

    print("\n-----------------------------------------")
    print(f"TOTAL DE COMISSOES: R$ {total_comissao:.2f}")


# ==========================================
# RECIBO DA VENDA
# ==========================================

# [NOVO] Função que imprime o recibo da venda com a data e os valores individuais de cada produto.
def emitir_recibo(venda):
    # Recibo com data e valores individuais de todos os produtos da venda.

    print("\n==========================================")
    print("               RECIBO DE VENDA")
    print("==========================================")
    print(f"Venda N: {venda['codigo']}")
    print(f"Data: {venda['data'].strftime('%d/%m/%Y')}")  # Data da venda no formato DD/MM/AAAA.
    print(f"Cliente: {venda['cliente']}")
    print(f"Vendedor: {venda['vendedor']}")
    print("------------------------------------------")

    # For responsável por mostrar todos os produtos da venda (e não só um), cada um com seus valores.
    for item in venda["itens"]:
        print(f"{item['nome']}")
        print(
            f"  {item['quantidade']} x R$ {item['valor_unitario']:.2f}"
            f" = R$ {item['subtotal']:.2f}"
            f" | Imposto ({item['taxa_imposto']}%): R$ {item['imposto']:.2f}"
            f" | Total: R$ {item['total']:.2f}"
        )

    print("------------------------------------------")
    print(f"Subtotal: R$ {venda['subtotal']:.2f}")
    print(f"Imposto:  R$ {venda['imposto']:.2f}")
    print(f"TOTAL:    R$ {venda['total']:.2f}")
    print("==========================================")


# [NOVO] Função que permite imprimir novamente o recibo de uma venda já realizada.
def reimprimir_recibo():

    print("\n========== REIMPRIMIR RECIBO ==========")

    # If responsável por informar que não há vendas realizadas.
    if not vendas:
        print("Nenhuma venda realizada.")
        return

    texto = input("Numero da venda: ").strip()  # Texto digitado pelo usuário.

    # If responsável por verificar se o que foi digitado é um número (sem usar try/except).
    if not texto.isdecimal():
        print("Numero invalido!")
        return

    codigo = int(texto)  # Converte para número inteiro, já que foi validado acima.

    # Procura a venda com o número informado (devolve None se não encontrar).
    venda = next((v for v in vendas if v["codigo"] == codigo), None)

    # If responsável por informar que a venda não existe.
    if venda is None:
        print("Venda nao encontrada!")
        return

    emitir_recibo(venda)  # Imprime o recibo da venda encontrada.


# ==========================================
# MENU RELATORIOS
# ==========================================

# [NOVO] Menu que reúne todos os relatórios do sistema.
def menu_relatorios():

    # While responsável por manter o menu aberto até o usuário escolher voltar.
    while True:

        print("\n========== RELATORIOS ==========")

        print("1. Historico de Vendas (todas)")
        print("2. Relatorio por Periodo")
        print("3. Produtos Vendidos")
        print("4. Total de Vendas")
        print("5. Imposto por Periodo")
        print("6. Comissao por Vendedor")
        print("7. Reimprimir Recibo")
        print("8. Voltar ao Menu Principal")

        print("================================")

        opcao = input("Escolha uma opcao: ").strip()

        # If/elif/else responsável por chamar a função da opção escolhida.
        if opcao == "1":
            listar_vendas()
        elif opcao == "2":
            relatorio_por_periodo()
        elif opcao == "3":
            relatorio_produtos_vendidos()
        elif opcao == "4":
            relatorio_total_vendas()
        elif opcao == "5":
            relatorio_imposto_periodo()
        elif opcao == "6":
            relatorio_comissao_vendedor()
        elif opcao == "7":
            reimprimir_recibo()
        elif opcao == "8":
            print("\nVoltando ao menu principal...")
            break  # Sai do menu de relatórios.
        else:
            # Else executado quando a opção digitada não existe.
            print("Opcao invalida! Escolha entre 1 e 8.")

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

       
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            adicionar_produto_estoque()
        elif opcao == "3":
            remover_produto_estoque()
        elif opcao == "4":
            listar_produtos()
        elif opcao == "5":
            print("\nVoltando ao menu principal...")
            break
        else:
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
        print("7. Relatorios")  # [ALTERADO] Antes era "Consultar Vendas"; agora abre o menu de relatórios.
        print("8. Fechar Sistema")

        print("=======================================")

        opcao = input("Escolha uma opcao: ").strip()

    
        if opcao == "1":
            menu_estoque()
        elif opcao == "2":
            cadastrar_cliente()
        elif opcao == "3":
            listar_clientes()
        elif opcao == "4":
            cadastrar_vendedor()
        elif opcao == "5":
            listar_vendedores()
        elif opcao == "6":
            registrar_venda()
        elif opcao == "7":
            menu_relatorios()  # [ALTERADO] Antes chamava listar_vendas(); agora abre o menu de relatórios.
        elif opcao == "8":
            print("\nEncerrando o sistema...")
            print("Obrigado por utilizar o sistema!")
            break
        else:
            
            print("Opcao invalida! Escolha entre 1 e 8.")

# ==========================================
# INICIAR SISTEMA
# ==========================================

if __name__ == "__main__":
    menu_principal()