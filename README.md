# TCP-Quiz

## Requisitos

MySQL

Python 3.*

## Configuração

A configuração desse projeto esta centralizada no arquivo application.yml, é preciso fornecer configurações de host e banco de dados.

Além disso, temos uma pasta com arquivos de sql, que podem ser adicionados ao banco, para configurar o banco de dados e para que possa utilizar sem precisar criar quizzes de inicio, para executar esses arquivos no terminal, basta rodar o comando $mysql -u {SEU_USUARIO} -p < nome_do_arquivo.sql. Entre esses arquivos, temos cria_tabelas.sql, deve ser executado por primeiro, para criar a estrutura das tabelas, em seguida, temos o preenche_tabelas.sql, que vai inserir 2 quizzes e 5 pontuações, podendo assim, ja utilizar todas as funções do menu. Por último, temos também, um arquivo esvazia_tabelas.sql, que é opcional, caso queira resetar as tabelas.

Por fim, é preciso instalar as dependencias do python utilizadas no projeto, rodando o comando $pip3 install -r requirements.txt

## Descrição

Este projeto contém 2 arquivos .py com funções diferentes, sendo eles client.py e server.py que representam nosso cliente e servidor, o servidor precisa ser executado primeiro, para aguardar as conexões dos clientes. Enquanto o servidor estiver ligado, pode ser executado diversas instâncias de clientes, rodando  que irão ter suas conexões idependentes umas das outras.

Feita a conexão, basta digitar seu usuário, seguir os passos dos menus que serão apresentados pelo servidor e aproveitar os quizzes.

Comando para executar o servidor : python3 server.py
Comando para executar o cliente  : python3 client.py
