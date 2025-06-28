import src

def menu():
    print("""
        === Escolha uma opção === 
        1 - Buscar Ofertas
        2 - Postar Oferta
        3 - Fechar Oferta
        4 - Like
        5 - Dislike
        6 - Atualizar
        7 - Sair
""")
    
def menuOferta():
    print("""
        === Escolha uma Opção === 
        1 - Atacante
        2 - Defensor
        3 - Goleiro
""")
    
def buscarOfertas():
    src.exibirOfertasAbertas()

def postarOferta():
    menuOferta()
    c = int(input("Escolha uma opção -> "))
    if c == 1:
        gols = int(input("Quantos gols esse atacante fez? -> "))
        src.postarOfertaAtacante(gols)
    elif c == 2:
        desarmes = int(input("Quantos desarmes esse defensor fez? -> "))
        src.postarOfertaDefensor(desarmes)
    elif c == 3:
        altura = int(input("Qual a altura do goleiro? -> "))
        src.postarOfertaGoleiro(altura)

def fecharOferta():
    menuOferta()
    c = int(input("Escolha uma opção -> "))
    if c == 1:
        gols = int(input("Quantos gols esse atacante fez? -> "))
        src.fecharOfertaAtacante(gols)
    elif c == 2:
        desarmes = int(input("Quantos desarmes esse defensor fez? -> "))
        src.fecharOfertaDefensor(desarmes)
    elif c == 3:
        altura = int(input("Qual a altura do goleiro? -> "))
        src.fecharOfertaGoleiro(altura)

def like():
    cod = int(input("Insira o código da mensagem -> "))
    src.darLike(cod)

def dislike():
    cod = int(input("Insira o código da mensagem -> "))
    src.darDislike(cod)

def atualizar():
    src.atualizar()

def sair():
    src.encerrarServidor()
    exit(0)