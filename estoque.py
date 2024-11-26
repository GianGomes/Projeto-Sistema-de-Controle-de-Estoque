import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

def criar_tabela(cursor):

    sql = '''
        CREATE TABLE IF NOT EXISTS PRODUTOS(
           pro_id integer primary key autoincrement,
           pro_nome text not null,
           pro_qntd integer not null,
           pro_preco real not null
        )
    '''
    cursor.execute(sql)



def add_prod():
    
    pro_nome = input("Nome do produto: ")
    pro_qntd = int(input("Quantia em estoque: "))
    pro_preco = float(input("Preço por unidade: "))

    cursor.execute("INSERT INTO PRODUTOS(pro_nome , pro_qntd , pro_preco) VALUES (? , ? , ?)",(pro_nome , pro_qntd , pro_preco))
    conn.commit()
    print("Produto registrado com sucesso!")



def list_prod():
    
    cursor.execute("SELECT * FROM PRODUTOS")
    PRODUTOS = cursor.fetchall()

    if PRODUTOS:
        print("\nProdutos no estoque.")
        for produto in PRODUTOS:
            print(f"ID: {produto[0]} | Nome do produto: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f}")
    else:
        print("\nNão há produtos no estoque")



def update_prod():

    list_prod()
    pro_id = int(input("\nDigite o ID do produto que deseja atualizar: "))
    campo = input("Deseja alterar 'quantidade' ou 'preço'?").lower()

    if campo == "quantidade":
        nova_qntd = int(input("Nova quantidade: "))
        cursor.execute("UPDATE PRODUTOS SET pro_qntd = ? WHERE pro_id = ?", (nova_qntd, pro_id))
    elif campo == "preço":
        novo_preco = float(input("Novo preço: "))
        cursor.execute("UPDATE PRODUTOS SET pro_preco = ? WHERE pro_id = ?", (novo_preco, pro_id))
    else:
        print("Opção inválida!")
        return
    
    conn.commit()
    print("Produto atualizado com sucesso!")



def del_prod():

    list_prod()
    pro_id = str(input("Digite o ID do produto: "))
    cursor.execute("DELETE FROM PRODUTOS WHERE pro_id = ?", (pro_id))
    conn.commit()
    print("Produto removido com sucesso!")



def search_prod():

    criterio = input("Buscar por 'id' ou 'nome'? ").lower()

    if criterio == "id":
        pro_id = str(input("Digite o ID do produto: "))
        cursor.execute("SELECT * FROM PRODUTOS WHERE pro_id = ?", (pro_id))
    elif criterio == "nome":
        pro_nome = input("Digite o nome do produto: ")
        cursor.execute("SELECT * FROM PRODUTOS WHERE pro_nome LIKE ?", (f"%{pro_nome}%",))
    else:
        print("Opção inválida.")
        return
    
    produtos = cursor.fetchall()
    if produtos:
        print("\nProduto(s) encontrados: ")
        for produto in produtos:
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: {produto[3]:.2f}")
        else:
            print("Nenhum produto encontrado.")



def menu():

    criar_tabela(cursor)
    conn.commit()

    while True:

        print("\n***Sistema de Controle de Produtos do Estoque***")
        print("1- Adicionar produto")
        print("2- Listar produtos")
        print("3- Atualizar produtos")
        print("4- Remover produtos")
        print("5- Buscar produtos")
        print("6- Sair do sistema")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            add_prod()
        elif opcao == "2":
            list_prod()
        elif opcao == "3":
            update_prod()
        elif opcao == "4":
            del_prod()
        elif opcao == "5":
            search_prod()
        elif opcao == "6":
            print("Saindo do sistema, até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")



menu()

conn.close()