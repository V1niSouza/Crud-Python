from pymongo import MongoClient 
from pymongo import errors
from bson import errors as berrors 
from bson.objectid import ObjectId  
 
   # Função para conectar ao servidor MongoDB
def conectar():
    conexao = MongoClient('localhost', 27017)
    return conexao

    # Função para desconectar do servidor MongoDB
def desconectar(conexao):
    if conexao:
        conexao.close()


                         #Funções lists
def listProd():
    conexao = conectar() 
    db = conexao.bdMongo_Vinicius 
    try:
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find() 
            print("Listando produtos")
            print("-----------------")
            for produto in produtos: 
                print(f"ID: {produto['_id']}")
                print(f"Produto: {produto['nome']}")
                print(f"Preço: {produto['preco']}")
                print(f"Estoque: {produto['estoque']}")
                print("-----------------")
        else:
            print("Não existem produtos.")
    except errors.PyMongoError as e:
        print(f"Erro ao acessar o banco: {e}")
    finally:
        desconectar(conexao)

def listClient():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius
    
    try:
        if db.clientes.count_documents({}) > 0:
            clientes = db.clientes.find() 
            print("Listando Clientes")
            print("-----------------")
            for cliente in clientes:
                print(f"ID: {cliente['_id']}")
                print(f"Nome: {cliente['nome']}")
                print(f"Telefone: {cliente['telefone']}")
                print(f"Endereço: {cliente['endereco']}")
                print(f"CPF: {cliente['cpf']}")
                print("-----------------")
        else:
            print("Não existem clientes.")
    except errors.PyMongoError as e:
        print(f"Erro ao acessar o banco: {e}")
    finally:
        desconectar(conexao)

def listVend():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius
    
    try:
        if db.vendas.count_documents({}) > 0:
            vendas = db.vendas.find() 
            print("Listando Vendas")
            print("-----------------")
            for venda in vendas:
                print(f"ID: {venda['_id']}")
                print(f"Nome do Cliente: {venda['nomeCli']}")
                print(f"CPF do Cliente: {venda['cpfCli']}")
                print(f"Produto: {venda['nomeProd']}")
                print(f"Quantidade: {venda['qtd']}")
                print(f"valor: {venda['price']}")
                print("-----------------")
        else:
            print("Não existem vendas.")
    except errors.PyMongoError as e:
        print(f"Erro ao acessar o banco: {e}")
    finally:
        desconectar(conexao)



                #Funções inserts

def insertProd():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))
    try:
        db.produtos.insert_one(
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque  
            }
        )
        print(f"O produto {nome} foi inserido com sucesso!")
    except errors.PyMongoError as e:
        print(f'Não foi possível inserir o produto: {e}')
    finally:
        desconectar(conexao)

def insertClient():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius 
    nome = input('Informe o nome do cliente: ')
    telefone = input('Informe o telefone do cliente: ')
    endereco = input('Informe o endereço do cliente: ')
    cpf = input('Informe o CPF do cliente: ')
    try:
        db.clientes.insert_one(
            {
                "nome": nome,
                "telefone": telefone,
                "endereco": endereco,
                "cpf": cpf
            }
        )

        print(f"O cliente {nome} foi inserido com sucesso!")
    except errors.PyMongoError as e:
        print(f'Não foi possível inserir o cliente: {e}')
    finally:
        desconectar(conexao)

def insertVenda():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius 
    nomeCli = input('Informe o nome do cliente: ')
    cpfCli = input('Informe o CPF do cliente: ')
    nomeProd = input('Informe o nome do produto: ')
    qtd = int(input('Informe a quantidade: '))
    price = float(input('Informe o valor da venda: '))
    try:
        produto = db.produtos.find_one({"nome": nomeProd})
        if produto:
            momentEstoque = produto['estoque']
            if momentEstoque >= qtd:
                db.vendas.insert_one(
                    {
                        "nomeCli": nomeCli,
                        "cpfCli": cpfCli,
                        "nomeProd": nomeProd,
                        "qtd": qtd,
                        "price": price
                    }
                )
                newEstoque = momentEstoque - qtd
                db.produtos.update_one(
                    {"_id": produto['_id']},
                    {"$set": {"estoque": newEstoque}}
                ) 
                print(f"Venda realizada com sucesso")
                print(f"Estoque atualizado = {nomeProd}: {newEstoque}")
            else:
                print(f"Quantidade insuficiente! Existe somente: {momentEstoque}")
        else:
            print(f"O produto não encontrado.")
    
    except errors.PyMongoError as e:
        print(f'Não foi possível realizar a venda: {e}')
    finally:
        desconectar(conexao)

                #Funções updates

def updateProd():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius 
    _id = input('Informe o ID do produto: ')
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))
    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {'$set': {
                    'nome': nome,
                    'preco': preco,
                    'estoque': estoque
                }}
            )
            if res.modified_count == 1:
                print(f'O produto {nome} foi alterado com sucesso!')
            else:
                print('Não foi possível atualizar o produto')
        else:
            print('Não existem produtos a serem atualizados!')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)

