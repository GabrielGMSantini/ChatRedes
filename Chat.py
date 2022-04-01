# Importando as bibliotecas necessárias
import socket
import threading
import time
import sys

# definindo o tamanho do buffer
bufferSize = 1024
bufferSize2 = 1024

# Criando os objetos de socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sockets criados com sucesso")

# Criando um Lock para controle
l = threading.Lock()

# Setando a porta que será utilizada
port = input('Porta do servidor: ')
port = int(port)

# Função CLiente


def Client():

    while(True):
        print('Clique ENTER para iniciar o envio')
        a = sys.stdin.read(1)
        l.acquire()
        print('IP Destinatário: ')
        IPDest = input()
        serverAddressPort = (IPDest, port)
        msg = input('Mensagem: ')
        a = sys.stdin.read(1)
        bytesToSend = str.encode(msg)
        s.sendto(bytesToSend, serverAddressPort)
        ack_thread = threading.Thread(target=EsperaAck)
        ack_thread.start()
        l.release()

# Função Servidor


def Server():

    # Bind da porta sem IP específico, a fim de escutar qualquer outro computador na rede
    s2.bind(('', port))
    print("Bind feito na porta %s" % (port))

    ackFromServer = "ACK"
    ServerResponse = str.encode(ackFromServer)

    while(True):
        bytesAddressPair = s2.recvfrom(bufferSize2)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        mostra_thread = threading.Thread(
            target=MostraMensagem, args=(message, address))
        mostra_thread.start()

        # respondendo ao cliente
        s2.sendto(ServerResponse, address)

# Função de Espera da Resposta


def EsperaAck():

    RcvMsg = s.recvfrom(bufferSize)
    msg2 = "Message of ACK {}".format(RcvMsg[0])
    print(msg2)


def MostraMensagem(message, address):

    l.acquire()
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    Resposta = input("Resposta: ")
    bytesToResend = str.encode(Resposta)
    s.sendto(bytesToResend, address)
    l.release()


server_thread = threading.Thread(target=Server)
client_thread = threading.Thread(target=Client)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()
