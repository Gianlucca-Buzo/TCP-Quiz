USE tcp_quiz;

INSERT INTO Quizzes VALUES 
    ('1234','{"descricao": "Informacoes sobre a Isa","perguntas":{"1":{  "textoQuestao":"Qual a idade da Isa?",  "alternativaCorreta":"c",  "alternativas":{ "a":"19", "b":"22", "c":"21", "d":"18", "e":"20"  }},"2":{  "textoQuestao":"Qual o nome completo da Isa?",  "alternativaCorreta":"a",  "alternativas":{ "a":"Isabela Fernandes Gomes Dias", "b":"Isabella Gomes Fernandes Dias", "c":"Isabela Dias Fernandes Gomes", "d":"Isabella Fernandes Gomes Dias", "e":"Isabela Gomes Dias Fernandes"  }},"3":{  "textoQuestao":"Aonde a Isa nasceu?",  "alternativaCorreta":"d",  "alternativas":{ "a":"Porto Alegre", "b":"Pelotas", "c":"Foz do Iguacu", "d":"Sao Paulo", "e":"Sao Lourenco"  }},"4":{  "textoQuestao":"Qual o nome do namorado da Isa?",  "alternativaCorreta":"e",  "alternativas":{ "a":"Cleiton", "b":"Lucas", "c":"Fabricio", "d":"Fabio", "e":"Lucca"  }},"5":{  "textoQuestao":"Qual a profissao da Isa?",  "alternativaCorreta":"b",  "alternativas":{ "a":"Secretaria", "b":"Engenheira de Software", "c":"Astronauta", "d":"Cantora Pop", "e":"Fisiculturista"  }}} }'),
    ('4321','{"descricao": "Informacoes sobre o Lucca","perguntas":{"1":{"textoQuestao":"Qual a idade do Lucca?","alternativaCorreta":"c","alternativas":{"a":"19","b":"22","c":"21","d":"18","e":"20"}},"2":{"textoQuestao":"Qual o nome completo do Lucca?","alternativaCorreta":"a","alternativas":{"a":"Gianlucca de Mendonca Buzo","b":"Lucca de Mendeonca Buzo","c":"Gianlucca Buzo de Mendonca","d":"Gian Lucca de Mendonca Buzo","e":"Lucca Buzo de Mendonca"}},"3":{"textoQuestao":"Aonde a Lucca nasceu?","alternativaCorreta":"b","alternativas":{"a":"Porto Alegre","b":"Pelotas","c":"Foz do Iguacu","d":"Sao Paulo","e":"Sao Lourenco"}},"4":{"textoQuestao":"Qual o nome da namorada do Lucca?","alternativaCorreta":"d","alternativas":{"a":"Fernanda","b":"Roberta","c":"Claudia","d":"Isabela","e":"Julia"}},"5":{"textoQuestao":"Qual a profissao do Lucca?","alternativaCorreta":"b","alternativas":{"a":"Jogador de Volei","b":"Engenheira de Software","c":"Piloto de Formula 1","d":"Rapper","e":"Fisiculturista"}}}}');

INSERT INTO Pontuacoes (Pin,Usuario,Pontuacao) VALUES
    ('1234','user1',3),
    ('1234','user3',2),
    ('1234','user5',0),
    ('4321','user2',5),
    ('4321','user7',1),
    ('4321','user6',2);