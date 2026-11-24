import json
import os
from datetime import date, datetime  # Importa as ferramentas de data usadas na data da venda e nos relatórios por período.

# ==========================================
# CONFIGURACOES PADRAO E ARQUIVO JSON
# ==========================================

ARQUIVO_DADOS = "ARQUIVOS.JSON"

TAXA_IMPOSTO_PADRAO = 25.0
TAXA_COMISSAO_PADRAO = 5.0

DADOS_INICIAIS = {
    "produtos": [
        {
            "codigo": "P0001",
            "nome": "Mouse Gamer",
            "valor": 89.90,
            "estoque": 20,
            "taxa_imposto": TAXA_IMPOSTO_PADRAO,
            "taxa_comissao": TAXA_COMISSAO_PADRAO
        },
        {
            "codigo": "P0002",
            "nome": "Teclado Mecanico",
            "valor": 199.90,
            "estoque": 15,
            "taxa_imposto": TAXA_IMPOSTO_PADRAO,
            "taxa_comissao": TAXA_COMISSAO_PADRAO
        },
        {
            "codigo": "P0003",
            "nome": "Headset Gamer",
            "valor": 149.90,
            "estoque": 12,
            "taxa_imposto": TAXA_IMPOSTO_PADRAO,
            "taxa_comissao": TAXA_COMISSAO_PADRAO
        },
        {
            "codigo": "P0004",
            "nome": "Monitor LED 24 Polegadas",
            "valor": 699.90,
            "estoque": 8,
            "taxa_imposto": TAXA_IMPOSTO_PADRAO,
            "taxa_comissao": TAXA_COMISSAO_PADRAO
        }
    ],
    "clientes": [
        {
            "codigo": "C0001",
            "nome": "Lucas Ferreira",
            "telefone": "83987654321"
        },
        {
            "codigo": "C0002",
            "nome": "Mariana Oliveira",
            "telefone": "83991234567"
        },
        {
            "codigo": "C0003",
            "nome": "Gabriel Santos",
            "telefone": "83988776655"
        }
    ],
    "vendedores": [
        {
            "codigo": "V0001",
            "nome": "Pedro Henrique",
            "telefone": "83999887766"
        },
        {
            "codigo": "V0002",
            "nome": "Ana Beatriz",
            "telefone": "83995554433"
        }
    ],
    "vendas": []
}

produtos = []
clientes = []
vendedores = []
vendas = []

contador_produto = 0
contador_cliente = 0
contador_vendedor = 0


def _extrair_numero_codigo(codigo, prefixo):
    if isinstance(codigo, str) and codigo.startswith(prefixo):
        parte_num = codigo[len(prefixo):]
        if parte_num.isdecimal():
            return int(parte_num)
    return 0


