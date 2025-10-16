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

TODO: construir o restante! 
