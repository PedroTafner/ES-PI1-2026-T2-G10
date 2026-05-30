def descriptografia(opcao,texto):

    """
    A descriptografia envolve o método da Cifra de Hills, que usa o cálculo P = (1/A) * C,
    na qual o C é o texto criptografado, o inverso de A (1/a) é matriz chave 2x2 necessária responsável por 
    deixar o texto descriptografado, e o P que é o texto normal.     
    
    O 1/A (representado na função como 'A') foi inserido numa lista, em que A[0] é a primeira linha da matriz, e a A[1] a segunda.
    
    O dado (CPF, Protocolo de votação, Chave de Acesso) vai ser dividido em uma matriz de 2 linhas,
    em que os caractéres ímpares (1º,3º,5º...) vão ser armazenados na linhas_crip[0]
    e os caractéres pares (2º, 4º, 6º...) na linhas_crip[1]
    
    Args:
        opcao (0: CPF; 1: Chave de acesso; 2: Protocolo de votacao)
        dado: respectiva informacao criptografada de acordo com a sua opção

    Returns:
        (str): o dado informado descriptografado
    """

    A=[[42,-63],[-21,84]]
    linhas_crip = [[], []]
    alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

    # Opcões disponíveis: CPF (0), Chave de acesso(1) e Protocolo de votação (2)

    # Cada opçao possui um contador, que se refere ao número de colunas da matriz P (cont1)
    # e para a contagem certe de for na qual o Protocolo e a Chave de acesso necessitam (cont2)

    if opcao == 0 or opcao == 2:
        cont1=6
        cont2=11
    elif opcao == 1:
        cont1=4
        cont2=7

    # Inserção das letras do texto criptografado no linhas_crip

    for i in range(0,cont2,2):
        letra=texto[i]
        linhas_crip[0].append(letra)

        letra = texto[i+1] 
        linhas_crip[1].append(letra)
    
    # Transformação das letras do texto criptografado na sua respectiva posição da lista alfabeto

    for i in range(cont1):
        linhas_crip[0][i] = alfabeto.index(linhas_crip[0][i])
        linhas_crip[1][i] = alfabeto.index(linhas_crip[1][i])

    # Operação Cifra de Hills (P = A * C) + Substituição na lista linhas_crip

    for i in range(cont1):
        num1=A[0][0] * linhas_crip[0][i] + A[0][1] * linhas_crip[1][i]
        num1=int(num1)
        while num1 > 25:
            num1-=26
        while num1 < 0:
            num1+=26

        num2=A[1][0] * linhas_crip[0][i] + A[1][1] * linhas_crip[1][i]
        num2=int(num2)
        while num2 > 25:
            num2-=26
        while num2 < 0:
            num2+=26

        linhas_crip[0][i]=num1
        linhas_crip[1][i]=num2

    # Transformação dos 3 primeiros dígitos em letras do alfabeto para a Chave de Acesso e o Protocolo de Votação

    if opcao == 1 or opcao == 2:
        for i in range(2): #0 2
            alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
            linhas_crip[0][i] = alfabeto.pop(linhas_crip[0][i])

            if i==0:
                alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
                linhas_crip[1][i] = alfabeto.pop(linhas_crip[1][i])
    
    # Formação do dado descriptografado

    dado_descriptografado = ""
    for i in range(cont1):
        dado_descriptografado += str(linhas_crip[0][i]) + str(linhas_crip[1][i])

    if opcao == 0 or opcao == 1:
        dado_descriptografado = dado_descriptografado[:cont2]

    return dado_descriptografado