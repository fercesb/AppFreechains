import subprocess, random, string, time, os

def gerarUsername():
    caracteres = string.ascii_lowercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

def gerarChaves():
    chaves = subprocess.run(["./freechains", f"--host=localhost:{porta}", "keys", "pubpvt", f"{username}"],  stdout=subprocess.PIPE, text=True)
    return chaves.stdout.strip().split()

def iniciarServidor():
    subprocess.Popen(["./freechains-host", f"--port={porta}", "start", f"{diretorioChain}"])
    time.sleep(2)

def encerrarServidor():
    subprocess.Popen(["./freechains-host", f"--port={porta}", "stop"])
    time.sleep(2)

def entrarNaCadeia():
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chains", "join", f"{forum}", f"{chavePioneiro}"])

def postarOfertaGoleiro(altura):
    template =  f"Posição: Goleiro / Altura: {altura} / Contato: {emailContato} / Status: Aberta"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaGoleiro(altura):
    template =  f"Posição: Goleiro / Altura: {altura} / Contato: {emailContato} / Status: Fechada"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def postarOfertaDefensor(desarmes):
    template = f"Posição: Defensor / Desarmes: {desarmes} / Contato: {emailContato} / Status: Aberta"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaDefensor(desarmes):
    template = f"Posição: Defensor / Desarmes: {desarmes} / Contato: {emailContato} / Status: Fechada"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])
    
def postarOfertaAtacante(gols):
    template = f"Posição: Atacante / Gols: {gols} / Contato: {emailContato} / Status: Aberta"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def fecharOfertaAtacante(gols):
    template = f"Posição: Atacante / Gols: {gols} / Contato: {emailContato} / Status: Fechada"
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "post", "inline", f"{template}", f"--sign={chavePrivada}"])

def enviarCadeiaPara(portaDest=8330):
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{portaDest}", "send", f"{forum}"])

def pedirCadeiaPara(portaDest=8330):
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "peer", f"localhost:{portaDest}", "recv", f"{forum}"])

def buscarBlocos():
    # Buscar todos os heads
    saida = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "consensus"],
                   capture_output=True,
                   text=True)
    
    heads = saida.stdout.strip().split()

    # Armazenar em um dicionário o head, payload, status e reputação de cada bloco
    blocos, contador = {}, 0
    for head in heads:

        blocos[contador] = {}

        blocos[contador]["head"] = head

        pl = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "get", "payload", f"{head}"], stdout=subprocess.PIPE, text=True)
        pl = pl.stdout.strip()

        blocos[contador]["payload"] = pl

        blocos[contador]["status"] = pl[pl.find("Status: ") + len("Status: "):]

        rep = subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "reps", f"{head}"], stdout=subprocess.PIPE, text=True)
        blocos[contador]["reputacao"] = int(rep.stdout.strip())

        contador += 1

    return blocos

def filtrarOfertasAbertas():
    blocos = buscarBlocos()

    # Armazenar em uma lista todas as ofertas
    abertas = []
    for chave, bloco in blocos.items():
        if bloco["status"] == "Aberta" and int(bloco["reputacao"]) >= 0:
            abertas.append(bloco["payload"])

    # Remover da lita ofertas que foram fechadas
    for chave, bloco in blocos.items():
        for payload in abertas:
            
            # Remover o "Status" do payload para fazer a comparação
            cutbc = bloco["payload"].split(".com")[0] + ".com"
            cutpl = payload.split(".com")[0] + ".com"

            if bloco["status"] == "Fechada" and cutbc == cutpl:
                abertas.remove(payload)

    # Exibir todas as ofertas abertas
    print("\n=== Ofertas Abertas ===\n")
    for payload in abertas:    
        print(f"{payload}\n")
    print("\n")

def darLike(mensagem):
    blocos = buscarBlocos()

    # Comparar todos os payloads com a mensagem do parâmetro
    for chave, bloco in blocos.items():
        if bloco["payload"] == mensagem:
            head = bloco["head"]
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "like", f"{head}", f"--sign={chavePrivada}"])

def darDislike(mensagem):
    blocos = buscarBlocos()

    # Comparar todos os payloads com a mensagem do parâmetro
    for chave, bloco in blocos.items():
        if bloco["payload"] == mensagem:
            head = bloco["head"]
            subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "dislike", f"{head}", f"--sign={chavePrivada}"])

def setTimestamp(timestamp):
    subprocess.run(["./freechains-host", "now", f"{timestamp}"])

def verReputacao():
    subprocess.run(["./freechains", f"--host=localhost:{porta}", "chain", f"{forum}", "reps", f"{chavePublica}"], stdout=subprocess.PIPE, text=True)

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