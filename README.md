# 🗳️ VOTUP - Sistema de Votação Eletrônica

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2%2B-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema moderno de votação eletrônica desenvolvido com Django REST Framework, seguindo o padrão **Service Layer** para garantir alta testabilidade, manutenibilidade e flexibilidade.

## 📋 Funcionalidades

- 🔐 **Autenticação JWT** - Sistema seguro de login com tokens
- 👥 **Gerenciamento de Usuários** - Administração completa de usuários do sistema
- 🗳️ **Gestão de Eleitores** - Cadastro e validação de eleitores
- 👤 **Gestão de Candidatos** - Administração de candidatos e chapas
- 📊 **Sistema de Votação** - Processo de votação eletrônica seguro
- 📈 **Relatórios em PDF** - Geração de relatórios detalhados
- 📊 **Dashboard de Resultados** - Visualização em tempo real dos resultados
- 🔄 **Auditoria Completa** - Rastreamento de todas as ações do sistema

## 🏗️ Arquitetura

O projeto utiliza o padrão **Service Layer**, promovendo:

- 🎯 **Separação de Responsabilidades** - Regras de negócio isoladas em services
- 🧪 **Alta Testabilidade** - Funções simples facilitam testes unitários e de integração
- 🔌 **Baixo Acoplamento** - Services acessam ORM diretamente, sem abstrações intermediárias
- 📈 **Escalabilidade** - Preparado para crescimento e mudanças

```
┌─────────────────────────────────────────────────────────┐
│                    ADAPTERS (External)                  │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │   Web/REST API  │  │    Database     │             │
│  │   (ViewSets)    │  │  (Repositories) │             │
│  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                        PORTS                            │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Input Ports    │  │  Output Ports   │             │
│  │  (Use Cases)    │  │  (Interfaces)   │             │
│  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                      DOMAIN CORE                        │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │    Entities     │  │  Business Rules │             │
│  │   (Models)      │  │   (Domain)      │             │
│  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Tecnologias

- **Backend**: Django 5.2+ / Django REST Framework
- **Banco de Dados**: PostgreSQL 17
- **Autenticação**: JWT (JSON Web Tokens)
- **Storage**: MinIO (S3-compatible)
- **Relatórios**: JasperReports / FPDF
- **Documentação**: Swagger/OpenAPI 3.0
- **Containerização**: Docker & Docker Compose
- **Gerenciador de Dependências**: uv

## 📚 Documentação da API

Após executar o projeto, acesse:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

## 🚀 Instalação e Configuração

### Pré-requisitos

Certifique-se de ter instalado:

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de dependências)
- [Docker](https://docs.docker.com/engine/install/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### 1. 📥 Clone o Repositório

```bash
git clone https://github.com/seu-usuario/votup-back.git
cd votup-back
```

### 2. 🐍 Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
# Linux/macOS
source .venv/bin/activate

# Windows
.\.venv\Scripts\activate
```

### 3. 📦 Instalar Dependências

```bash
# Instalar todas as dependências
uv sync

# Ou instalar manualmente
uv pip install -r pyproject.toml
```

### 4. 🐳 Configurar Serviços com Docker

```bash
# Subir PostgreSQL e MinIO
cd compose
docker-compose up -d

# Verificar se os serviços estão rodando
docker-compose ps
```

### 5. ⚙️ Configurar Variáveis de Ambiente

Crie o arquivo `votup.conf` na raiz do projeto:

```bash
# Banco de Dados
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_HOST=localhost
DB_PORT=5432
DB_NAME=votup
DB_USER=postgres
DB_PASS=123456

# MinIO (Storage S3-compatible)
AWS_ACCESS_KEY_ID=miniovotup
AWS_SECRET_ACCESS_KEY=miniovotup
AWS_STORAGE_BUCKET_NAME=votup
AWS_S3_ENDPOINT_URL=http://localhost:9000

# JasperReports (Relatórios)
SOURCE_LOCAL=/usr/app/reports
JASPER_HOST=http://localhost:8089/jasperserver/rest_v2/reports/Reports/
JASPER_USER=votup
JASPER_PASS=123456
```

