from socket import *

serverName='localhost'
serverPort= 8080
clientSocket = socket(AF_INET, SOCK_STREAM)
server = (serverName,serverPort)
clientSocket.connect(server)
message= input( ' Digite seu nome: ' )
while 1:
    clientSocket.send(message.encode())
    modifiedMessage, serverAddress=clientSocket.recvfrom(1500)
    print(modifiedMessage.decode())
    message = input(' ')
clientSocket.close()


# from socket import *
# serverName='localhost'
# serverPort= 8082
# tcp_client = socket(AF_INET, SOCK_STREAM)
# tcp_client.connect((serverName,serverPort))
# print ('Para digite \"exit\"')
# message = input( ' Digite sua mensagem: ' )
# while message != 'exit':
#     tcp_client.send(message.encode())
#     modifiedMessage, serverAddress = tcp_client.recvfrom(1500)
#     print(modifiedMessage.decode())
#     message = input()
# tcp_client.close()