/*  hosname: localhost
	user: 'root'
	password: Zxxyf1
*/

CREATE DATABASE pi1_2026;
USE pi1_2026;

CREATE TABLE candidatos (
    id_candidato INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    partido VARCHAR(50) NOT NULL,
    num_votacao INT NOT NULL
);

CREATE TABLE eleitores (
    id_eleitor INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(12) UNIQUE NOT NULL,
    mesario BOOLEAN DEFAULT FALSE,
    chave_acesso VARCHAR(8) UNIQUE NOT NULL,
    titulo_eleitor VARCHAR(50) UNIQUE NOT NULL,
    status_voto BOOLEAN DEFAULT FALSE
);

CREATE TABLE resultado (
    id_resultado INT PRIMARY KEY AUTO_INCREMENT,
    protocolo_votacao VARCHAR(12),
    horario_votacao DATETIME,
    id_candidato INT NOT NULL,

    FOREIGN KEY (id_candidato)
        REFERENCES candidatos(id_candidato)
);
