from socket import *
import mysql.connector
import json
import random
import yaml

with open('application.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

size = data['size']
serverPort = data['serverPort']
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)
letras = ['a','b','c','d','e']
mysql_cnx = mysql.connector.connect(user=data['mysql_user'], password=data['mysql_password'],
                              host=data['mysql_host'],
                              database=data['mysql_database'])
cursor = mysql_cnx.cursor()

def salvaPontuacao (usuario,pin,pontuacao):
    query = (f'INSERT INTO Pontuacoes (Pin,Usuario,Pontuacao) VALUES ("{pin}","{usuario}","{pontuacao}");')
    cursor.execute(query)
    mysql_cnx.commit()


def selecionarQuiz(pin):
    query = (f'SELECT Quiz_Json FROM Quizzes WHERE Pin = {pin};')
    cursor.execute(query)
    for row in cursor:
        json_acceptable_string = row[0].replace("'", "\"")
        quiz_json = json.loads(json_acceptable_string)
    return quiz_json


def listarQuizzes():
    query = (f'SELECT * FROM Quizzes;')
    cursor.execute(query)
    for row in cursor:
        pin = row[0]
        json_acceptable_string = row[1].replace("'", "\"")
        quiz_json = json.loads(json_acceptable_string)
        descricao = quiz_json["descricao"]
        envia(f'\nPin: {pin}\nDescricao: {descricao}\n')

def salvaQuiz(pin,json):
    query = (f'INSERT INTO Quizzes (Pin,Quiz_Json) VALUES ("{pin}","{json}");')
    cursor.execute(query)
    mysql_cnx.commit()


def criaQuizManualmente():
    envia("\nDigite a descricao do Quiz: ")
    descricao = recebe()
    json_questao = dict()
    pin = str(random.randint(999,9999))
    json_questao['pin'] = pin
    json_questao['descricao'] = descricao
    perguntas = dict()
    for i in range(1,6):
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
    salvaQuiz(pin,json_questao)


def criaQuiz():
    envia("\nCriar Quiz: \n 1 - JSON\n 2 - Manualmente\n")
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
    return connection.recv(size).decode()



if __name__ == '__main__':
    print("Quiz server is on!")
    while 1:
        connection, clientAddress = serverSocket.accept()
        usuario = recebe()
        while 1:
            envia(f"\n Bem vindo ao Quiz, {usuario}\n O que deseja fazer?\n 1 - Jogar um Quiz\n 2 - Listar os Quizzes existentes\n 3 - Criar um Quiz\n 4 - Sair\n ")
            opcao = recebe()
            if opcao == "1":
                envia("Digite o pin do Quiz: ")
                pin = recebe()
                quiz_json = selecionarQuiz(pin)
                salvaPontuacao(usuario,pin,5) #Teste
            elif opcao == "2":
                listarQuizzes()
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