def _normalizar_data(valor_data):
    if isinstance(valor_data, date) and not isinstance(valor_data, datetime):
        return valor_data
    if isinstance(valor_data, datetime):
        return valor_data.date()
    if isinstance(valor_data, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(valor_data, fmt).date()
            except ValueError:
                continue
    return date.today()


def sincronizar_contadores():
    global contador_produto, contador_cliente, contador_vendedor

    contador_produto = max(
        [_extrair_numero_codigo(p.get("codigo", ""), "P") for p in produtos],
        default=0
    )
    contador_cliente = max(
        [_extrair_numero_codigo(c.get("codigo", ""), "C") for c in clientes],
        default=0
    )
    contador_vendedor = max(
        [_extrair_numero_codigo(v.get("codigo", ""), "V") for v in vendedores],
        default=0
    )


def salvar_dados():
    vendas_serializaveis = []
    for venda in vendas:
        copia_venda = dict(venda)
        data_obj = _normalizar_data(copia_venda.get("data"))
        copia_venda["data"] = data_obj.isoformat()
        vendas_serializaveis.append(copia_venda)

    payload = {
        "produtos": produtos,
        "clientes": clientes,
        "vendedores": vendedores,
        "vendas": vendas_serializaveis
    }

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(payload, arquivo, ensure_ascii=False, indent=4)


def carregar_dados():
    global produtos, clientes, vendedores, vendas

    if not os.path.exists(ARQUIVO_DADOS):
        produtos = [dict(p) for p in DADOS_INICIAIS["produtos"]]
        clientes = [dict(c) for c in DADOS_INICIAIS["clientes"]]
        vendedores = [dict(v) for v in DADOS_INICIAIS["vendedores"]]
        vendas = []
        sincronizar_contadores()
        salvar_dados()
        return

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print(f"Aviso: Nao foi possivel ler {ARQUIVO_DADOS}. Carregando dados iniciais.")
        dados = DADOS_INICIAIS

    produtos = dados.get("produtos", [])
    clientes = dados.get("clientes", [])
    vendedores = dados.get("vendedores", [])
    vendas = dados.get("vendas", [])

    for venda in vendas:
        venda["data"] = _normalizar_data(venda.get("data"))

    sincronizar_contadores()


# ==========================================
# GERACAO DE CODIGOS
# ==========================================

def gerar_codigo(prefixo):
    if prefixo == "P":
        global contador_produto
        contador_produto += 1
        return f"P{contador_produto:04d}"

    elif prefixo == "C":
        global contador_cliente
        contador_cliente += 1
        return f"C{contador_cliente:04d}"

    elif prefixo == "V":
        global contador_vendedor
        contador_vendedor += 1
        return f"V{contador_vendedor:04d}"


def gerar_codigo_produto():
    return gerar_codigo("P")


def gerar_codigo_cliente():
    return gerar_codigo("C")


def gerar_codigo_vendedor():
    return gerar_codigo("V")


# ==========================================
# CONTROLE DE ESTOQUE / Feito por Douglas
# ==========================================

def cadastrar_produto():
    print("\n--- CADASTRO DE PRODUTO ---")

    while True:
        nome = input("Digite o nome do produto: ")

        if nome == "":
            print("Erro: O nome do produto não pode ficar em branco!")
            continue

        nome_repetido = False

        for produto in produtos:
            if produto["nome"].lower() == nome.lower():
                print("Erro: Já existe um produto cadastrado com o nome", produto["nome"])
                nome_repetido = True
                break

        if not nome_repetido:
            break

    while True:
        try:
            valor = float(input("Digite o valor unitário (R$): "))

            if valor <= 0:
                print("Erro: O valor do produto deve ser maior que zero!")
                continue

            break

        except ValueError:
            print("Erro: Digite um valor numérico válido!")

    while True:
        try:
            estoque = int(input("Digite a quantidade inicial em estoque: "))

            if estoque < 0:
                print("Erro: A quantidade em estoque não pode ser menor que zero!")
                continue

            break

        except ValueError:
            print("Erro: Digite uma quantidade inteira válida!")

    codigo = gerar_codigo_produto()

    novo_produto = {
        "codigo": codigo,
        "nome": nome,
        "valor": valor,
        "estoque": estoque,
        "taxa_imposto": TAXA_IMPOSTO_PADRAO,
        "taxa_comissao": TAXA_COMISSAO_PADRAO
    }

    produtos.append(novo_produto)
    salvar_dados()
    print("Produto", nome, "cadastrado com sucesso.")
    print("Código gerado:", codigo)


def listar_produtos():
    print("\n--- CONSULTA DE ESTOQUE ---")
    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    valor_total_estoque = 0

    for produto in produtos:
        valor_total_produto = produto["valor"] * produto["estoque"]

        print(
            "Código:", produto["codigo"],
            "| Nome:", produto["nome"],
            "| Preço: R$", produto["valor"],
            "| Estoque:", produto["estoque"],
            "| Valor total: R$", f"{valor_total_produto:.2f}"
        )

        valor_total_estoque += valor_total_produto

    print(f"\nValor bruto total do estoque: R$ {valor_total_estoque:.2f}")


def remover_produto_estoque():
    print("\n--- REMOVER PRODUTO DO ESTOQUE ---")

    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    while True:
        codigo = input("Digite o código do produto: ").upper()

        for produto in produtos:
            if produto["codigo"] == codigo:
                break
        else:
            print("Erro: Produto não encontrado!")
            continue

        break

    print("\nProduto:", produto["nome"])
    print("Quantidade disponível:", produto["estoque"])

    while True:
        try:
            quantidade = int(input("Digite a quantidade que deseja remover: "))

            if quantidade > produto["estoque"]:
                print("Erro: A quantidade informada é maior que o estoque disponível!")
                continue

            if quantidade <= 0:
                print("Erro: A quantidade deve ser maior que zero!")
                continue

            break

        except ValueError:
            print("Erro: Digite uma quantidade inteira válida!")

    produto["estoque"] -= quantidade
    salvar_dados()

    print("\nProduto removido do estoque com sucesso!")
    print("Produto:", produto["nome"])
    print("Quantidade removida:", quantidade)
    print("Estoque restante:", produto["estoque"])


def adicionar_produto_estoque():
    print("\n--- ADICIONAR PRODUTO AO ESTOQUE ---")

    if not produtos:
        print("Nenhum produto cadastrado no momento.")
        return

    while True:
        codigo = input("Digite o código do produto: ").upper()

        for produto in produtos:
            if produto["codigo"] == codigo:
                break
        else:
            print("Erro: Produto não encontrado!")
            continue

        break

    print("\nProduto:", produto["nome"])
    print("Quantidade disponível:", produto["estoque"])

    while True:
        try:
            quantidade = int(input("Digite a quantidade que deseja adicionar: "))

            if quantidade <= 0:
                print("Erro: A quantidade deve ser maior que zero!")
                continue

            break

        except ValueError:
            print("Erro: Digite uma quantidade inteira válida!")

    produto["estoque"] += quantidade
    salvar_dados()

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
    salvar_dados()

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
    salvar_dados()

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

    carrinho = []

    while True:
        listar_produtos()

        codigo_produto = input("\nCodigo do produto: ").strip().upper()

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

        if item is not None:
            item["quantidade"] += quantidade
        else:
            carrinho.append({
                "codigo_produto": produto["codigo"],
                "nome": produto["nome"],
                "valor_unitario": produto["valor"],
                "quantidade": quantidade,
                "taxa_imposto": produto["taxa_imposto"],
                "taxa_comissao": produto["taxa_comissao"]
            })

        print("Produto adicionado ao carrinho!")

        continuar = input("\nDeseja adicionar outro produto? (S/N): ").strip().upper()

        if continuar != "S":
            break

    if not carrinho:
        print("Carrinho vazio!")
        return

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

    confirmar = input("\nDeseja confirmar a compra? (S/N): ").strip().upper()

    if confirmar != "S":
        print("Compra cancelada! Carrinho mantido durante esta operacao.")
        return

    listar_clientes()

    codigo_cliente = input("\nCodigo do cliente: ").strip().upper()

    cliente = next(
        (c for c in clientes if c["codigo"] == codigo_cliente),
        None
    )

    if cliente is None:
        print("Cliente nao encontrado! Venda cancelada.")
        return

    listar_vendedores()

    codigo_vendedor = input("\nCodigo do vendedor: ").strip().upper()

    vendedor = next(
        (v for v in vendedores if v["codigo"] == codigo_vendedor),
        None
    )

    if vendedor is None:
        print("Vendedor nao encontrado! Venda cancelada.")
        return

    for item in carrinho:
        produto_estoque = next(
            (p for p in produtos if p["codigo"] == item["codigo_produto"]),
            None
        )
        if produto_estoque is not None:
            produto_estoque["estoque"] -= item["quantidade"]

    proximo_codigo_venda = max(
        (v.get("codigo", 0) for v in vendas if isinstance(v.get("codigo"), int)),
        default=0
    ) + 1

    nova_venda = {
        "codigo": proximo_codigo_venda,
        "data": date.today(),
        "cliente": cliente["nome"],
        "vendedor": vendedor["nome"],
        "itens": carrinho,
        "subtotal": round(subtotal_geral, 2),
        "imposto": round(imposto_geral, 2),
        "total": round(total_geral, 2),
        "comissao": round(comissao_geral, 2)
    }

    vendas.append(nova_venda)
    salvar_dados()

    print("\n========== VENDA FINALIZADA ==========")
    print(f"Cliente: {cliente['nome']}")
    print(f"Vendedor: {vendedor['nome']}")
    print(f"Total: R$ {total_geral:.2f}")
    print(f"Comissao: R$ {comissao_geral:.2f}")
    print("Estoque atualizado com sucesso!")

    emitir_recibo(nova_venda)


# ==========================================
# CONSULTA DE VENDAS E RELATORIOS
# ==========================================

def converter_data(texto):
    partes = texto.split("/")

    if len(partes) != 3:
        return None

    dia, mes, ano = partes

    if not (dia.isdecimal() and mes.isdecimal() and ano.isdecimal()):
        return None
    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        return None

    dia = int(dia)
    mes = int(mes)
    ano = int(ano)

    if ano < 1 or mes < 1 or mes > 12:
        return None

    bissexto = (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0
    dias_do_mes = [31, 29 if bissexto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if dia < 1 or dia > dias_do_mes[mes - 1]:
        return None

    return date(ano, mes, dia)


def pedir_periodo():
    print("\nInforme o periodo (formato DD/MM/AAAA). Enter para nao limitar.")

    txt_ini = input("Data inicial: ").strip()
    txt_fim = input("Data final: ").strip()

    inicio = date.min
    fim = date.max

    if txt_ini != "":
        inicio = converter_data(txt_ini)
        if inicio is None:
            print("Data invalida! Use o formato DD/MM/AAAA.")
            return None

    if txt_fim != "":
        fim = converter_data(txt_fim)
        if fim is None:
            print("Data invalida! Use o formato DD/MM/AAAA.")
            return None

    if inicio > fim:
        print("A data inicial nao pode ser maior que a data final!")
        return None

    return inicio, fim


def vendas_do_periodo(inicio, fim):
    return [v for v in vendas if inicio <= _normalizar_data(v["data"]) <= fim]


def texto_periodo(inicio, fim):
    ini_txt = inicio.strftime("%d/%m/%Y") if inicio != date.min else "inicio"
    fim_txt = fim.strftime("%d/%m/%Y") if fim != date.max else "hoje"
    return f"{ini_txt} a {fim_txt}"


def listar_vendas():
    print("\n========== HISTORICO DE VENDAS ==========")

    if not vendas:
        print("Nenhuma venda realizada.")
        return

    total_geral = 0

    for venda in vendas:
        data_venda = _normalizar_data(venda["data"])
        print("\n-----------------------------------------")
        print("Venda:", venda["codigo"], "| Data:", data_venda.strftime("%d/%m/%Y"))
        print("Cliente:", venda["cliente"])
        print("Vendedor:", venda["vendedor"])

        for item in venda["itens"]:
            print(
                f"  - {item['nome']} | Qtd: {item['quantidade']} "
                f"| Unitario: R$ {item['valor_unitario']:.2f} "
                f"| Subtotal: R$ {item['subtotal']:.2f}"
            )

        print(f"Subtotal: R$ {venda['subtotal']:.2f}")
        print(f"Imposto: R$ {venda['imposto']:.2f}")
        print(f"Total da venda: R$ {venda['total']:.2f}")
        print(f"Comissao: R$ {venda['comissao']:.2f}")

        total_geral += venda["total"]

    print("\n=========================================")
    print(f"Quantidade de vendas: {len(vendas)}")
    print(f"TOTAL DE VENDAS: R$ {total_geral:.2f}")


def relatorio_por_periodo():
    print("\n========== RELATORIO POR PERIODO ==========")

    periodo = pedir_periodo()
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    subtotal = imposto = total = comissao = 0

    for venda in lista:
        data_venda = _normalizar_data(venda["data"])
        print(
            f"\nVenda {venda['codigo']} | {data_venda.strftime('%d/%m/%Y')} "
            f"| Cliente: {venda['cliente']} | Vendedor: {venda['vendedor']}"
        )
        print(
            f"  Subtotal: R$ {venda['subtotal']:.2f} | Imposto: R$ {venda['imposto']:.2f} "
            f"| Total: R$ {venda['total']:.2f} | Comissao: R$ {venda['comissao']:.2f}"
        )

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


def relatorio_produtos_vendidos():
    print("\n========== PRODUTOS VENDIDOS ==========")

    periodo = pedir_periodo()
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    consolidado = {}

    for venda in lista:
        for item in venda["itens"]:
            cod = item["codigo_produto"]

            if cod not in consolidado:
                consolidado[cod] = {"nome": item["nome"], "quantidade": 0, "subtotal": 0}

            consolidado[cod]["quantidade"] += item["quantidade"]
            consolidado[cod]["subtotal"] += item["subtotal"]

    total_unidades = 0
    total_valor = 0

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


def relatorio_total_vendas():
    print("\n========== TOTAL DE VENDAS ==========")

    periodo = pedir_periodo()
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    total = sum(v["total"] for v in lista)

    for venda in lista:
        data_venda = _normalizar_data(venda["data"])
        print(
            f"Venda {venda['codigo']} | {data_venda.strftime('%d/%m/%Y')} "
            f"| Total: R$ {venda['total']:.2f}"
        )

    print("\n-----------------------------------------")
    print(f"Quantidade de vendas: {len(lista)}")
    print(f"TOTAL DE VENDAS: R$ {total:.2f}")
    print(f"Ticket medio: R$ {total / len(lista):.2f}")


def relatorio_imposto_periodo():
    print("\n========== IMPOSTO POR PERIODO ==========")

    periodo = pedir_periodo()
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    total_imposto = 0

    for venda in lista:
        data_venda = _normalizar_data(venda["data"])
        print(
            f"Venda {venda['codigo']} | {data_venda.strftime('%d/%m/%Y')} "
            f"| Subtotal: R$ {venda['subtotal']:.2f} "
            f"| Imposto: R$ {venda['imposto']:.2f}"
        )
        total_imposto += venda["imposto"]

    print("\n-----------------------------------------")
    print(f"TOTAL DE IMPOSTOS NO PERIODO: R$ {total_imposto:.2f}")


def relatorio_comissao_vendedor():
    print("\n========== COMISSAO POR VENDEDOR ==========")

    periodo = pedir_periodo()
    if periodo is None:
        return

    inicio, fim = periodo
    lista = vendas_do_periodo(inicio, fim)

    print(f"\nPeriodo: {texto_periodo(inicio, fim)}")

    if not lista:
        print("Nenhuma venda encontrada no periodo.")
        return

    por_vendedor = {}

    for venda in lista:
        nome = venda["vendedor"]

        if nome not in por_vendedor:
            por_vendedor[nome] = {"vendas": 0, "total": 0, "comissao": 0}

        por_vendedor[nome]["vendas"] += 1
        por_vendedor[nome]["total"] += venda["total"]
        por_vendedor[nome]["comissao"] += venda["comissao"]

    total_comissao = 0

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

def emitir_recibo(venda):
    data_venda = _normalizar_data(venda["data"])
    print("\n==========================================")
    print("               RECIBO DE VENDA")
    print("==========================================")
    print(f"Venda N: {venda['codigo']}")
    print(f"Data: {data_venda.strftime('%d/%m/%Y')}")
    print(f"Cliente: {venda['cliente']}")
    print(f"Vendedor: {venda['vendedor']}")
    print("------------------------------------------")

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


def reimprimir_recibo():
    print("\n========== REIMPRIMIR RECIBO ==========")

    if not vendas:
        print("Nenhuma venda realizada.")
        return

    texto = input("Numero da venda: ").strip()

    if not texto.isdecimal():
        print("Numero invalido!")
        return

    codigo = int(texto)

    venda = next((v for v in vendas if v["codigo"] == codigo), None)

    if venda is None:
        print("Venda nao encontrada!")
        return

    emitir_recibo(venda)


# ==========================================
# MENU RELATORIOS
# ==========================================

def menu_relatorios():
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
            break
        else:
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
        print("7. Relatorios")
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
            menu_relatorios()
        elif opcao == "8":
            salvar_dados()
            print("\nEncerrando o sistema...")
            print("Obrigado por utilizar o sistema!")
            break
        else:
            print("Opcao invalida! Escolha entre 1 e 8.")


# ==========================================
# INICIAR SISTEMA
# ==========================================

if __name__ == "__main__":
    carregar_dados()
    menu_principal()