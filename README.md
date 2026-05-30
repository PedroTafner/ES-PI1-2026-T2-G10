# ES-PI1-2026-T2-G10
Projeto Integrador 1

Descrição: Projeto com o intuito de criar um sistema backend de votação digital fictício, com a integração prática de conhecimentos das áreas de Lógica de Programação em Python, manipulação de banco de dados com SQL e aplicação de conceitos matemáticos (como Álgebra Linear) voltados à proteção da informação.

Integrantes do Grupo:
- Arthur Paioli  
- Daniel Castro  
- João Felipe Bodo Pinheiro  
- Pedro Osti  
- Pedro Tafner  

Tecnologias Utilizadas:
- Linguagem de Programação: Python
- Banco de Dados: MySQL  
- Biblioteca de Conexão com o Banco: mysql-connector-python  
- Bibliotecas Python Utilizadas:
  - datetime (manipulação de data e hora)  
  - random (geração de valores aleatórios)  
  - os (manipulação de arquivos e diretórios)  
  - time (controle de tempo de execução)  
- Ambiente de Desenvolvimento: Visual Studio Code (VsCode)
- Controle de Versão: Git e GitHub

Instruções para execução do sistema:

- Ter MySQL WorkBench instalado na máquina
- Criar um banco de dados, seguindo o script anexado na pasta "Outros"
- Clonar o repositório para sua máquina utilizando Git Bash
- Abrir projeto utilizando VSCode ou Pycharm e instalar as extensões do Python
- Executar arquivo "main"
- Use o menu de gerenciamento para cadastrar eleitores, editar dados, adicionar candidatos, remover eleitores, etc...
- Use o menu de votação para abrir o sistema de votação (caso seja mesário) para conseguir votar após a abertura você pode votar com qualquer eleitor
- No menu de votação existem também os sistemas de auditoria das votações, onde você pode ver os logs de ocorrências, protocolos de votação (que são gerados quando você vota) e, além disso, no menu de votação, você ainda pode conferir os resultados da votação, como o boletim de urna, estatísticas de comparecimento, votos por partido e validação de integridade.