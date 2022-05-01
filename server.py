from socket import *
import mysql.connector
import json
import random
import yaml
from colorama import Fore

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

def listaPontuacoes (pin):
    query = (f'SELECT Usuario,Pontuacao FROM Pontuacoes WHERE Pin = "{pin}" ORDER BY (Pontuacao) DESC;')
    cursor.execute(query)
    lista = f'\nUSUARIO - PONTUACAO'
    for row in cursor:
        usuario = row[0]
        pontuacao = row[1]
        lista = lista + f'\n{usuario} - {pontuacao}'
    envia(lista+ '\n')


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


def listarQuizzes():
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
    envia(lista)

def salvaQuiz(pin,json):
    query = (f'INSERT INTO Quizzes (Pin,Quiz_Json) VALUES ("{pin}","{json}");')
    cursor.execute(query)
    mysql_cnx.commit()

def jogar(usuario,pin):
    quiz = selecionarQuiz(pin)
    perguntas = quiz['perguntas']
    respostas_corretas = 0
    for i in range(1,6):
        pergunta = perguntas[str(i)]
        questao_string = f"\nQuestao {i}: {pergunta['textoQuestao']}\n"
        alternativas = pergunta['alternativas']
        for letra in letras:
            questao_string = questao_string + f"{letra}) {alternativas[letra]} \n"
        envia(questao_string)
        resposta = recebe()
        if(resposta == pergunta['alternativaCorreta']):
            respostas_corretas += 1
            envia(Fore.GREEN+' Resposta Correta'+Fore.WHITE)
        else:
            envia(Fore.RED + " Resposta Incorreta"+Fore.WHITE)
    
    salvaPontuacao(usuario,pin,respostas_corretas)
    envia(Fore.GREEN+f' Voce acertou {respostas_corretas} questoes\n\nRank: \n'+Fore.WHITE)
    listaPontuacoes(pin)

    

def criaQuiz():
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
            envia(f"\n Bem vindo ao Quiz, {usuario}\n O que deseja fazer?\n 1 - Jogar um Quiz\n 2 - Listar os Quizzes existentes\n 3 - Criar um Quiz\n 4 - Visualizar Ranking \n 5 - Sair\n ")
            opcao = recebe()
            if opcao == "1":
                envia("Digite o pin do Quiz: ")
                pin = recebe()
                if not existe_pontuacao(pin,usuario):
                    quiz_json = selecionarQuiz(pin)
                    if quiz_json == None:
                        envia("\nNao existe quiz com esse PIN!\n")
                    else:
                        jogar(usuario,pin)
                        #salvaPontuacao(usuario,pin,5) #Teste
                else:
                    envia("\nVoce ja jogou esse quiz antes!\n")
            elif opcao == "2":
                listarQuizzes()
            elif opcao == "3":
                criaQuiz()
            elif opcao == "4":
                envia("Digite o pin do Quiz: ")
                pin = recebe()
                listaPontuacoes(pin)
            elif opcao == "5":
                connection.close()
            else:
                envia("Opcao Invalida!")


