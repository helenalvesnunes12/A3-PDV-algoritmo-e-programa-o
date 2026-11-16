produtos = [] # Lista onde são armazenados os produtos como dicionário.

def cadastrar_produto(): 
    #Função onde os produtos são cadastrados, um produto não pode ter o código igual a zero, nome em branco, nome repetido, 
    #valor menor que zero e quantidade menor que zero.
    
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
        if produto["nome"].lower() == nome.lower(): # .lower() Serve para deixar todo o texto em minúsculo, para comparar.
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
    
    # Criação do dicionário do produto.
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

# Menu de teste
def menu_estoque():
    while True:
        print("\n=== CONTROLE DE ESTOQUE ===")
        print("1. Cadastrar Produto")
        print("2. Consultar Estoque")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            print("Saindo do controle de estoque...")
            break
        else:
            print("Opção inválida! Escolha entre 1 e 3.")

# Inicia o menu de testes
menu_estoque()