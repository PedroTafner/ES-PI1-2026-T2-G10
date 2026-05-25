def criptografia(opcao,dado):

    # A criptografia envolve o método da Cifra de Hills, que usa o cálculo C = A * P,
    # na qual o C é o texto criptografado, o A é matriz chave 2x2 necessária responsável por 
    # deixar o texto criptografado, e o P que é o texto normal.     
    
    # O A foi inserido numa lista, em que A[0] é a primeira linha da matriz, e a A[1] a segunda.
    
    # O dado (CPF, Protocolo de votação, Chave de Acesso) vai ser dividido em uma matriz de 2 linhas,
    # em que os caractéres ímpares (1º,3º,5º...) vão ser armazenados na linhas_dado[0]
    # e os caractéres pares (2º, 4º, 6º...) na linhas_dados[1]
    
    A=[[4,3],[1,2]]
    dado = str(dado)
    linhas_dado = [[],[]]
    alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

    # Opcões disponíveis: CPF (0), Chave de acesso(1) e Protocolo de votação (2)

    # Para o bom funcionamento da Cifra de Hills, o último digito do CPF e da Chave de acesso
    # precisaram ser duplicados

    if opcao == 0 or opcao ==1:
        dado += dado[len(dado)-1]

    # Cada opçao possui um contador, que se refere ao número de colunas da matriz P (cont1)
    # e para a contagem certe de for na qual o Protocolo e a Chave de acesso necessitam (cont2) 

    if opcao == 0: 
        cont1=6

        # Inserção dos dígitos do CPF no linhas_dado
        
        for i in range(0,11,2):
            num=dado[i]
            num=int(num)
            linhas_dado[0].append(num)

            num=dado[i+1]
            num=int(num)
            linhas_dado[1].append(num)

    elif opcao == 1 or opcao == 2:
        if opcao == 1:
            cont1=4
            cont2=8

        else:
            cont1=6
            cont2=12

        # Transformação das 3 primeiras letras da Chave de acesso e do Protocolo de votação
        # na posição dos mesmos na lista alfabeto + Inserção de dados no linhas_dado
        
        for i in range(1,cont2,2): 
            if i<4:
                num_letra = alfabeto.index(dado[i-1])
                num_letra = int(num_letra)
                linhas_dado[0].append(num_letra)
            else:
                linhas_dado[0].append(int(dado[i-1]))

            if i<3:
                num_letra = alfabeto.index(dado[i])
                num_letra = int(num_letra)
                linhas_dado[1].append(num_letra)
            else:
                linhas_dado[1].append(int(dado[i]))
   
   # Operação Cifra de Hills (C = A * P) + Substituição na lista linhas_dado

    for i in range(cont1):
        num1=A[0][0] * linhas_dado[0][i] + A[0][1] * linhas_dado[1][i]
        num1=int(num1)
        while num1 > 25:
            num1-=26
        while num1 < 0:
            num1+=26

        num2=A[1][0] * linhas_dado[0][i] + A[1][1] * linhas_dado[1][i]
        num2=int(num2)
        while num2 > 25:
            num2-=26
        while num2 < 0:
            num2+=26

        linhas_dado[0][i]=num1
        linhas_dado[1][i]=num2

    # Criptografia do resultado, optado pelo grupo por ser registrado com letras do alfabeto
    
    for i in range(cont1):
        alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
        linhas_dado[0][i] = alfabeto.pop(linhas_dado[0][i])
        alfabeto = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
        linhas_dado[1][i] = alfabeto.pop(linhas_dado[1][i])

    # Formação do dado criptografado
    
    dado_criptografado = ""
    for i in range(cont1):
        dado_criptografado += str(linhas_dado[0][i]) + str(linhas_dado[1][i])
        
    return dado_criptografado


cpf= '12345678901'
print(criptografia(0,cpf))

chave='ABCD'
print(criptografia(1,chave))

protocolo = 'ABCD'
print(criptografia(2,protocolo))