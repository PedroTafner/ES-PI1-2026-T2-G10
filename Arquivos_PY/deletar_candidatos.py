import mysql.connector

# 1. Definição da Função
def deletar_candidato(conexao, cursor, numero_candidato):
    # Pede a confirmação do usuário
    confirmacao = input(f"Tem certeza que deseja deletar o candidato nº {numero_candidato}? (s/n): ")

    # Se a resposta NÃO for "s", cancela e sai da função
    if confirmacao.lower() != "s":  
        print("Operação cancelada.")
        return  

    # Comando SQL com %s (marcador de posição) por segurança
    sql = "DELETE FROM candidatos WHERE numero = %s"
    valor = (numero_candidato,)  # Tupla de um elemento só

    
    cursor.execute(sql, valor)
    conexao.commit() # Salva as alterações no banco

    # Verifica se alguma linha foi afetada (se o candidato existia)
    if cursor.rowcount > 0:
        print("\n--- CANDIDATO REMOVIDO ---")
        print(f"  Numero: {numero_candidato}")
        print("--------------------------\n")
    else:
        print(f"Nenhum candidato encontrado com o número {numero_candidato}.")

    host="localhost",
    user="root",          # Seu usuário do MySQL
    password="sua_senha",  # Sua senha do MySQL
    database="seu_banco"   # Nome do seu banco de dados
)

cursor = conexao.cursor()

print("--- SISTEMA DE EXCLUSÃO DE CANDIDATOS ---")

num_para_deletar = input("Digite o número do candidato que deseja deletar: ")

deletar_candidato(conexao, cursor, num_para_deletar)

# 6. Fechando as conexões
cursor.close()
conexao.close()
print("Conexão fechada com sucesso.")