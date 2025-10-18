# Acelera Concurso API
Aqui eu vou disponibilizar a documentação para ser possível testar essa API.

Essa API é responsável pela parte de Banco de Dados do Sistema.

Esse projeto utiliza por padrão o [PostgreSQL](https://www.postgresql.org/).

Primeiro de tudo, para **FAZER FUNCIONAR,** veja a sequência de [Passos a Seguir](#passos-a-seguir).

Esse projeto foi construído a parti de uma máquina virtual Python: *.venv*. Utilizei a versão **Python 3.14.0**.
* Se você tem dúvidas, instale essa versão do Python a parti do [PyEnv](https://github.com/pyenv/pyenv).
  * Se bem sucedido, o projeto funcionará sem problemas.

Esse projeto tem um algoritmo que visa auxiliar em funções do GIT. O arquivo Python é o: [gitter.py](gitter.py)

## Passos a Seguir
Seguindo essa ordem, você conseguirá testar essa API sem maiores problemas. Ao concluir cada passo, volte para cá até finalizar.

1. Instale as [Dependencias](#dependências)
2. Verifique as [Variáveis de Ambiente](#variáveis-de-ambiente)
3. Execute as [Migrações](#sobre-migrations) | **Opção Número 2**
4. Verifique as informações descritas em [Segurança e Autenticação](#segurança-e-autenticação)

## Dependências
Para ver as dependencias do projeto, você pode acessar o arquivo: [requirements.txt](requirements.txt).

Para instalar as dependências, execute o comando abaixo no seu terminal:

```commandline
pip install -r requirements.txt
```

## Variáveis de Ambiente
Eu disponibilizei um arquivo chamado [.env.example](.env.example).

* Copie/Renomeie para **.env** e então:
  * Banco de Dados:
    * Eu sugiro a criação de um banco de dados chamado: **db_acelera_concurso**
    * Substitua os valores de credenciais para os seus.

## Sobre Migrations
Esse projeto utiliza [alembic](https://alembic.sqlalchemy.org/en/latest/) como a sua ferramenta para realizar migrations.

Esse projeto possui um programa Python, cujo objetivo é ser um auxiliar para realização de serviços de migrations na base de dados.

Execute o Script: [migrate.py](migrate.py) e siga as instruções conforme a sua necessidade.

## Segurança e Autenticação
Esse projecto utiliza os recursos disponíbilizados através da biblioteca [bcrypt](https://pypi.org/project/bcrypt/).
Ela utiliza dos recursos de hash passwords para fazer o processo de criptografia das senhas de nosso usuários.

Também existe nesse projeto um mecanismo para o envio via e-mail do código de verificação, útil para confirmação de conta.
O código-fonte dessa classe se encontra em: [ActiveEmailUtil](/src/utils/active_email_util.py). Ele se utiliza de recursos como
senha de aplicativo: [Ajuda do Google](https://support.google.com/mail/answer/185833?hl=pt-BR), você precisa gerar a sua senha
na sua conta google e colocar o seu email no arquivo de variáveis de ambiente `.env` para ter efeito, se desejas testar.
Altere as variáveis `EMAIL_ADDRESS` e `EMAIL_PASSWORD`, onde email password é a sua senha de aplicativo.

**NOTA: NÃO TESTADO PARA OUTROS PROVEDORES DE E-MAIL.**

TODO: construir o restante! 
