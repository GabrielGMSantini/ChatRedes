# Importando as bibliotecas necessárias
import socket
import threading
import time
import sys
import json


#definindo funções de manipulação JSON
import json

def codificarMensagem(IP_origem,IP_destino,Porta_origem,Porta_destino,Timestamp,Mensagem):
    x={
        "IP_origem": IP_origem,
        "IP_destino": IP_destino,
        "Porta_origem": Porta_origem,
        "Porta_destino": Porta_destino,
        "Timestamp da mensagem": Timestamp,
        "Mensagem": Mensagem
    }
    return json.dumps(x)

def codificarACK(IP_origem,IP_destino,Porta_origem,Porta_destino,Timestamporiginal,Timestampresposta,ACK):
    x = {
        "IP_origem": IP_origem,
        "IP_destino": IP_destino,
        "Porta_origem": Porta_origem,
        "Porta_destino": Porta_destino,
        "Timestamp da mensagem original": Timestamporiginal,
        "Timestamp da mensagem de resposta": Timestampresposta,
        "ACK": ACK
    }
    return json.dumps(x)

def codificarResposta(IP_origem,IP_destino,Porta_origem,Porta_destino,Timestamporiginal,Timestampresposta,Mensagemoriginal,Mensagemresposta):
    x = {
        "IP_origem": IP_origem,
        "IP_destino": IP_destino,
        "Porta_origem": Porta_origem,
        "Porta_destino": Porta_destino,
        "Timestamp da mensagem original": Timestamporiginal,
        "Timestamp da mensagem de resposta": Timestampresposta,
        "Mensagem Original": Mensagemoriginal,
        "Mensagem de resposta": Mensagemresposta
    }
    return json.dumps(x)




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
    
    #fazendo o bind do socket do cliente (necessário para conseguir recuperar a porta antes de ter enviado alguma coisa)
    s.bind(('', port+1))
    while(True):
        # Para começar a enviar uma mensagem, é pedido que o usuário digite ENTER
        print('Digite ENTER para iniciar o envio')
        a = sys.stdin.read(1)
        l.acquire()
        # Input do IP do destinatário da mensagem
        IPDest = input('\nIP Destinatário: ')
        portaDest = input('\nPorta do Destinatário: ')
        # Armazenando a porta e o IP em um objeto
        serverAddressPort = (IPDest, portaDest)
        # Input da mensagem a ser enviada
        msg = input('Mensagem: ')
        
        bytesToSend = str.encode(codificarMensagem(socket.gethostbyname(socket.gethostname()), IPDest,s.getsockname()[1], portaDest, time.time(), msg))
        # Envio da mensagem para o IP e a porta selecionadas
        s.sendto(bytesToSend, serverAddressPort)
        # Chamada da função de espera de ACK em outra thread
        ack_thread = threading.Thread(target=EsperaAck)
        ack_thread.start()
        l.release()


# Função Servidor
def Server():

    # Bind da porta sem IP específico, a fim de escutar qualquer outro computador na rede
    s2.bind(('', port))
    print("Bind feito na porta %s" % (port))
    while(True):
        bytesAddressPair = s2.recvfrom(bufferSize2)
        l.acquire()
        JSON = bytesAddressPair[0]
        address = bytesAddressPair[1]
        decodedJSON = json.loads(JSON)
        # respondendo ao cliente
        s2.sendto(str.encode(codificarACK(socket.gethostbyname(socket.gethostname()), decodedJSON["IP_origem"],decodedJSON["Porta_destino"],decodedJSON["Porta_origem"],decodedJSON["Timestamp da mensagem"], time.time(),True)), address)
        l.release()

        mostra_thread = threading.Thread(
            target=MostraMensagem, args=(decodedJSON))
        mostra_thread.start()


# Função de Espera da Resposta
def EsperaAck():

    RcvMsg = s.recvfrom(bufferSize)
    JSONACK = RcvMsg[0]
    decodedACK = json.loads(JSONACK)
    print("ACK :" + str(decodedACK["ACK"]))
    EsperaResposta()


# Função que mostra a mensagem e produz uma resposta
def MostraMensagem(decodedJSON):

    l.acquire()
    message = decodedJSON["Mensagem"]
    address = decodedJSON["IP_origem"]
    # Na tela é mostrada a mensagem e o IP do cliente
    clientMsg = "\n\tMensagem do Cliente:{}".format(message)
    clientIP = "\tIP do Cliente:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # Input da Resposta para o cliente
    Resposta = input("\nResposta: ")
    bytesToResend = str.encode(codificarResposta(socket.gethostbyname(socket.gethostname()), decodedJSON["IP_origem"], s2.getsockname()[1], decodedJSON["Porta_origem"], decodedJSON["Timestamp da mensagem"], time.time(), decodedJSON["Mensagem"], Resposta))
    s2.sendto(bytesToResend, (address, decodedJSON["Porta_origem"]))
    l.release()


def EsperaResposta():

    RcvMsg = s.recvfrom(bufferSize)
    JSONResposta = RcvMsg[0]
    decodedResposta = json.loads(JSONResposta)
    msgOriganal = "\n\tMensagem Original: {}".format(decodedResposta["Mensagem Original"])
    msg2 = "\n\tMensagem de Resposta {}".format(decodedResposta["Mensagem de resposta"])
    clientIP = "\tIP da Resposta:{}".format(decodedResposta["IP_origem"])
    print(msgOriganal)
    print(clientIP)
    print(msg2)


# Criação das threads de servidor e cliente
server_thread = threading.Thread(target=Server)
client_thread = threading.Thread(target=Client)

# Começo das threads
server_thread.start()
client_thread.start()

# server_thread.join()
# client_thread.join()
