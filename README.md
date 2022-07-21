# Executando a aplicação
1. Clone este repositório
```
git clone https://github.com/ALTbruno/desafio-stone
```

2. Entre na pasta
```
cd desafio-stone
```

3. Crie um arquivo .env 
```
touch .env
```

4. Abra o arquivo .env e insira os valores para as variáveis de ambiente
```
CONNECTOR=''
NAME=''
USER=''
PASSWORD=''
HOST=''
PORT=''
SECRET_KEY = ''
```

5. Crie um ambiente virtual
```
python -m venv .venv
```

6. Ative o ambiente virtual
```
source .venv/Scripts/activate
```

7. Baixe as dependências do projeto
```
pip install -r requirements.txt
```

8. Execute
```
python manage.py runserver
```

# Documentação
[Clique aqui](./DOCS.md)
