# A. Manual de utilização

1. Colocar o arquivo *main.py* na pasta do freechains
2. Abrir o terminal nesta pasta e executar *python -i main.py*

- Com isso já foi criada uma pasta para o host, iniciado o host e feito join na cadeia

3. Para sair execute *encerrarServidor()* e em seguida *exit()*

# B. Comandos implementados

1. **Postar oferta:**
- postarOfertaAtacante(gols)
- postarOfertaDefensor(desarmes)
- postarOfertaGoleiro(altura)

2. **Fechar Oferta (os parâmetros devem ser os mesmos da criação da oferta):**
- fecharOfertaAtacante(gols)
- fecharOfertaDefensor(desarmes)
- fecharOfertaGoleiro(altura)

3. **Buscar Ofertas (Apenas ofertas com status aberto e reputação >= 0):**
- filtrarOfertasAbertas()

4. **Atualizar a cadeia:**
- enviarCadeiaPara(porta)
- pedirCadeiaPara(porta)

5. **Avaliar:**
- darLike(mensagem)
- darDislike(mensagem)

6. **Alterar Timestamp**
- setTimestamp(timestamp)

7. **Ver Reputação**
- verReputacao()

# C. Comandos não implementados

As chaves publicas e privadas não puderam ser geradas dinamicamente pois estavam gerando um bug em que só o primeiro bloco era inserido, consequentemente a função darlike(mensagem) não funciona pois o protocolo entende que está sendo atribuido um like para o próprio post *(chain like: like must not target itself)*. Apesar disso, ainda é possível usar o sistema de reputação ao esconder uma oferta dando um dislike.

# D. Ferramentas Utilizadas:

- Python
- Subprocess para executar os comandos do Freechains
- Random para gerar o username e escolher uma porta aleatória para o host
- Time para aplicar delays ao iniciar e encerrar o host
- Os para capturar o path