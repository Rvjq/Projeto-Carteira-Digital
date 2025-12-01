📘 Wallet API – Guia de Instalação e Execução

Este documento descreve o passo a passo para instalar, configurar e executar o projeto Wallet API utilizando MySQL, FastAPI e UV.

🚀 1. Pré-requisitos

Certifique-se de ter instalado:

Git

MySQL Server 8.0+

🛠️ 2. Instalar MySQL Server

Baixe o MySQL 8.0+:

🔗 https://dev.mysql.com/downloads/mysql/8.0.html

Após instalar, adicione o MySQL ao PATH:

setx PATH "%PATH%;\"C:\Program Files\MySQL\MySQL Server 8.4\bin\""


Ajuste o caminho caso sua instalação seja diferente.

🐍 3. Instalar o UV (gerenciador de pacotes Python)

Execute no PowerShell:

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

📦 4. Clonar o Repositório
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>

⚙️ 5. Configurar Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

DB_HOST=localhost
DB_PORT=3306
DB_USER=wallet_api_homolog
DB_PASSWORD=api123
DB_NAME=wallet_homolog

TAXA_SAQUE_PERCENTUAL=0.01
TAXA_CONVERSAO_PERCENTUAL=0.02
TAXA_TRANSFERENCIA_PERCENTUAL=0.01

PRIVATE_KEY_SIZE=32
PUBLIC_KEY_SIZE=16

# Variáveis para migração
ROOT_USER=root
ROOT_PASSWORD=root
MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.4\bin

🗄️ 6. Executar Migrações do Banco

O projeto possui um script migration.py que cria o banco e as tabelas.

Execute:

uv run migration.py


Se tudo estiver correto, o banco wallet_homolog será criado.

▶️ 7. Rodar o Servidor FastAPI

Execute:

uv run uvicorn api.main:app --reload


O servidor iniciará em:

👉 http://127.0.0.1:8000

👉 Documentação Swagger: http://127.0.0.1:8000/docs


📁 8. Estrutura do Projeto
api/
 ├── main.py
 ├── services/
 ├── models/
 ├── persistence/
 ├── routers/
migration.py
.env
README.md