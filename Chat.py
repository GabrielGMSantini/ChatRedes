# Importando a biblioteca socket
import socket

# Importando a biblioteca Threading
from threading import Thread

# definindo o tamanho do buffer
bufferSize = 1024
bufferSize2 = 1024

# Criando os objetos de socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sockets criados com sucesso")

port = input('Porta usada: ')
port = int(port)


def Client():

    IPDest = input('IP Destinatário: ')
    serverAddressPort = (IPDest, port)

    while(True):
        msg = input('Mensagem: ')
        bytesToSend = str.encode(msg)
        s.sendto(bytesToSend, serverAddressPort)

        ack_thread.start()
        ack_thread.join()


def Server():

    # Bind da porta sem IP específico, a fim de escutar qualquer outro computador na rede
    s2.bind(('', port))
    print("Bind feito na porta %s" % (port))

    msgFromServer = "ACK"
    ServerResponse = str.encode(msgFromServer)

    while(True):
        bytesAddressPair = s2.recvfrom(bufferSize2)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        # respondendo ao cliente
        s2.sendto(ServerResponse, address)


def EsperaAck():

    RcvMsg = s.recvfrom(bufferSize)
    msg2 = "Message of ACK {}".format(RcvMsg[0])
    print(msg2)


server_thread = Thread(target=Server)
client_thread = Thread(target=Client)
ack_thread = Thread(target=EsperaAck)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()
