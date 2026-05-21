import Arquivos_PY.gerenciamento as ger
import Arquivos_PY.votacao as vot

ger.limpar()
vot.arquivoTXT(2,'apagando log')
vot.reset_protocolo()
opcao=0

while opcao != 3:
    ger.limpar()
    print("\n\t-- MENU PRINCIPAL --")
    print("\n1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Sair")

    opcao=int(input("\nEscolha uma opção: "))
    match opcao:
        case 1: #OPÇÃO GERENCIAMENTO
            ger.opcao_gerenciamento()
        
        case 2: #OPÇÃO VOTAÇÃO
            vot.opcao_votacao()
        
        case 3:
            input("\nPrograma finalizado, tecle ENTER para fechar.")
            ger.limpar()
        
        case _:
            ger.limpar()