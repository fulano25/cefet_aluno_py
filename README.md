# cefet_aluno_py

Um wrapper em python para o Portal do Aluno do CEFET/RJ.

cefet_aluno_py é uma api criada incialmente para fazer a integração entre a grade do aluno do Cefet e o Google agenda. Porém há outras possibilidades, como automatizar o download dos relatórios disponíveis no site e a obter a grade de horários em formatos de dados mais amigáveis para edição.

Por enquanto está em fase de prova de conceito, mas você já pode utilizar o main script para importar sua grade para o google agenda.

É necessário clonar este repositório, e instalar as dependências necessárias na sua instalação do python.

```bash
git clone https://github.com/saulodias/cefet_aluno_py.git
```

```bash
pip install -r requirements.txt
```

Renomeie o arquivo private.py.example para private.py e coloque seu `login` e `senha` nos campos indicados.

Você também vai precisar de um arquivo de credenciais da api do Google. `credentials.json`

Salve na pasta raiz.

https://developers.google.com/calendar/quickstart/go

A API do Google inicia um servidor na porta 8080. Certifique-se que não há algum serviço utilizando esta porta antes de executar o script, ou ocorrerá um erro.
