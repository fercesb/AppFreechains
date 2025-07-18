import src

def menuPrincipal():
    print("""
        === Escolha uma opção ===
        1 - Buscar Leilões Abertos
        2 - Iniciar Leilão
        3 - Enviar Lance
        4 - Ver Vencedor Atual
        5 - Dar Like
        6 - Dar Dislike
        7 - Atualizar Cadeia
        8 - Ver Minha Reputação
        9 - Sair
""")
    
def buscarLeiloesAbertos(porta, forum):
    print("""
        Listar também mensagens bloqueadas?
        1 - Sim
        2 - Não
    """)
    c = int(input("Escolha uma opção -> "))
    if c == 1:
        src.exibirLeiloesAbertos(porta, forum, True)
    elif c == 2:
        src.exibirLeiloesAbertos(porta, forum, False)

def iniciarLeilao(porta, forum, chavePrivada):
    agente = input("Como você quer ser chamado? -> ")
    jogador = input("Qual é o nome do jogador? -> ")
    valor = int(input("Qual o valor do lance mínimo? -> "))
    src.iniciarLeilao(agente, jogador, valor, porta, forum, chavePrivada)
    print("Leilão iniciado com sucesso!")

def enviarLance(porta, forum, chavePrivada):
    nome = input("Como você quer ser chamado? -> ")
    codigo = int(input("Qual é o código do leilão? -> "))
    valor = int(input("Qual é o valor do seu lance? -> "))
    src.enviarLance(nome, codigo, valor, porta, forum, chavePrivada)
    print("Lance enviado com sucesso!")

def retirarLance(porta, forum, chavePrivada):
    nome = input("Qual nome você insetiu no lance? -> ")
    codigo = int(input("Qual o código do lance? -> "))
    valor = int(input("Qual era o valor do lance? -> "))  
    src.retirarLance(nome, codigo, valor, porta, forum, chavePrivada)

def elegerVencedor(porta, forum):
    codigo = int(input("Qual é o código do leilão? -> "))
    print("""
        Considerar lances bloqueados?
        1 - Sim
        2 - Não
    """)
    c = int(input("Escolha uma opção -> "))
    if c == 1:
        src.exibirMelhorLance(codigo, porta, forum, True)
    if c == 2:
        src.exibirMelhorLance(codigo, porta, forum, False)

def like(porta, forum, chavePrivada):
    value = int(input("Informe o código do leilão a dar like -> "))
    src.darLike(value, porta, forum, chavePrivada)

def dislike(porta, forum, chavePrivada):
    value = int(input("Informe o código do leilão a dar dislike -> "))
    src.darDislike(value, porta, forum, chavePrivada)

def atualizar(porta, forum):
    src.atualizarCadeia(porta, forum)

def verReputação(porta, forum, chave):
    src.verReputacao(porta, forum, chave)

def sair(porta):
    src.encerrarHost(porta)
    exit(0)