<h1 align="center"> Chat entre Terminais usando Socket e Threads </h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=FINALIZADO&color=BLUE&style=for-the-badge"/>
</p>

<h2> ✍ Descrição do Projeto </h2>

Projeto feito no laboratório 04 da disciplina de Redes de Computadores A, sobre o oitavo semestre do curso de Engenharia da Computação lecionado pelo professor Leandro Alonso Xastre, na Pontifícia Universidade Católica de Campinas, no ano de 2022.

O projeto consiste em desenvolver um chat de terminal para linux onde um cliente e um servidor em computadores diferentes consigam mandar mensagens, receber confirmação de envio desta mensagem e enviar uma resposta para o mesmo IP do remetente da mensagem. A linguagem escolhida para a realização do mesmo foi o Python, com o uso de threads e sockets.

## :hammer: Funcionalidades do projeto

- `Envio de Mensagem`: Definindo-se um IP para a máquina e sua porta, é possível enviar mensagens utilizando soquetes.
- `Receber ACK`: Para verificar se a mensagem chegou com sucesso no destinatário escolhido, é possível receber um sinal de ACK
- `Envio de Resposta`: Com a confirmação de recebimento de mensagem, é possível que o destinatário da mensagem mande uma resposta para o servidor de quem a enviou

## 📁 Acesso ao projeto

O Acesso ao projeto é feito pelo Download do arquivo "Chat.py", sendo o Python 3 necessário para o rodar no terminal.

## 🛠️ Abrir e rodar o projeto

Ao executar o arquivo, primeiro é pedido que o usuário digite seu IP e a porta que o seu servidor usará, o que é importante para que outros usuários possam mandar mensagens nesse servidor. Desta forma, um menu irá aparecer com opções de envio e resposta. A opção de resposta apenas funcionará se houver alguma mensagem recebida pelo servidor.
Escolhida a opção de envio, primeiro o sistema irá perguntar o IP e a porta do destinatário da mensagem e por fim, pedirá que o usuário escreva a mensagem, o que fará com que o servidor espere uma mensagem de ACK.
Caso o ACK seja positivo, o sistema irá esperar uma resposta do destinatário, mas caso não seja, irá notificar o recebimento negativo do ACK e voltará ao menu.

Para responder uma mensagem após recebê-la, o usuário deverá escolher a opção de resposta e logo após, teclar ENTER por medida de segurança a fim da limpeza de buffer, mandando assim a resposta que será notificada na tela de quem mandou a mensagem inicial.

## ✅ Tecnologias Usadas

Python

<h2> 👥 Integrantes do Projeto </h2>

<h3>Gabriel Gonçalves Mattos Santini</h3>
<h3>Gustavo Campos Dias</h3>
<h3>Gustavo Melo Cacau</h3>