### 6. 🗃️ Configurar Banco de Dados

```bash
# Executar migrações
uv run python manage.py migrate

# Criar dados iniciais (opcional)
uv run python manage.py loaddata fixtures/initial_data.json
```

### 7. 🎯 Configurar MinIO

1. Acesse o MinIO Console: `http://localhost:9001`
2. Faça login com:
   - **Usuário**: `miniovotup`
   - **Senha**: `miniovotup`
3. Crie um bucket chamado `votup`
4. Configure as políticas de acesso como público

### 8. 🚀 Executar o Projeto

```bash
# Executar servidor de desenvolvimento
uv run python manage.py runserver

# O projeto estará disponível em:
# http://localhost:8000
```

## 🔑 Credenciais Padrão

### Administrador do Sistema
- **Email**: `admin@votup.local`
- **Senha**: `AdminVotup2024!`

### MinIO Console
- **URL**: `http://localhost:9001`
- **Usuário**: `miniovotup`
- **Senha**: `miniovotup`

### PostgreSQL
- **Host**: `localhost:5432`
- **Banco**: `votup`
- **Usuário**: `postgres`
- **Senha**: `123456`

> ⚠️ **Importante**: Altere todas as credenciais padrão em produção!

## 🧪 Testes

```bash
# Executar todos os testes
uv run pytest

# Executar testes com cobertura
uv run pytest --cov=. --cov-report=html

# Executar testes específicos
uv run pytest core/tests/test_voting.py

# Ver relatório de cobertura
open htmlcov/index.html
```

## 📊 Logs e Monitoramento

Os logs são organizados em categorias:

```bash
logs/
├── errors.log      # Erros da aplicação
├── queries.log     # Queries SQL lentas (>100ms)
└── performance.log # Métricas de performance
```

## 🐳 Docker (Produção)

```bash
# Build da imagem
docker build -t votup-api .

# Executar com docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## 📖 Estrutura do Projeto

```
votup/
├── account/               # Módulo de autenticação
│   ├── models.py         # Modelo de usuário customizado
│   ├── serializers.py    # Serializers JWT
│   └── viewset.py        # ViewSets de autenticação
├── core/                 # Módulo principal
│   ├── domain/           # Entidades de domínio
│   ├── ports/            # Interfaces (contratos)
│   ├── repositories/     # Implementações de repositórios
│   ├── use_cases/        # Casos de uso da aplicação
│   ├── dto/              # Data Transfer Objects
│   ├── models/           # Modelos Django
│   └── viewset.py        # ViewSets da API
├── compose/              # Configurações Docker
├── logs/                 # Arquivos de log
├── media/                # Arquivos de mídia
├── reports/              # Templates de relatórios
├── votup/                # Configurações Django
│   ├── settings.py       # Configurações principais
│   └── urls.py           # Roteamento principal
├── pyproject.toml        # Dependências e configurações
├── votup.conf            # Variáveis de ambiente
└── README.md             # Este arquivo
```

## 🤝 Contribuindo

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### 📝 Padrões de Código

```bash
# Formatação de código
uv run black .

# Organização de imports
uv run isort .

# Verificação de tipos
uv run mypy .

# Linting
uv run flake8 .
```

### ✅ Concluído
- [x] Arquitetura Service Layer
- [x] Migração de Arquitetura Hexagonal para Service Layer
- [x] Testes unitários para services
- [x] Sistema de autenticação JWT
- [x] CRUD completo de entidades
- [x] Documentação Swagger/OpenAPI
- [x] Sistema de logs otimizado
- [x] Geração de relatórios PDF

### 🚧 Em Desenvolvimento
- [ ] Testes unitários e de integração
- [ ] CI/CD com GitHub Actions
- [ ] WebSockets para resultados em tempo real
- [ ] API de notificações

### 🔮 Futuro
- [ ] Microserviços
- [ ] Event Sourcing
- [ ] Aplicativo mobile
- [ ] Blockchain para auditoria

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

