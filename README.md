# Acelera Concurso API
API REST responsável pela camada de persistência de dados do sistema Acelera Concurso.

## Tabela de Conteúdos
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Sobre as Rotas](#sobre-as-rotas)
3. [Como Funcionar?](#como-funcionar)
4. [Pré-requisitos](#pré-requisitos)
5. [Configuração Local](#configuração-local)
6. [Clone o Repositório](#clone-o-repositório)
7. [Ambiente Virtual e Dependências](#ambiente-virtual-e-dependências)
8. [Variáveis de Ambiente](#variáveis-de-ambiente)
9. [Executando as Migrações](#executando-as-migrações)
10. [Scripts Utilitários](#scripts-utilitários)
11. [Segurança e Autenticação](#segurança-e-autenticação)
    1. [Autenticação de Rotas](#autenticação-de-rotas)
12. [Variáveis de Ambiente de Segurança](#variáveis-de-ambiente-de-segurança)

## Sobre o Projeto
Esta API gerencia todas as operações de banco de dados para a plataforma Acelera Concurso. Construída em Python, utiliza PostgreSQL como sistema de gerenciamento de banco de dados e Alembic para o versionamento das migrações de schema.

O projeto foi desenvolvido utilizando Python 3.12.0. Para garantir a compatibilidade e evitar problemas, recomendamos o uso do [PyEnv](https://github.com/pyenv/pyenv) para gerenciar a versão do Python.

O fluxo envolve o registro no banco de dados e a busca via essa interface de contrato de aplicação. É possível cadastrar:
1. Usuário
2. Concurso;
3. Disciplina;
   1. Nota de Disciplina;
4. Assunto;
   1. Nota de Assunto;

Essas funções descritas acima são as principais e elas são "excluídas" via o procedimento denominado **soft-delete** onde os dados são desativados via uma variável de
valor booleano chamada `delete` dentro do modelo da base de dados.

Para poder **Finalizar** Disciplina, Assunto e suas respectivas Notas é preciso obter o **Minimo de 75%** nas resoluções de questões geradas por IA, e não possuir Nota
que não esteja finalizada para o determinado objeto.

Informo que para poder FINALIZAR UMA DISCIPLINA, **não poderá exister Assunto ou Nota de Assunto não finalizado**.

Também é possível salvar:
* **Pomodoro**: é possível salvar uma configuração de pomodoro vinculando ao usuário;
* **Dica de Estudo**: ligação via chave estrangeira com o usuário;
* **Desempenho Resolvendo Questões**: registro de log.

Envolvendo o uso de Inteligência Artificial, integração deve ser feita via front-end.

Com todos esses recursos é possível planejar os estudos de forma mais eficaz.

**Esse projeto faz parte do meu TCC: [abelbarreto-dev](https://github.com/abelbarreto-dev).**

## Sobre as Rotas
Nesse projeto existe também uma documentação específica para lidar com as rotas, se você quiser conferir os modulos, entre no pacote [routes](src/routes).

Para maiores detalhes, acesse O [Mapa das Rotas](/docs/ROUTES_MAP.md)!

Acesso o Indice [Aqui](/docs/ROUTES_MAP.md#tabela-de-conteúdo).

## Como Funcionar?
Considere todos os capítulos de configuração dessa aplicação antes de tentar fazer funcionar essa API para testes. Se tudo correr bem, você pode executar localmente sem problemas.

Ver: [Clone o Repositório](#clone-o-repositório), [Pré Requisítos](#pré-requisitos),
[Configuração Local](#configuração-local), [Ambiente Virtual e Dependencias](#ambiente-virtual-e-dependências),
[Variáveis de Ambiente](#variáveis-de-ambiente), [Variáveis de Ambiente e Segurança](#variáveis-de-ambiente-de-segurança) e
[Executando as Migrações](#executando-as-migrações).

**AGORA, execute o Módulo: [RenameCorsFile](rename_cors_file.py).**
```commandline
python rename_cors_file.py
```

**SOMENTE APÓS TUDO ISSO, VOCÊ PODERÁ FAZER FUNCIONAR SEM PROBLEMAS!**

[Ver o Módulo](app.py)

Se precisar alterar o cors, altere a lista.

Em Modo Desenvolvimento (Debugger)
```commandline
fastapi dev app.py
``` 
Em Modo Local (Sem Debugger)
```commandline
fastapi run app.py
``` 
Pelo Script
```
python app.py
```

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
```commandline
git clone https://github.com/seu-usuario/acelera-concurso-api.git
```
Ou opção via SSH:
```
git clone git@github.com:bcarsoftware/acelera_concurso_api.git
```
Ou [GitHubCLI](https://cli.github.com/):
```commandline
gh repo clone bcarsoftware/acelera_concurso_api
```
Depois, acesse o diretório:
```commandline
cd acelera-concurso-api
```

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

Banco de Dados: Crie um banco de dados no [PostgreSQL](https://www.postgresql.org/) (sugestão: db_acelera_concurso). Em seguida, edite a variável `DB_URL` no arquivo .env, substituindo os valores dentro das chaves {} **(como {user}, {password}, {host}, {port} e {db_name})**
pelas suas credenciais e informações do banco de dados. Existem também variáveis de ambientes que se refere à quantidade de pontos do estudante que utiliza o sistema. Elas são:
`SUBJECT_POINTS`; `TOPICS_POINTS` e `NOTE_POINTS`. As *Variáveis de Ambiente* são carregadas no módulo: [Constraints](/src/core/constraints.py).

| Variável         | Descrição                        | Exemplo                   |
|------------------|----------------------------------|---------------------------|
| `DB_URL`         | Url do Banco de Dados.           | postgresql+psycopg2://... |
| `SUBJECT_POINTS` | Pontos de Disciplina Finalizada. | 45 (Valor Número Inteiro) |
| `TOPIC_POINTS`   | Pontos de Assunto Finalizada.    | 15 (Valor Número Inteiro) |
| `NOTE_POINTS`    | Pontos de Nota Finalizada        | 5 (Valor Número Inteiro)  |

**Considere os exemplos de tipo de dados para evitar erros.**

**Segurança:** Configure as variáveis de segurança conforme detalhado na seção [Segurança e Autenticação](#segurança-e-autenticação). 

## Executando as Migrações
As migrações do banco de dados são gerenciadas pelo Alembic. Para facilitar o processo, utilize o script auxiliar [migrate.py](migrate.py). Execute-o e siga as instruções para aplicar as migrações e criar o schema inicial na sua base de dados.

**OBSERVAÇÃO:** Crie um banco de dados no seu postgres e insira o nome desse banco na variável `DB_URL`, no arquivo `.env` já renomeado. Eu sugiro: **`db_acelera_concurso`** com nome do banco de dados.

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
As seguintes variáveis no arquivo `.env` precisam ser configuradas:

| Variável                     | Descrição                                                                                                                          |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `ALGORITHM`                  | Algoritmo usado para gerar os tokens JWT (ex: HS265).                                                                              |
| `EMAIL_PASSWORD`             | A senha de aplicativo de 16 caracteres gerada na sua conta Google.                                                                 |
| `SECRET_KEY`                 | Chave secreta para operações criptográficas. Utilize o script [gen_secret_key.py](gen_secret_key.py) para gerar um valor seguro.   |
| `ADMIN_SECRET_KEY`           | Chave secreta para operações de administrador. Utilize o script [gen_secret_key.py](gen_secret_key.py) para gerar um valor seguro. |                                                                        
| `EMAIL_ADDRESS`              | Seu endereço de e-mail do Gmail para os testes.                                                                                    |
| `EXPIRE_CODE_TIME`           | Tempo de expiração (em minutos) para o código de verificação enviado por e-mail.                                                   |
| `EXPIRE_SESSION_TIME`        | Tempo de expiração (em minutos) para o token de sessão JWT, definindo a duração do login do usuário.                               |
| `EXPIRE_TOKEN_SESSION`       | Tempo de sessão ativa do usuário no sistema, troque 0 por número positivo.                                                         |
| `EXPIRE_ADMIN_TOKEN_SESSION` | Tempo de sessão ativa do usuário administrador, troque 0 por número positivo.                                                      |

**NOTA: recomendo fortemente a configuração da variável `DB_URL` [ver mais](#variáveis-de-ambiente).**

*That's All Folks!*
