CREATE DATABASE tcp_quiz;
USE tcp_quiz;

CREATE TABLE Quizzes (
    Pin VARCHAR(4) NOT NULL,
    Quiz_Json TEXT NOT NULL,
    PRIMARY  KEY (`Pin`)
);

CREATE TABLE Jogadores (
    ID_Jogador BIGINT NOT NULL AUTO_INCREMENT,
    Usuario VARCHAR(15) NOT NULL,
    PRIMARY  KEY (`ID_Jogador`,`Usuario`)
);

CREATE TABLE Pontuacoes (
    Pin VARCHAR(4) NOT NULL REFERENCES `Quizzes` (`Pin`),
    ID_Jogador BIGINT NOT NULL REFERENCES `Jogadores` (`ID_Jogador`),
    PRIMARY  KEY (`Pin`,`ID_Jogador`)
);


