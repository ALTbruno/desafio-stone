# Documentação API
Esta documentação tem por finalidade auxiliar e facilitar a usabilidade da API.

### Endpoint
O endpoint de conexão com a API é: http://127.0.0.1:8000/ 

### Recursos disponíveis
Atualmente existem os seguintes recursos abaixo que você pode manipular através dos métodos GET, POST:
* Cliente
* Conta

### Tratamento de dados
Todos os dados enviados e recebidos pela API estão/deverão ser em formato JSON (application/json).

## Cliente
Este módulo é responsável por administrar os clientes do banco.

### GET: Listar Clientes
* Listar todos os clientes: ```http://127.0.0.1:8000/clientes```

Retorno: Uma lista com os clientes cadastrados \
HTTP Status: 200 OK
```json
[
    {
        "id": 1,
        "nome": "Letícia",
        "sobrenome": "Sousa",
        "data_nascimento": "1980-10-13",
        "cpf": "11222222222",
        "email": "leticia@mail.com",
        "senha": "12345678"
    },
    {
        "id": 10,
        "nome": "Marcos",
        "sobrenome": "Silva",
        "data_nascimento": "2001-09-03",
        "cpf": "12345678974",
        "email": "marcos@mail.com",
        "senha": "kmsdlksklf"
    }
]
```

* Listar cliente único por ID: ```http://127.0.0.1:8000/clientes/{id_cliente}```

Retorno: Um objeto com dados do cliente \
HTTP Status: 200 OK
```json
{
    "id": 1,
    "nome": "Letícia",
    "sobrenome": "Sousa",
    "data_nascimento": "1980-10-13",
    "cpf": "11222222222",
    "email": "leticia@mail.com",
    "senha": "12345678"
}
```

### POST: Cadastrar cliente
 ```http://127.0.0.1:8000/clientes```

Parâmetro								|Descrição
-|-
nome									|**Obrigatório** <br> Nome do cliente<br> VARCHAR(50)
sobrenome								|**Obrigatório** <br> Sobrenome do cliente<br> VARCHAR(150)
data_nascimento							|**Obrigatório** <br> Data de nascimento <br> DATE(aaaa-MM-dd)
cpf										|**Obrigatório**  <br> Formato: 00000000000 <br> VARCHAR(11)
email									|**Obrigatório**  <br> E-mail válido <br> VARCHAR(255)
senha									|**Obrigatório**  <br> No mínimo 8 caracteres <br> VARCHAR(255)

Exemplo de preenchimento do payload com envio dos dados do usuário:
```json
{
    "nome": "Fulano",
    "sobrenome": "da Silva",
    "data_nascimento": "2004-07-17",
    "cpf": "12345678974",
    "email": "email_valido@dominio.com",
    "senha": "fgvkFd41"
}
```

Retorno: Cliente cadastrado com ID\
HTTP Status: 201 Created
```json
{
    "id": 124,
    "nome": "Fulano",
    "sobrenome": "da Silva",
    "data_nascimento": "2004-07-17",
    "cpf": "12345678974",
    "email": "email_valido@dominio.com",
    "senha": null
}
```

## Conta
Este módulo é responsável por administrar as contas do banco.
O número único de conta é gerado pelo módulo Cliente ao cadastrar cliente.

### GET: Listar Contas
* Listar todas as contas: ```http://127.0.0.1:8000/contas```

Retorno: Uma lista com as contas cadastradas \
HTTP Status: 200 OK
```json
[
    {
        "id": 1,
        "agencia": "0001",
        "numero": "4676439067",
        "saldo": "1653.74",
        "cliente": 1
    },
    {
        "id": 3,
        "agencia": "0001",
        "numero": "8988218630",
        "saldo": "55717.65",
        "cliente": 10
    }
]
```

* Listar conta única por id: ```http://127.0.0.1:8000/contas/{id_conta}```

Retorno: Um objeto com dados da conta \
HTTP Status: 200 OK
```json
{
    "id": 1,
    "agencia": "0001",
    "numero": "4676439067",
    "saldo": "1653.74",
    "cliente": 1
}
```

### GET: Buscar dados de uma conta específica
* Buscar saldo: ```http://127.0.0.1:8000/contas/{id_conta}/saldo```

