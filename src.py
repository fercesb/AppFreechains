import subprocess, random, string, time, math, ast, os

# ===== FUNÇÕES AUXILIARES ===== #

# Escolher a porta do host de forma aleatória
def selecionarPorta():
    return random.randint(4000, 4100)

# Gerar um username aleatório
def gerarUsername():
    caracteres = string.ascii_lowercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

# Definir o diretório do host baseado no username
def definirDiretorio(username):
    return os.getcwd() + f"/{username}"

# Gerar as chaves publica e privada de forma dinâmica
def gerarChaves(porta, username):
    chaves = subprocess.run(["./freechains", f"--host=localhost:{porta}", "keys", "pubpvt", username],  stdout=subprocess.PIPE, text=True)
    return chaves.stdout.strip().split()

# Capturar a reputação através da chave
def verReputacao(porta, forum, chavePublica):
    rep = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "reps", f"{chavePublica}"], stdout=subprocess.PIPE, text=True)
    return int(rep.stdout.strip())

# Fazer a escrita da porta de um host no arquivo pares.txt
def escreverNoArquivo(porta):
    with open("pares.txt", "a") as arquivo:
        arquivo.write(f"{porta}\n")

# Apagar um valor no arquivo pares.txt
def apagarNoArquivo(porta):
    with open("pares.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    with open("pares.txt", "w") as arquivo:
        for linha in linhas:
            try:
                if int(linha.strip()) != porta:
                    arquivo.write(linha)
            except ValueError:
                arquivo.write(linha)

# Ler as portas do arquivo pares.txt
def lerPortas():
    with open("pares.txt", "r") as arquivo:
        portas = [int(linha.strip()) for linha in arquivo]
    return portas

# Gerar o template de um leilao
def gerarTemplateIniciacao(agente, jogador, valor, chave, status):

    dic = {}

    dic['tipo'] = "leilao"
    dic['codigo'] = random.randint(1000, 9999)
    dic['agente'] = agente
    dic['jogador'] = jogador
    dic['contato'] = agente + "@email.com"
    dic['valor'] = valor
    dic['status'] = status
    dic['userKey'] = chave[64:]
    dic['userRep'] = 0
    dic['head'] = None

    return dic

# Gerar o template de um lance
def gerarTemplateLance(nome, codigo, valor, chave, status):

    dic = {}

    dic['tipo'] = "lance"
    dic['codigo'] = random.randint(1000, 9999)
    dic['nome'] = nome
    dic['codigoLeilao'] = codigo
    dic['valorLance'] = valor
    dic['contato'] = nome + "@email.com"
    dic['status'] = status
    dic['userKey'] = chave[64:]
    dic['userRep'] = 0
    dic['valorPonderado'] = 0
    dic['head'] = None

    return dic

# ===== FUNÇÕES DE HOST ===== #

# Iniciar o host
def iniciarHost(porta, diretorio):
    escreverNoArquivo(porta)
    subprocess.Popen(["./freechains-host", f"--port={porta}", "start", diretorio],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    time.sleep(2)

# Encerrar o host
def encerrarHost(porta):
    subprocess.Popen(["./freechains-host", f"--port={porta}", "stop"])
    apagarNoArquivo(porta)
    time.sleep(2)

# Entrar na cadeia
def entrarNaCadeia(porta, forum, chavePioneiro):
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chains", "join", forum, chavePioneiro])

# Sair da cadeia
def sairDaCadeia(porta, forum):
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chains", "leave", forum])

# ===== FUNÇÕES DE CADEIA ===== #

# Realizar o post de um leilão
def iniciarLeilao(agente, jogador, valor, porta, forum, chavePrivada):
    template = gerarTemplateIniciacao(agente, jogador, valor, chavePrivada, "Aberto")
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "post", "inline", f"{template}", f"--sign={chavePrivada}"])

# Realizar o fechamento de um leilão (não utilizado)
def finalizarLeilao(agente, jogador, valor, porta, forum, chavePrivada):
    template = gerarTemplateIniciacao(agente, jogador, valor, chavePrivada, "Encerrado")
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "post", "inline", f"{template}", f"--sign={chavePrivada}"])

# Realizar o envio de um lance
def enviarLance(nome, codigo, valor, porta, forum, chavePrivada):
    template = gerarTemplateLance(nome, codigo, valor, chavePrivada, "Válido")
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "post", "inline", f"{template}", f"--sign={chavePrivada}"])

# Realizar o cancelamento de um lance (não utilizado)
def retirarLance(nome, codigo, valor, porta, forum, chavePrivada):
    template = gerarTemplateLance(nome, codigo, valor, chavePrivada, "Cancelado")
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "post", "inline", f"{template}", f"--sign={chavePrivada}"])

