# A. Manual de utilização

1. Colocar o arquivo *main.py* na pasta do freechains
2. Abrir o terminal nesta pasta e executar *python main.py*

- Com isso já foi criada uma pasta para o host, iniciado o host e feito join na cadeia

# B. Comandos implementados

1. **Postar oferta (Necessário reputação >= 0 para postar):**
- postarOfertaAtacante(gols)
- postarOfertaDefensor(desarmes)
- postarOfertaGoleiro(altura)

2. **Fechar Oferta (Os parâmetros devem ser os mesmos da criação da oferta):**
- fecharOfertaAtacante(gols)
- fecharOfertaDefensor(desarmes)
- fecharOfertaGoleiro(altura)

3. **Buscar Ofertas (Apenas ofertas com status aberto e reputação >= 0):**
- exibirOfertasAbertas()

4. **Atualizar a cadeia:**
- enviarCadeiaPara(porta)
- pedirCadeiaPara(porta)

5. **Avaliar:**
- darLike(value)
- darDislike(value)

6. **Alterar Timestamp**
- setTimestamp(timestamp)

7. **Ver Reputação (O usuário pode ser removido da cadeia dependendo da reputação)**
- verReputacao()

# C. Comandos não implementados
No momento as chaves estão hard coded para facilitar testes

# D. Ferramentas Utilizadas:

- Python
- Subprocess para executar os comandos do Freechains
- Random para gerar o username e escolher uma porta aleatória para o host
- Time para aplicar delays ao iniciar e encerrar o host
- Os para capturar o path