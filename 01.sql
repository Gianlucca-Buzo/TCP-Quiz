DROP DATABASE tcp_quiz;
CREATE DATABASE tcp_quiz;
USE tcp_quiz;

CREATE TABLE Quizzes (
    Pin VARCHAR(4) NOT NULL,
    Quiz_Json TEXT NOT NULL,
    PRIMARY  KEY (`Pin`)
);

CREATE TABLE Pontuacoes (
    Pin VARCHAR(4) NOT NULL REFERENCES `Quizzes` (`Pin`),
    Usuario VARCHAR(15) NOT NULL,
    Pontuacao INT NOT NULL,
    PRIMARY  KEY (`Pin`,`Usuario`)
);


