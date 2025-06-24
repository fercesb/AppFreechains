import src

def menu():
    print("""
        === Escolha uma opção === 
        1 - Buscar Ofertas
        2 - Postar Oferta
        3 - Fechar Oferta
        4 - Atualizar
        5 - Sair
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

def atualizar():
    src.atualizar()

def sair():
    src.encerrarServidor()
    exit(0)