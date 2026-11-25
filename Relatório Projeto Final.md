# Relatório Técnico — Clínica MedTec (Sistema de Agendamentos)

## 1\. Identificação

- **Nome completo:** Vitória Souza Reis  
- **Data de entrega:** 25/11/2026  
- **Nome e descrição do sistema:** Clínica MedTec — Um site feito em Python (Flask) e SQLite para cadastrar pacientes e marcar consultas, mostrando tudo organizado por dia e horário.

---

## 2\. Descrição do Sistema

Fiz o **Clínica MedTec** pensando em como funciona a recepção de um consultório pequeno. Muitas clínicas ainda anotam os horários em cadernos ou planilhas, querendo ou não fica mais fácil confundir o horário de alguém, perder o telefone do paciente ou marcar duas pessoas ao mesmo tempo, desorganizando tudo.

Meu sistema resolve isso juntando o cadastro de pacientes e a agenda de consultas num lugar só. Na primeira página aparecem todas as consultas marcadas, já em ordem de dia e hora, com um campo de busca para achar de forma rápida pelo nome do paciente, pelo motivo ou pela data. Também dá pra editar e apagar consultas no mesmo canto. Na segunda página ficam os pacientes cadastrados, onde dá para adicionar, mudar os dados ou excluir. O site funciona tanto no computador quanto no celular, sendo ele responsivo, o que facilita sua utilização.

---

## 3\. Decisões Técnicas

- **Por que você escolheu esse tema/problema?**  
  Escolhi fazer um sistema de agendamentos porque é uma coisa que existe de verdade no dia a dia de qualquer clínica e porque eu já conseguia imaginar bem como as duas tabelas (pacientes e consultas) iam se ligar uma na outra.  
    
- **Quais foram as maiores dificuldades no desenvolvimento? Como você as resolveu?**  
  A parte que mais deu trabalho foi fazer a lista de consultas aparecer na ordem certa de dia e hora usando um algoritmo em Python, e também garantir que, quando eu apagasse um paciente, as consultas dele não ficassem perdidas no banco. Para resolver a ordem, eu fiz a função `ordenar_consultas_por_data_hora` usando Bubble Sort. Já no banco, eu ativei o `PRAGMA foreign_keys = ON` e coloquei `ON DELETE CASCADE` na chave estrangeira, aí quando apaga o paciente, as consultas dele vão junto automaticamente.  
    
- **Como você organizou o banco de dados? Descreva as tabelas e o relacionamento entre elas.**  
  Usei o SQLite (`clinica.db`) com duas tabelas bem diretas:  
    
  - `pacientes`: guarda o `id` (chave primária), `nome`, `telefone` e `data_nascimento`.  
  - `consultas`: guarda o `id` (chave primária), `paciente_id` (que liga com o `id` do paciente), `data`, `hora` e `motivo`. A relação entre elas é de **1 para N**, ou seja, um mesmo paciente pode marcar várias consultas em dias diferentes, mas cada consulta é de um único paciente.


- **Qual parte do sistema você mais se orgulha? Por quê?**  
  A parte que eu mais gostei de fazer foi a tela principal com a tabela ordenada por dia e hora junto com o filtro de busca. Ficou bem limpa, fácil de mexer e deu uma sensação boa ver tudo funcionando junto sem precisar abrir um monte de páginas diferentes.

---

## 4\. Conexão com as UCs

- **UC30 · Lógica de Programação:**  
  A lógica aparece na função `ordenar_consultas_por_data_hora` lá no `app.py`, onde eu usei o Bubble Sort com laços `for` e `if/else` pra comparar a data e a hora de cada consulta e colocar em ordem. Também usei funções e condicionais para validar os formulários antes de salvar e para formatar a data pro padrão brasileiro.  
    
- **UC31 · Interface e Usabilidade:**  
  Fiz o visual com HTML e CSS no arquivo `static/style.css`, usando duas páginas (`Consultas` e `Pacientes`) com um menu simples no topo para trocar entre elas. Coloquei `media query` e `overflow-x: auto` nas tabelas para o site não quebrar quando abre no celular.  
    
- **UC32 · Banco de Dados:**  
  Usei o `sqlite3` direto no arquivo `database.py` pra criar as tabelas `pacientes` e `consultas` ligadas por chave estrangeira. Fiz o CRUD completo (criar, listar, editar e apagar) nas duas tabelas e usei `INNER JOIN` pra juntar o nome do paciente com a consulta, `WHERE` nos filtros e edições, e `ORDER BY` para listar os pacientes em ordem alfabética.  
    
- **UC33 · Programação Web / APIs:**  
  Montei o servidor em Flask no `app.py`, usando dois templates Jinja2 (`index.html` e `pacientes.html`) pra mostrar os dados do banco na tela. Além das páginas HTML, criei as rotas `/api/pacientes` e `/api/consultas` que devolvem os dados em JSON.  
    
- **UC34 · Organização do Trabalho:**  
  Deixei o código separado para não desorganizar: a parte do banco ficou no `database.py`, as rotas no `app.py`, os HTMLs na pasta `templates/` e o CSS na pasta `static/`. Também escrevi o `README.md` explicando o que o projeto faz e como rodar ele.  
    
- **UC35 · Projeto Integrador:**  
  Pra conseguir colocar o site no ar no Render, eu conferi as bibliotecas no `requirements.txt` (incluindo o Flask e o Gunicorn) e criei o `Procfile` com o comando `web: gunicorn app:app` para o servidor conseguir iniciar o projeto online.

---

## 5\. Reflexão Final

Fazendo esse trabalho de recuperação eu percebi que quando a gente planeja o banco de dados e as rotas antes de sair escrevendo código, tudo flui bem mais fácil e dá menos erro no meio do caminho. Se eu pudesse voltar no começo do ano, teria tirado mais dúvidas na hora das aulas de banco de dados e praticado mais SQL em casa pra não acumular matéria. Sobre TI e saúde, eu acho que as duas áreas combinam muito porque a tecnologia ajuda a evitar erros de anotação, agiliza o atendimento e deixa quem trabalha na clínica com mais tempo para cuidar das pessoas de verdade.  
