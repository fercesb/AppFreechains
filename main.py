import src, menu

while True:
    menu.menu()
    c = int(input("Escolha uma opção -> "))

    if c == 1:
        menu.buscarOfertas()
    elif c == 2:
        menu.postarOferta()
    elif c == 3:
        menu.fecharOferta()
    elif c == 4:
        menu.atualizar()
    elif c == 5:
        menu.sair()
    else:
        print("Opção inválida!")
