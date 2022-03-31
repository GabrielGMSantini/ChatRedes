# Importando a library de sockets
import socket	
# definindo tamanho do buffer		
bufferSize  = 1024
# Criando o objeto de socket
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)		
print ("Socket criado com sucesso")
# Definindo a porta que deve ser usada
port = 12345			
#Bindando a porta sem definir um ip especifico, para que, dessa forma, o socket escute a qualquer outro computador na rede
s.bind(('', port))		
print ("socket binded to %s" %(port))
# Colocando o server pra escutar
while(True):
    bytesAddressPair = s.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # respondendo ao cliente
    s.sendto(bytesToSend, address)
