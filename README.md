# URNA MAGICA

Pré-requisitos:
[Docker](https://docs.docker.com/engine/install/), [Python 3.13](https://www.python.org/downloads/), [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

## 1. Criando uma Virtual Environment

1.2. Crie uma nova Virtual Environment:

``` sh
uv venv
```

## 2. Ativando a Virtual Environment

2.1. Para ativar a Virtual Environment, digite:

Linux

``` sh
source .venv/bin/activate
```

Windows

``` sh
.\venv\Scripts\activate
```

## 3. Configurando banco de dados

3.1. Em `skeleton.conf` atualize as seguintes variáveis de conexão com o banco de dados:

````
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_HOST=localhost
DB_PORT=5432
DB_NAME=votup
DB_USER=postgres
DB_PASS=123456
````

3.2. Crie as tabelas no seu banco de dados, digite:

``` sh
uv run manage.py runserver
```


## Configurando serviço de image(minIO),

- Em `votup.conf` atualize as seguintes variáveis de configuração do serviço:

````
AWS_ACCESS_KEY_ID = "miniokey"
AWS_SECRET_ACCESS_KEY = "123456"
AWS_STORAGE_BUCKET_NAME = "urn-magic"
AWS_S3_ENDPOINT_URL = "http://localhost:9000" 
````
- Apos entrar na interface web do minio crie o bucket no `Create a bucket`:
- Na aba `Acess Keys` crie as chaves que estao no `votup.conf`

## Configurando serviço de pdf JASPER,

- Em produção

## Acesso do admin

- usuario `admin@gmail.com`
- senha `TwIu7an43@v1`