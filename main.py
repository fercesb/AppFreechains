import menuSrc, src

forum = "#forum"
chavePioneiro = "99CA7DC51444DE55E0A71697C95EC5170CDF7C115A59733769A1E9ED60A4A403"
porta = src.selecionarPorta()
username = src.gerarUsername()
diretorio = src.definirDiretorio(username)

src.iniciarHost(porta, diretorio)

chaves = src.gerarChaves(porta, username)
chavePublica = chaves[0]
chavePrivada = chaves[1]

src.entrarNaCadeia(porta, forum, chavePioneiro)

while True:

    menuSrc.menuPrincipal()

    try:
        c = int(input("Escolha uma opção -> "))
    except ValueError:
        print("Opção inválida!")
        continue

    if c == 1:
        menuSrc.buscarLeiloesAbertos(porta, forum)
    elif c == 2:
        menuSrc.iniciarLeilao(porta, forum, chavePrivada)
    elif c == 3:
        menuSrc.enviarLance(porta, forum, chavePrivada)
    elif c == 4:
        menuSrc.elegerVencedor(porta, forum)
    elif c == 5:
        menuSrc.like(porta, forum, chavePrivada)
    elif c == 6:
        menuSrc.dislike(porta, forum, chavePrivada)
    elif c == 7:
        menuSrc.atualizar(porta, forum)
    elif c == 8:
        menuSrc.verReputação(porta, forum, chavePublica)
    elif c == 9:
        menuSrc.sair(porta)
