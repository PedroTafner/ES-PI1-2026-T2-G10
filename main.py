import opcoes

opcao=0
while opcao != 3:
    print("\n\t-- MENU PRINCIPAL --")
    print("\n1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Sair")

    opcao=int(input("\nEscolha uma opção: "))
    match opcao:
        case 1: #OPÇÃO GERENCIAMENTO
            opcoes.opcao_gerenciamento()
        case 2: #OPÇÃO VOTAÇÃO
            opcoes.opcao_votacao()
        case 3: #FIM DO PROGRAMA
            print("Programa finalizado.")
        case _: #OPÇÃO INEXISTENTE
            print("Opção Inválida")
