from socket import *

serverName='localhost'
serverPort= 8080
clientSocket = socket(AF_INET, SOCK_STREAM)
server = (serverName,serverPort)
clientSocket.connect(server)
message= input( ' Digite seu usuario: ' )
while 1:
    clientSocket.send(message.encode())
    modifiedMessage, serverAddress=clientSocket.recvfrom(1500)
    print(modifiedMessage.decode())
    if(modifiedMessage.decode() == 'Fechando Conexao'):
        break
    message = input(' ')
clientSocket.close()
print('Conexao Fechada')