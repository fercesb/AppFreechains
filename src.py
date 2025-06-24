import subprocess, random, string, time, os, ast

def escreverNoArquivo(porta):
    with open("pares.txt", "a") as arquivo:
        arquivo.write(f"{porta}\n")

def apagarNoArquivo(porta):
    with open("pares.txt", "r") as arquivo:
        linhas = arquivo.readlines()

    with open("pares.txt", "w") as arquivo:
        for linha in linhas:
            try:
                if int(linha.strip()) != porta:
                    arquivo.write(linha)
            except ValueError:
                # Caso a linha não seja um número válido
                arquivo.write(linha)

def lerPortas():
    with open("pares.txt", "r") as arquivo:
        portas = [int(linha.strip()) for linha in arquivo]
    return portas

def gerarUsername():
    caracteres = string.ascii_lowercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

def gerarChaves():
    chaves = subprocess.run(["./freechains", f"--host=localhost:{porta}", "keys", "pubpvt", f"{username}"],  stdout=subprocess.PIPE, text=True)
    return chaves.stdout.strip().split()

def entrarNaCadeia():
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chains", "join", f"{forum}", f"{chavePioneiro}"])

def sairDaCadeia():
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chains", "leave", f"{forum}"])

def verReputacao(value=None):

    # Retornar reputação de uma mensagem
    if value != None:
        rep = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "reps", f"{value}"], stdout=subprocess.PIPE, text=True)
        return int(rep.stdout.strip())

    # Retornar reputação de um usuário
    rep = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "reps", f"{chavePublica}"], stdout=subprocess.PIPE, text=True)
    return int(rep.stdout.strip())

def avaliarReputacao():
    rep = verReputacao()
    if rep >= 0:
        return True
    if rep <= -3:
        print("Sua reputação está muito baixa! Você está sendo removido da cadeia")
        sairDaCadeia()
    return False

def gerarTemplate(posicao, valor, status):

    dic = {}

    dic['codigo'] = random.randint(1000, 9999)
    dic['posicao'] = posicao
    dic['caracteristica'] = valor
    dic['contato'] = emailContato
    dic['status'] = status

    return dic

def iniciarServidor():
    escreverNoArquivo(porta)
    subprocess.Popen(["./freechains-host", f"--port={porta}", "start", f"{diretorioChain}"])
    time.sleep(2)

def encerrarServidor():
    subprocess.Popen(["./freechains-host", f"--port={porta}", "stop"])
    apagarNoArquivo(porta)
    time.sleep(2)

def postarOfertaAtacante(gols):
    template = gerarTemplate("Atacante", gols, "Aberta")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaAtacante(gols):
    template = gerarTemplate("Atacante", gols, "Fechada")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def postarOfertaDefensor(desarmes):
    template = gerarTemplate("Defensor", desarmes, "Aberta")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaDefensor(desarmes):
    template = gerarTemplate("Defensor", desarmes, "Fechada")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])
    
def postarOfertaGoleiro(altura):
    template = gerarTemplate("Goleiro", altura, "Aberta")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaGoleiro(altura):
    template = gerarTemplate("Goleiro", altura, "Fechada")
    if avaliarReputacao():
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def enviarCadeiaPara(portaDest=8330):
    avaliarReputacao()
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{portaDest}", "send", f"{forum}"])

def pedirCadeiaPara(portaDest=8330):
    avaliarReputacao()
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{portaDest}", "recv", f"{forum}"])

def buscarBlocos():
    # Buscar todos os heads
    saida = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "consensus"],
                   capture_output=True,
                   text=True)
    
    heads = saida.stdout.strip().split()

    # Armazenar em um dicionário o head, payload, status e reputação de cada bloco
    lista = []
    for head in heads:

        pl = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "get", "payload", f"{head}"], stdout=subprocess.PIPE, text=True)
        pl = pl.stdout.strip()

        if pl != '':
            lista.append(ast.literal_eval(pl))

            indice = len(lista) - 1
            lista[indice]['reputacao'] = verReputacao(head)
            lista[indice]['head'] = head

    return lista

def filtrarOfertasAbertas():
    blocos = buscarBlocos()

    for i in blocos:
        for j in blocos:
            if i['posicao'] == j['posicao'] and i['caracteristica'] == j['caracteristica'] and i['contato'] == j['contato'] and i['status'] != j['status']:
                blocos.remove(i)
                blocos.remove(j)

    return blocos

def exibirOfertasAbertas():
    avaliarReputacao()
    
    lista = filtrarOfertasAbertas()

    print("\n=== Ofertas Abertas ===\n")

    for item in lista:
        if item['reputacao'] >= 0:
            print(f"Código: {item['codigo']}")

            posicao = item['posicao']
            print(f"Posição: {posicao}")

            if posicao == "Atacante":
                print(f"Gols: {item['caracteristica']}")
            if posicao == "Defensor":
                print(f"Desarmes: {item['caracteristica']}")
            if posicao == "Goleiro":
                print(f"Altura: {item['caracteristica']}")

            print(f"Contato: {item['contato']}\n")
        
def darLike(value):

    # Like se for uma chave pública
    if type(value) is not int and len(value) == 64:
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "like", f"{value}", f"--sign={chavePrivada}"])
        return

    # Like se for uma mensagem
    blocos = buscarBlocos()

    for bloco in blocos:
        if bloco['codigo'] == value:
            head = bloco['head']
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "like", f"{head}", f"--sign={chavePrivada}"])

def darDislike(value):

    # Dislike se for uma chave pública
    if type(value) is not int and len(value) == 64:
        subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "like", f"{value}", f"--sign={chavePrivada}"])
        return

    # Dislike se for uma mensagem
    blocos = buscarBlocos()

    for bloco in blocos:
        if bloco['codigo'] == value:
            head = bloco['head']
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "dislike", f"{head}", f"--sign={chavePrivada}"])

def setTimestamp(timestamp):
    subprocess.run(["./freechains-host", "now", f"{timestamp}"])

def atualizar():
    portas = lerPortas()
    for port in portas:
        if port != porta:
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{port}", "recv", f"{forum}"])

username = gerarUsername()
diretorioChain = os.getcwd() + f"/{username}"
forum = "#forum"
porta = random.randint(4000, 4100)
chavePioneiro = "99CA7DC51444DE55E0A71697C95EC5170CDF7C115A59733769A1E9ED60A4A403"
emailContato = username + "@email.com"

iniciarServidor()

# Gerar as chaves. Comentado pois possui bug
#chavePublica, chavePrivada = gerarChaves()

chavePublica = "99CA7DC51444DE55E0A71697C95EC5170CDF7C115A59733769A1E9ED60A4A403"
chavePrivada = "C922B9D924D48A4D51C9F8881E7F1D9A6C8492CD576CA6CF3B23D0A385C10FDD99CA7DC51444DE55E0A71697C95EC5170CDF7C115A59733769A1E9ED60A4A403"

entrarNaCadeia()