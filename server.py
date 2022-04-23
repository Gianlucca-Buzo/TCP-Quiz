from socket import *
import mysql.connector
import json
import random

connection_code = 1500
serverPort = 8080
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)
letras = ['a','b','c','d','e']
mysql_cnx = mysql.connector.connect(user='root', password='lucca2021',
                              host='localhost',
                              database='quiz')

# choice = input(Fore.CYAN + f"\n Bem vindo ao Quiz {name}\n O que deseja fazer?\n 1 - Jogar um Quiz\n 2 - Listar os Quiz existentes\n 3 - Criar um Quiz\n ")
def criaQuizManualmente():
    envia("Digite a descricao do Quiz: ")
    descricao = recebe()
    json_questao = dict()
    pin = str(random.randint(999,9999))
    json_questao['pin'] = pin
    json_questao['descricao'] = descricao
    perguntas = dict()
    for i in range(1,2):
        pergunta = dict()
        envia(f"Digite a perguna numero {i}: ")
        textoQuestao = recebe()
        pergunta['textoQuestao'] = textoQuestao
        alternativas = dict()
        for letra in letras:
            envia(f"Digite a resposta letra {letra}:")
            resposta = recebe()
            alternativas[letra] = resposta
        envia("Digite a alternativa correta para esta questao: ")
        alternativaCorreta = recebe()
        while not letras.__contains__(alternativaCorreta):
            envia("Alternativa inexistente\nDigite a alternativa correta para esta questao: ")
            alternativaCorreta = recebe()
        pergunta['alternativaCorreta'] = alternativaCorreta
        pergunta['alternativas'] = alternativas
        perguntas[str(i)] = pergunta
    json_questao['perguntas'] = perguntas
    envia(f"Quiz criado pin: {pin}")
    print(json.dumps(json_questao, indent=4))


def criaQuiz():
    envia("Criar Quiz: \n 1 - JSON\n 2 - Manualmente")
    opcao = recebe()
    if opcao == "1":
        envia("Digite o JSON do Quiz: ")
        json_quiz = recebe()
        print(f"Json recebido {json_quiz}")
    elif opcao == "2":
        criaQuizManualmente()
    else:
        envia("Opcao Invalida!")
        
def envia(mensagem):
    connection.sendall(mensagem.encode())

def recebe():
    return connection.recv(connection_code).decode()



if __name__ == '__main__':
    print("Quiz server is on!")
    while 1:
        connection, clientAddress = serverSocket.accept()
        nome = recebe()
        while 1:
            envia(f"\n Bem vindo ao Quiz {nome}\n O que deseja fazer?\n 1 - Jogar um Quiz\n 2 - Listar os Quizzes existentes\n 3 - Criar um Quiz\n 4 - Sair\n ")
            opcao = recebe()
            if opcao == "1":
                envia("Digite o pin do Quiz: ")
            elif opcao == "2":
                envia("Listar")
            elif opcao == "3":
                criaQuiz()
            elif opcao == "4":
                break
            else:
                envia("Opcao Invalida!")
        connection.close()




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