Retorno: Um objeto com o saldo da conta \
HTTP Status: 200 OK
```json
{
    "saldo": "1653.74"
}
```

* Buscar extrato: ```http://127.0.0.1:8000/contas/{id_conta}/transacoes```

Retorno: Lista com todas as transações para o ID informado ordenadas de mais recentes para as mais antigas \
HTTP Status: 200 OK
```json
[    
    {
        "id": 7,
        "data_hora": "2022-07-17T17:11:45.308005-03:00",
        "valor": "10.00",
        "tipo": "DPST",
        "conta": 1
    },
    {
        "id": 2,
        "data_hora": "2022-07-17T16:56:40.168977-03:00",
        "valor": "27.00",
        "tipo": "TFEN",
        "conta": 1
    },
    {
        "id": 1,
        "data_hora": "2022-06-17T17:08:32.663228-03:00",
        "valor": "200.00",
        "tipo": "SQUE",
        "conta": 1
    }
]
```

* Buscar extrato por período: ```http://127.0.0.1:8000/contas/{id_conta}/transacoes?De=aaaa-MM-dd&Ate=aaaa-MM-dd```

Retorno: Lista com todas as transações do cliente dentro do intervalo informado ordenadas de mais recentes para as mais antigas \
HTTP Status: 200 OK
```json
[
    {
        "id": 1,
        "data_hora": "2022-06-17T17:08:32.663228-03:00",
        "valor": "200.00",
        "tipo": "SQUE",
        "conta": 1
    }
]
```

### POST: Efetuar transações
* Depositar: ```http://127.0.0.1:8000/contas/{id_conta}/depositar```

Parâmetro								|Descrição
-|-
valor_deposito									|**Obrigatório** <br> Valor para depósito. <br> Deve ser enviado como string. <br> Formatos: 10 ou 10.5 ou 10.50

Exemplos de preenchimento do payload para requisição de depósito:
```json
{
    "valor_deposito": "10"
}
```
```json
{
    "valor_deposito": "10.5"
}
```
```json
{
    "valor_deposito": "10.50"
}
```

Retorno: Objeto com mensagem de sucesso, saldo anterior e atual. \
HTTP Status: 200 OK
```json
{
    "mensagem": "Depósito realizado com sucesso.",
    "saldo_anterior": "1653.74",
    "saldo_atual": "1663.74"
}
```

* Sacar: ```http://127.0.0.1:8000/contas/{id_conta}/sacar```

Parâmetro								|Descrição
-|-
valor_saque									|**Obrigatório** <br> Valor para saque. <br> Deve ser enviado como string. <br> Formatos: 10 ou 10.5 ou 10.50

Exemplos de preenchimento do payload para requisição de saque:
```json
{
    "valor_saque": "10"
}
```
```json
{
    "valor_saque": "10.5"
}
```
```json
{
    "valor_saque": "10.50"
}
```

Retorno: Objeto com mensagem de sucesso, saldo anterior e atual. \
HTTP Status: 200 OK
```json
{
    "mensagem": "Saque realizado com sucesso.",
    "saldo_anterior": "1663.74",
    "saldo_atual": "1653.24"
}
```

* Transferir: ```http://127.0.0.1:8000/contas/transferir```

Parâmetro								|Descrição
-|-
conta_saida								|**Obrigatório** <br> Número da conta de onde o valor_transferencia será descontado.
conta_destino							|**Obrigatório** <br> Número da conta de onde o valor_transferencia será creditado <br> Deve ser diferente da conta_saida.
valor_transferencia						|**Obrigatório** <br> Valor para transferência. <br> Deve ser enviado como string. <br> Não deve ser superior ao saldo da conta_saida. <br> Formatos: 10 ou 10.5 ou 10.50


Exemplo de preenchimento do payload com envio dos dados para transferência:
```json
{
    "conta_saida": "4676439067",
    "conta_destino": "8988218630",
    "valor_transferencia": "10"
}
```
```json
{
    "conta_saida": "4676439067",
    "conta_destino": "8988218630",
    "valor_transferencia": "10.5"
}
```
```json
{
    "conta_saida": "4676439067",
    "conta_destino": "8988218630",
    "valor_transferencia": "10.50"
}
```

Retorno: Objeto com mensagem de sucesso \
HTTP Status: 200 OK
```json
{
    "mensagem": "Transferência realizada com sucesso."
}
```