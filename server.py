from socket import *
import mysql.connector
import json
import random
import yaml
from colorama import Fore
import threading

with open('application.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

size = data['size']
serverPort = data['serverPort']
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
letras = ['a','b','c','d','e']
mysql_cnx = mysql.connector.connect(user=data['mysql_user'], password=data['mysql_password'],
                              host=data['mysql_host'],
                              database=data['mysql_database'])
cursor = mysql_cnx.cursor()

def listaPontuacoes (connection,pin):
    query = (f'SELECT Usuario,Pontuacao FROM Pontuacoes WHERE Pin = "{pin}" ORDER BY (Pontuacao) DESC;')
    cursor.execute(query)
    envia(connection,f'\nUSUARIO - PONTUACAO')
    lista = ''
    for row in cursor:
        usuario = row[0]
        pontuacao = row[1]
        lista = lista + f'\n{usuario} - {pontuacao}'
    envia(connection,lista+ '\n')


def verifica_cursor(cursor):
    for x in cursor:
        return True
    return False

def existe_pontuacao (pin,usuario):
    cursor.execute(f'SELECT Pontuacao FROM Pontuacoes WHERE Pin = "{pin}" AND Usuario = "{usuario}"')
    return verifica_cursor(cursor)

def salvaPontuacao (usuario,pin,pontuacao):
    query = (f'INSERT INTO Pontuacoes (Pin,Usuario,Pontuacao) VALUES ("{pin}","{usuario}","{pontuacao}");')
    cursor.execute(query)
    mysql_cnx.commit()


def selecionarQuiz(pin):
    query = (f'SELECT Quiz_Json FROM Quizzes WHERE Pin = {pin};')
    cursor.execute(query)
    quiz_json = None
    for row in cursor:
        json_acceptable_string = row[0].replace("'", "\"")
        quiz_json = json.loads(json_acceptable_string)
    return quiz_json


def listarQuizzes(connection):
    query = (f'SELECT * FROM Quizzes;')
    cursor.execute(query)
    i = 1
    lista = ''
    for row in cursor:
        pin = row[0]
        json_acceptable_string = row[1].replace("'", "\"")
        quiz_json = json.loads(json_acceptable_string)
        descricao = quiz_json["descricao"]
        lista = lista + f'Quiz {i}: Pin: {pin} Descricao: {descricao}\n'
        i += 1
    connection.sendall(lista.encode())
    # envia(lista)

def salvaQuiz(pin,json):
    query = (f'INSERT INTO Quizzes (Pin,Quiz_Json) VALUES ("{pin}","{json}");')
    cursor.execute(query)
    mysql_cnx.commit()

def jogar(usuario,pin,connection):
    quiz = selecionarQuiz(pin)
    perguntas = quiz['perguntas']
    respostas_corretas = 0
    for i in range(1,6):
        pergunta = perguntas[str(i)]
        questao_string = f"\nQuestao {i}: {pergunta['textoQuestao']}\n"
        alternativas = pergunta['alternativas']
        for letra in letras:
            questao_string = questao_string + f"{letra}) {alternativas[letra]} \n"
        envia(connection,questao_string)
        resposta = recebe(connection)
        if(resposta == pergunta['alternativaCorreta']):
            respostas_corretas += 1
            envia(connection,Fore.GREEN+' Resposta Correta'+Fore.WHITE)
        else:
            envia(connection,Fore.RED + " Resposta Incorreta"+Fore.WHITE)
    
    salvaPontuacao(usuario,pin,respostas_corretas)
    envia(connection,Fore.GREEN+f' Voce acertou {respostas_corretas} questoes\n\nRank: \n'+Fore.WHITE)
    listaPontuacoes(connection,pin)

    

def criaQuiz(connection):
    envia(connection,"\nDigite a descricao do Quiz: ")
    descricao = recebe(connection)
    json_questao = dict()
    pin = str(random.randint(999,9999))
    json_questao['pin'] = pin
    json_questao['descricao'] = descricao
    perguntas = dict()
    for i in range(1,6):
        pergunta = dict()
        envia(connection,f"Digite a perguna numero {i}: ")
        textoQuestao = recebe(connection)
        pergunta['textoQuestao'] = textoQuestao
        alternativas = dict()
        for letra in letras:
            envia(connection,f"Digite a resposta letra {letra}:")
            resposta = recebe(connection)
            alternativas[letra] = resposta
        envia(connection,"Digite a alternativa correta para esta questao: ")
        alternativaCorreta = recebe(connection)
        while not letras.__contains__(alternativaCorreta):
            envia(connection,"Alternativa inexistente\nDigite a alternativa correta para esta questao: ")
            alternativaCorreta = recebe(connection)
        pergunta['alternativaCorreta'] = alternativaCorreta
        pergunta['alternativas'] = alternativas
        perguntas[str(i)] = pergunta
    json_questao['perguntas'] = perguntas
    envia(connection,f"Quiz criado pin: {pin}")
    print(json.dumps(json_questao, indent=4))
    salvaQuiz(pin,json_questao)


        
def envia(connection,mensagem):
    connection.sendall(mensagem.encode())

def recebe(connection):
    return connection.recv(size).decode()


def novoCliente(connection,clientAddress):
    print('Novo Cliente')
    usuario = recebe(connection)
    print(f"Usuario {usuario}")
    while 1:
        envia(connection,f"\n Bem vindo ao Quiz, {usuario}\n O que deseja fazer?\n 1 - Jogar um Quiz\n 2 - Listar os Quizzes existentes\n 3 - Criar um Quiz\n 4 - Visualizar Ranking \n 5 - Sair\n ")
        opcao = recebe(connection)
        if opcao == "1":
            envia(connection,"Digite o pin do Quiz: ")
            pin = recebe(connection)
            if not existe_pontuacao(pin,usuario):
                quiz_json = selecionarQuiz(pin)
                if quiz_json == None:
                    envia(connection,"\nNao existe quiz com esse PIN!\n")
                else:
                    jogar(usuario,pin,connection)
                    #salvaPontuacao(usuario,pin,5) #Teste
            else:
                envia(connection,"\nVoce ja jogou esse quiz antes!\n")
        elif opcao == "2":
            listarQuizzes(connection)
        elif opcao == "3":
            criaQuiz(connection)
        elif opcao == "4":
            envia(connection,"Digite o pin do Quiz: ")
            pin = recebe(connection)
            listaPontuacoes(connection,pin)
        elif opcao == "5":
            connection.close()
            exit(0)
        else:
            envia(connection,"Opcao Invalida!")


if __name__ == '__main__':
    print("Quiz server is on!")
    while 1:
        connection, clientAddress = serverSocket.accept()
        threading.Thread(target=novoCliente,args=(connection,clientAddress)).start()

        



# Descrição: Quiz com alternativas, um cliente manda as perguntas e respostas para o servidor e 
# outros clientes podem jogar o quiz. Ao final do quiz, o servidor retorna para o cliente a posição dele 
# no ranking.
# from socket import *

# def alterMessage(message):
# 	tipo = message[0:2]
# 	original_message = message[2:]
# 	if(tipo == 'CA'):
# 		return original_message.lower()
# 	else:
# 		if(tipo == 'CB'):
# 			return original_message.upper()
# 		else:
# 			return original_message


# serverPort = 8082
# tcp_server = socket(AF_INET,SOCK_STREAM)
# tcp_server.bind(('localhost',serverPort))
# tcp_server.listen(1)
# while 1:
# 	con, cliente = tcp_server.accept()
# 	message = con.recv(1500)
# 	modifiedMessage = alterMessage(message.decode())
# 	con.send(modifiedMessage.encode())