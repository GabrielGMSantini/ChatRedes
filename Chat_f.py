# Importando as bibliotecas necessárias
import socket
import threading
import time
import json


# definindo funções de manipulação JSON
def codificarMensagem(IP_origem, IP_destino, Porta_origem, Porta_destino, Timestamp, Mensagem):
    x = {
        "IP_origem": IP_origem,
        "IP_destino": IP_destino,
        "Porta_origem": Porta_origem,
        "Porta_destino": Porta_destino,
        "Timestamp da mensagem": Timestamp,
        "Mensagem": Mensagem
    }
    return json.dumps(x)


def codificarACK(IP_origem, IP_destino, Porta_origem, Porta_destino, Timestamporiginal, Timestampresposta, ACK):
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


def codificarResposta(IP_origem, IP_destino, Porta_origem, Porta_destino, Timestamporiginal, Timestampresposta, Mensagemoriginal, Mensagemresposta):
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


# Criando uma função para printar o menu
def printMenu():
    print("\n-----------------Menu-----------------")
    print("\nDigite [E] para Escrever uma mensagem")
    print("Digite [R] para Responder uma mensagem")


# definindo o tamanho dos buffers
bufferSize = 1024
bufferSize2 = 1024

# Criando os objetos de socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sockets criados com sucesso")

# Criando um Lock para controle
l = threading.Lock()

# Setando o IP do servidor
ip = input('Seu IP: ')

# Setando a porta do servidor
port = input('Sua Porta: ')
port = int(port)

# Declaração da flag usada no menu para controle de thread
global flagMenu
flagMenu = 0


# Função Cliente
def Client():

    # fazendo o bind do socket do cliente (necessário para conseguir recuperar a porta antes de ter enviado alguma coisa)
    s.bind(('', port+1))
    global flagMenu
    flagMenu = 5
    while(True):
        # Para começar a enviar uma mensagem, é pedido que o usuário digite ENTER
        if flagMenu != 0 and flagMenu != 2:
            l.acquire()
            time.sleep(2)
            printMenu()
            flagMenu = 0
            l.release()
            print('\n>> ', end='')
        choice = input()
        if choice == 'E':
            flagMenu = 1
        elif choice == 'R':
            flagMenu = 2
        elif choice == "":
            flagMenu = 0
        else:
            flagMenu = -1
        if flagMenu == 1:
            l.acquire()
            print("\n------------Enviando Mensagem------------")
            # Input do IP e da Porta do destinatário da mensagem
            IPDest = input('\nIP Destinatário: ')
            portaDest = input('\nPorta do Destinatário: ')
            portaDest = int(portaDest)
            # Armazenando a porta e o IP em um objeto
            serverAddressPort = (IPDest, portaDest)
            # Input da mensagem a ser enviada
            msg = input('\nMensagem: ')

            bytesToSend = str.encode(codificarMensagem(
                ip, IPDest, s.getsockname()[1], portaDest, time.time(), msg))
            # Envio da mensagem para o IP e a porta selecionadas
            s.sendto(bytesToSend, serverAddressPort)
            # Chamada da função de espera de ACK em outra thread
            ack_thread = threading.Thread(target=EsperaAck)
            ack_thread.start()
            flagMenu = 0
            l.release()
        elif flagMenu == -1:
            print("\n\tOpção Inválida!!")


# Função Servidor
def Server():

    # Bind da porta sem IP específico, a fim de escutar qualquer outro computador na rede
    s2.bind(('', port))
    s3.bind(('', port-1))
    print("Bind feito na porta %s" % (port))
    while(True):
        # Servidor espera uma mensagem chegar para devolver outra de ACK
        bytesAddressPair = s2.recvfrom(bufferSize2)
        JSON = bytesAddressPair[0]
        address = bytesAddressPair[1]
        # JSON da mensagem é recebido como byte e transformado em JSON
        decodedJSON = json.loads(JSON)
        print("\nJSON da Mensagem:")
        print(decodedJSON)
        # Respondendo o ACK ao cliente
        s2.sendto(str.encode(codificarACK(ip, decodedJSON["IP_origem"], decodedJSON["Porta_destino"],
                  decodedJSON["Porta_origem"], decodedJSON["Timestamp da mensagem"], time.time(), True)), address)

        # Chamada da função que mostra a mensagem e procede para resposta
        mostra_thread = threading.Thread(
            target=MostraMensagem, args=(decodedJSON["IP_origem"], decodedJSON["Porta_origem"], decodedJSON["Timestamp da mensagem"], decodedJSON["Mensagem"], address))
        mostra_thread.start()


# Função de Espera da Resposta
def EsperaAck():
    s.settimeout(10)
    try:
        RcvMsg = s.recvfrom(bufferSize)
        s.settimeout(None)
        JSONACK = RcvMsg[0]
        decodedACK = json.loads(JSONACK)
        print("\nMensagem Entregue")
        print("ACK : " + str(decodedACK["ACK"]))
        print("\nJSON do ACK:")
        print(decodedACK)
        EsperaResposta()
    except Exception:
        print("\nMensagem não encontrou o alvo")
        print("ACK : False")
        printMenu()
        print('\n>> ', end='')
    s.settimeout(None)


# Função que mostra a mensagem e produz uma resposta
def MostraMensagem(IP_origem, Porta_origem, Timestamp, Mensagem, address):

    message = Mensagem
    global flagMenu
    flagReturn = 0
    # Na tela é mostrada a mensagem e o IP do cliente
    print("\n---------Mensagem Recebida---------")
    clientMsg = "\nMensagem do Cliente: {}".format(message)
    clientIP = "\nIP do Cliente: {}".format(IP_origem)
    print(clientMsg)
    print(clientIP)
    print("\nDigite [E] para Ignorar e Escrever uma mensagem")
    print("Digite [R] para Responder a mensagem")
    print("\n>> ", end='')
    while True:
        if flagMenu == 2:
            l.acquire()
            # Input da Resposta para o cliente
            print("\n\nDigite [ENTER] para começar resposta")
            print("\n>> ", end='')
            Resposta = input("\nResposta: ")
            bytesToResend = str.encode(codificarResposta(ip, IP_origem, s2.getsockname()[
                1], Porta_origem, Timestamp, time.time(), Mensagem, Resposta))
            time.sleep(1)
            s3.sendto(bytesToResend, address)
            print("\n\nResposta Enviada com Sucesso")
            printMenu()
            print("\n>> ", end='')
            l.release()
            break


def EsperaResposta():

    print("\nEsperando Resposta...")
    RcvMsg = s.recvfrom(bufferSize)
    JSONResposta = RcvMsg[0]
    decodedResposta = json.loads(JSONResposta)
    msgOriginal = "\n\nMensagem Original: {}".format(
        decodedResposta["Mensagem Original"])
    msg2 = "\nMensagem de Resposta: {}".format(
        decodedResposta["Mensagem de resposta"])
    clientIP = "\nIP da Resposta: {}".format(decodedResposta["IP_origem"])
    print(msgOriginal)
    print(clientIP)
    print(msg2)
    print("\nJSON da Resposta:")
    print(decodedResposta)
    printMenu()
    print("\n>> ", end='')


# Criação das threads de servidor e cliente
server_thread = threading.Thread(target=Server)
client_thread = threading.Thread(target=Client)

# Começo das threads
server_thread.start()
client_thread.start()

# server_thread.join()
# client_thread.join()