def updateClient():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius  
    _id = input('Informe o ID do cliente: ')
    nome = input('Informe o novo nome do cliente: ')
    telefone = input('Informe o novo telefone do cliente: ')
    endereco = input('Informe o novo endereço do cliente: ')
    cpf = input('Informe o novo CPF do cliente: ')

    try:
        if db.clientes.count_documents({}) > 0:
            res = db.clientes.update_one(
                {"_id": ObjectId(_id)},
                {'$set': {
                    'nome': nome,
                    'telefone': telefone,
                    'endereco': endereco,
                    'cpf': cpf
                }}
            )
            if res.modified_count == 1:
                print(f'O cliente {nome} foi alterado com sucesso!')
            else:
                print('Não foi possível atualizar o cliente')
        else:
            print('Não existem clientes a serem atualizados!')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)

def updateVenda():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius  
    _id = input('Informe o ID da venda: ')
    nomeCli = input('Informe o novo nome do cliente: ')
    cpfCli = input('Informe o novo CPF do cliente: ')
    nomeProd = input('Informe o novo nome do produto: ')
    qtd = int(input('Informe a nova quantidade: '))
    price = float(input('Informe o novo valor da venda: '))

    try:
        if db.vendas.count_documents({}) > 0:
            res = db.vendas.update_one(
                {"_id": ObjectId(_id)},
                {'$set': {
                    'nomeCli': nomeCli,
                    'cpfCli': cpfCli,
                    'nomeProd': nomeProd,
                    'qtd': qtd,
                    'price': price
                }}
            )
            if res.modified_count == 1:
                print(f'A venda de {nomeProd} foi alterada com sucesso!')
            else:
                print('Não foi possível atualizar a venda')
        else:
            print('Não existem vendas a serem atualizadas!')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)


                        #Funções delets
def deletProd():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius  
    _id = input('Informe o ID do produto: ')

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one({"_id": ObjectId(_id)})
            if res.deleted_count > 0:
                print('Produto excluído com sucesso!')
            else:
                print('Não foi possível excluir o produto')
        else:
            print('Não existem produtos a serem excluídos')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)

def deletClient():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius 
    _id = input('Informe o ID do cliente: ')

    try:
        if db.clientes.count_documents({}) > 0:
            res = db.clientes.delete_one({"_id": ObjectId(_id)})
            if res.deleted_count > 0:
                print('Cliente excluído com sucesso!')
            else:
                print('Não foi possível excluir o cliente')
        else:
            print('Não existem clientes a serem excluídos')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)

def deletVenda():
    conexao = conectar()
    db = conexao.bdMongo_Vinicius  
    _id = input('Informe o ID da venda: ')

    try:
        if db.vendas.count_documents({}) > 0:
            res = db.vendas.delete_one({"_id": ObjectId(_id)})
            if res.deleted_count > 0:
                print('Venda excluída com sucesso!')
            else:
                print('Não foi possível excluir a venda')
        else:
            print('Não existem vendas a serem excluídas')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido: {f}')
    finally:
        desconectar(conexao)

def Options():
    print('--------- Deseja ir para qual menu? -----------')
    print('Selecione a Opção desejada')
    print('1 - Menu Produto')
    print('2 - Menu Cliente')
    print('3 - Menu Venda')
    opcao = int(input('O que deseja fazer: '))
    if opcao in [1, 2, 3]:
        if opcao == 1:
            OptionsProd()
        elif opcao == 2:
            OptionsClient()
        elif opcao == 3:
            OptionsVend()
    else:
        print('Opção inválida!')

def OptionsProd():
    print('--------- Deseja ir para qual menu? -----------')
    print('Selecione a Opção desejada')
    print('1 - Inserir Produto')
    print('2 - Listar Produtos')
    print('3 - Atualizar Produto')
    print('4 - Excluir Produto')
    opcao = int(input('O que deseja fazer: '))
    if opcao in [1, 2, 3, 4]:  # Corrigindo a lista de opções
        if opcao == 1:
            insertProd()
        elif opcao == 2:
            listProd()
        elif opcao == 3:
            updateProd()
        elif opcao == 4:
            deletProd()
    else:
        print('Opção inválida!')

def OptionsClient():
    print('--------- Deseja ir para qual menu? -----------')
    print('Selecione a Opção desejada')
    print('1 - Inserir Cliente')
    print('2 - Listar Clientes')
    print('3 - Atualizar Cliente')
    print('4 - Excluir Cliente')
    opcao = int(input('O que deseja fazer: '))
    if opcao in [1, 2, 3, 4]:  # Corrigindo a lista de opções
        if opcao == 1:
            insertClient()
        elif opcao == 2:
            listClient()
        elif opcao == 3:
            updateClient()
        elif opcao == 4:
            deletClient()
    else:
        print('Opção inválida!')

def OptionsVend():
    print('--------- Deseja ir para qual menu? -----------')
    print('Selecione a Opção desejada')
    print('1 - Inserir Venda')
    print('2 - Listar Vendas')
    print('3 - Atualizar Venda')
    print('4 - Excluir Venda')
    opcao = int(input('O que deseja fazer: '))
    if opcao in [1, 2, 3, 4]:  # Corrigindo a lista de opções
        if opcao == 1:
            insertVenda()
        elif opcao == 2:
            listVend()
        elif opcao == 3:
            updateVenda()
        elif opcao == 4:
            deletVenda()
    else:
        print('Opção inválida!')