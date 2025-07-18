# A. Manual de utilização

1. Clonar o repositório;
2. Entrar no diretório e instalar o Freechains;
    - wget https://github.com/Freechains/README/releases/download/v0.10.1/install-v0.10.1.sh
    - sh install-v0.10.1.sh .
3. Iniciar a aplicação com *python main.py*;
4. Utilizar a aplicação conforme o menu.

- Obs: Caso a aplicação quebre, é necessário apagar a porta no arquivo *pares.txt* e encerrar o processo com o comando *fuser -k porta/tcp*, por exemplo 
.
# B. Funcionalidades implementadas
1. Iniciar leilão;
2. Submeter lances para um leilão;
3. Filtragem de leilões dentre todos os blocos;
4. Filtragem de lances dentre todos os blocos;
5. Eleição do lance vencedor com base no valor e na reputação;
6. Atualização da cadeia de forma facilitada;
7. Atribuição de like e dislike;
8. Exibição de lances e leilões.

# C. Funcionalidades não implementadas
1. Encerramento de leilão;
2. Retirada de lances.

# D. Ferramentas Utilizadas:

- Python
- Subprocess para executar os comandos do Freechains
- Random para gerar o username e escolher uma porta aleatória para o host
- Time para aplicar delays ao iniciar e encerrar o host
- Os para capturar o path