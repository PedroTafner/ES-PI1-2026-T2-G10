import Arquivos_PY.gerenciamento as ger
import Arquivos_PY.votacao as vot


ger.limpar()
vot.arquivoTXT(2,'apagando log') # RESETA OS LOGS DE OCORRÊNCIAS DO SISTEMA
vot.reset_protocolo() # RESETA A LISTA DE PROTOCOLOS E DEIXA O STATUS DE VOTO DOS ELEITORES PARA 0
opcao=0

while opcao != 3:
    ger.limpar()
    print("\n\t-- MENU PRINCIPAL --")
    print("\n1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Sair")

    opcao=int(input("\nEscolha uma opção: "))
    match opcao:
        case 1:  #OPÇÃO GERENCIAMENTO
            ger.opcao_gerenciamento()
        
        case 2: # OPÇÃO VOTAÇÃO
            vot.opcao_votacao()
        
        case 3: # FINALIZA O PROGRAMA
            input("\nPrograma finalizado, tecle ENTER para fechar.")
            ger.limpar()
        
        case _:
            ger.limpar()