# Capturar todos os blocos da cadeia (exceto o genesis)
def parseCadeia(porta, forum, blocked):

    # Capturar todos os heads
    saida = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "consensus"],
                   capture_output=True,
                   text=True)
    
    heads = saida.stdout.strip().split()

    # Transformar os heads em payloads
    lista = []
    for head in heads:

        pl = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "get", "payload", head], stdout=subprocess.PIPE, text=True)
        pl = pl.stdout.strip()

        if pl != '':
            lista.append(ast.literal_eval(pl))

            indice = len(lista) - 1
            lista[indice]['head'] = head

    # Se incluir mensagens bloqueadas...
    if blocked == True:
        
        # Capturar todos os heads bloqueados
        saida = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "heads", "blocked"],
                   capture_output=True,
                   text=True)
        
        headsBlocked = saida.stdout.strip().split()

        # Transformar os heads bloqueados em payloads
        for head in headsBlocked:

            pl = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", forum, "get", "payload", head], stdout=subprocess.PIPE, text=True)
            pl = pl.stdout.strip()

            if pl != '':
                lista.append(ast.literal_eval(pl))

                indice = len(lista) - 1
                lista[indice]['head'] = head

    return lista

# Selecionar apenas os leilões dentre todos os blocos
def filtrarLeiloesAbertos(porta, forum, blocked):
    blocos = parseCadeia(porta, forum, blocked)

    # Selecionar apenas blocos com o tipo "leilao"
    leiloes = [b for b in blocos if b['tipo'] == "leilao"]

    return leiloes
            
# Selecionar apenas os lances dentre todos os blocos
def filtrarLancesAbertos(porta, forum, blocked):
    blocos = parseCadeia(porta, forum, blocked)

    # Selecionar apenas blocos com tipo "lance"
    lances = [b for b in blocos if b['tipo'] == "lance"]

    return lances

# Eleger o lance vencedor
def elegerMelhorLance(codigo, porta, forum, blocked):
    lances = filtrarLancesAbertos(porta, forum, blocked)

    # Selecionar os lances referentes ao leilão indicado
    lances = [b for b in lances if b['codigoLeilao'] == codigo]

    maiorLancePonderado = -99999999999999999
    codigoMaiorLance = None
    
    for lance in lances:
        # Capturar a reputação do autor
        lance['userRep'] = verReputacao(porta, forum, lance['userKey'])

        # Se a reputação for maior do que 0, pondera. Caso contrário valorPonderado = 0
        if lance['userRep'] > 0:
            lance['valorPonderado'] = lance['valorLance'] * math.log10(lance['userRep'])

        # Alterar o lance vencedor se for o caso
        if lance['valorPonderado'] > maiorLancePonderado:
            maiorLancePonderado = lance['valorPonderado']
            codigoMaiorLance = lance['codigo']

    return codigoMaiorLance

# Atualizar a cadeia consultando todos os pares
def atualizarCadeia(porta, forum):
    
    #Faz um recv para todas as portas no arquivo pares.txt, exceto sua própria porta
    portas = lerPortas()
    for port in portas:
        if port != porta:
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{port}", "recv", forum])

# Realizar a exibição de todos os leilões
def exibirLeiloesAbertos(porta, forum, blocked):
    leiloes = filtrarLeiloesAbertos(porta, forum, blocked)

    print("\n===== Leilões Abertos =====\n")

    for leilao in leiloes:
        print(f"Código: {leilao['codigo']}")
        print(f"Agente: {leilao['agente']}")
        print(f"Jogador: {leilao['jogador']}")
        print(f"Lance Mínimo: ${leilao['valor']}")
        print(f"Contato: {leilao['contato']}")
        print("\n")

# Realizar a exibição do lance vencedor atual
def exibirMelhorLance(codigo, porta, forum, blocked):
    codigo = elegerMelhorLance(codigo, porta, forum, blocked)
    blocos = filtrarLancesAbertos(porta, forum, blocked)

    for bloco in blocos:
        if bloco['codigo'] == codigo:
            print("\n===== Melhor Lance Atual =====\n")
            print(f"Nome do ganhador: {bloco['nome']}")
            print(f"Valor: {bloco['valorLance']}")

# Atribuir um like a uma postagem
def darLike(value, porta, forum, chavePrivada):
    blocos = parseCadeia(porta, forum, True)

    for bloco in blocos:
        if bloco['codigo'] == value:
            head = bloco['head']
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "like", f"{head}", f"--sign={chavePrivada}"])

# Atribuir um dislike a uma postagem
def darDislike(value, porta, forum, chavePrivada):
    blocos = parseCadeia(porta, forum, True)

    for bloco in blocos:
        if bloco['codigo'] == value:
            head = bloco['head']
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "dislike", f"{head}", f"--sign={chavePrivada}"])