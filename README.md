# Acelera Concurso API
API RESTful responsável pela camada de persistência de dados do sistema Acelera Concurso.

## Tabela de Conteúdos
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração Local](#configuração-local)
4. [Clone o Repositório](#clone-o-repositório)
5. [Ambiente Virtual e Dependências](#ambiente-virtual-e-dependências)
6. [Variáveis de Ambiente](#variáveis-de-ambiente)
7. [Executando as Migrações](#executando-as-migrações)
8. [Scripts Utilitários](#scripts-utilitários)
9. [Segurança e Autenticação](#segurança-e-autenticação)
   1. [Autenticação de Rotas](#autenticação-de-rotas)
10. [Variáveis de Ambiente de Segurança](#variáveis-de-ambiente-de-segurança)
11. [TODO](#todo)

## Sobre o Projeto
Esta API gerencia todas as operações de banco de dados para a plataforma Acelera Concurso. Construída em Python, utiliza PostgreSQL como sistema de gerenciamento de banco de dados e Alembic para o versionamento das migrações de schema.

O projeto foi desenvolvido utilizando Python 3.12.0. Para garantir a compatibilidade e evitar problemas, recomendamos o uso do [PyEnv](https://github.com/pyenv/pyenv) para gerenciar a versão do Python.

## Pré-requisitos
Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:

* Python 3.12+ 
* PostgreSQL 
* Git

## Configuração Local
Para executar o projeto localmente, siga os passos abaixo em ordem.
1. [Clone o Repositório](#clone-o-repositório)
2. [Ambiente Virtual e Dependências](#ambiente-virtual-e-dependências)
3. [Variáveis de Ambiente](#variáveis-de-ambiente)
4. [Executando as Migrações](#executando-as-migrações)
5. [Segurança e Autenticação](#segurança-e-autenticação)

## Clone o Repositório
git clone https://github.com/seu-usuario/acelera-concurso-api.git
cd acelera-concurso-api 

## Ambiente Virtual e Dependências
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

**Crie o ambiente virtual**
```commandline
python -m venv .venv
```

**Ative o ambiente (Linux/macOS)**
```commandline
source .venv/bin/activate
```

**Ative o ambiente (Windows)**
```
.\.venv\Scripts\activate
```

Com o ambiente ativado, instale as dependências listadas no arquivo requirements.txt.

```commandline
pip install -r requirements.txt
```

## Variáveis de Ambiente
O projeto utiliza um arquivo .env para carregar as configurações sensíveis. Um arquivo de exemplo foi disponibilizado em .env.example.

Crie uma cópia do arquivo de exemplo:

```commandline
cp .env.example .env
```

Abra o arquivo `.env` e configure as variáveis:

Banco de Dados: Crie um banco de dados no PostgreSQL (sugestão: db_acelera_concurso). Em seguida, edite a variável `DB_URL` no arquivo .env, substituindo os valores dentro das chaves {} **(como {user}, {password}, {host}, {port} e {db_name})**
pelas suas credenciais e informações do banco de dados.

**Segurança:** Configure as variáveis de segurança conforme detalhado na seção [Segurança e Autenticação](#segurança-e-autenticação). 

## Executando as Migrações
As migrações do banco de dados são gerenciadas pelo Alembic. Para facilitar o processo, utilize o script auxiliar [migrate.py](migrate.py). Execute-o e siga as instruções para aplicar as migrações e criar o schema inicial na sua base de dados.

```commandline
python migrate.py
```
Você pode mudar o head, criar uma migration ou aplicar no seu banco de dados.

## Scripts Utilitários
O projeto conta com alguns scripts para auxiliar em tarefas comuns:

> [gen_secret_key.py](gen_secret_key.py): Gera uma chave secreta (SECRET_KEY) segura para a aplicação e a copia para sua área de transferência. 
>
> * **Dependência:** Requer OpenSSL instalado no sistema. Para mais informações, veja o repositório do [OpenSSL](https://github.com/openssl/openssl). 
>
> * **Dependência Python:** Utiliza a biblioteca [pyperclip](https://github.com/asweigart/pyperclip). Em sistemas baseados em Debian/Ubuntu, pode ser necessário instalar o xclip:
> 
> ```commandline
> sudo apt install xclip
> ```
> Cole o valor gerado no arquivo env, na variável `SECRET_KEY`.

> [gitter.py](gitter.py): Script auxiliar com funções para automatizar tarefas comuns do GIT.

> [migrate.py](migrate.py): Interface de linha de comando para gerenciar as migrações do banco de dados com Alembic.

## Segurança e Autenticação
> **Criptografia de Senhas:**
A aplicação utiliza a biblioteca bcrypt para gerar o hash de senhas, garantindo que as credenciais dos usuários sejam armazenadas de forma segura.

> **Verificação de E-mail:**
Existe um mecanismo para envio de códigos de verificação por e-mail, essencial para a confirmação de contas de novos usuários. O código-fonte desta funcionalidade pode ser encontrado em ActiveEmailUtil.

Para testar o envio de e-mails, você precisará de uma conta Google com a verificação em duas etapas ativada e uma Senha de Aplicativo gerada. Para mais detalhes, consulte a [Ajuda do Google](https://support.google.com/mail/answer/185833?hl=pt-BR).

Para que funcione nesse projeto, garanta que as [variáveis de ambiente e segurança](#variáveis-de-ambiente-de-segurança) estejam devidamente configuradas.

**NOTA: A funcionalidade de envio de e-mail foi testada apenas com o Gmail.**

### Autenticação de Rotas
Utilizo autenticação via [**JWT**](https://github.com/jpadilla/pyjwt) em conjunto com uma fabrica de tokens: [token_factory](src/core/token_factory.py), com o auxílio de um *wrapper* que retira o token do cabeçalho (header) da requisição.
Se quiser conferir a lógica, acesse o arquivo [authentication](src/core/authentication.py), essa função é utilizada com
um decorator em todas as rotas que forem necessárias, você vai encontrar em alguns módulos do pacote [src/routes](src/routes).

## Variáveis de Ambiente de Segurança
As seguintes variáveis no arquivo .env precisam ser configuradas:

| Variável               | Descrição                                                                                                                    |
|------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `ALGORITHM`            | Algoritmo usado para gerar os tokens JWT (ex: HS265).                                                                        |
| `EMAIL_PASSWORD`       | A senha de aplicativo de 16 caracteres gerada na sua conta Google.                                                           |
| `SECRET_KEY`           | Chave secreta para operações criptográficas. Use o script [gen_secret_key.py](gen_secret_key.py) para gerar um valor seguro. |
| `EMAIL_ADDRESS`        | Seu endereço de e-mail do Gmail para os testes.                                                                              |
| `EXPIRE_CODE_TIME`     | Tempo de expiração (em minutos) para o código de verificação enviado por e-mail.                                             |
|  `EXPIRE_SESSION_TIME` | Tempo de expiração (em minutos) para o token de sessão JWT, definindo a duração do login do usuário.                         |
| `EXPIRE_TOKEN_SESSION` | Tempo de sessão ativa do usuário no sistema, troque 0 por número positivo.                                                   |

**NOTA: recomendo fortemente a configuração da variável `DB_URL` [ver mais](#variáveis-de-ambiente).**

## TODO
Construir o restante!