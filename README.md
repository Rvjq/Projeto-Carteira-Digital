# 📘 Wallet API – Guia de Instalação e Execução
Neste projeto foi o desenvolvido o mockup de uma API de Carteira Digital para disciplina Banco de Dados
seguindo os seguintes requisitos traçados pelo professor (https://drive.google.com/file/d/1bMj44ZDyxZ14uF3M17RNApwbZPZME0AW/view?usp=sharing).
Apos a api ter sido desenvolvida conforme as especificações, ela é o banco de dados foram conteinerizados
em forma de docker-compose.yaml como foi pedido pelo professor da disciplina Infraestrutura de software.

Ferramentas usadas:

- **FastAPI**
- **MySQL**
- **SQLAlchemy (Core, sem ORM)**
- **SQL puro para DDL/DML**
- Integração com API pública da **Coinbase** para conversão de moedas

A carteira permite:

- Criar carteiras (com chave pública e chave privada)
- Ver saldos por moeda (BTC, ETH, SOL, USD)
- Fazer **depósitos**
- Fazer **saques** (com taxa e validação da chave privada)
- Fazer **conversão entre moedas** (usando cotação da Coinbase)
- Fazer **transferência entre carteiras**
Este documento descreve o passo a passo para instalar, configurar e executar o projeto Wallet API utilizando MySQL, FastAPI e UV.

## 🚀 Executando a aplicação com Docker Compose

Este projeto pode ser executado facilmente utilizando **Docker** e **Docker Compose**, incluindo o banco de dados MySQL e a API Wallet.

### 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

Execute:
docker-compose build
docker-compose up -d

O servidor iniciará em:

http://127.0.0.1:8000  
http://127.0.0.1:8000/docs

## 🚀 Executando a aplicação manualmente sem Docker Compose

## 🚀 1. Pré-requisitos

Certifique-se de ter instalado:

- Git
- MySQL Server 8.0+

### 🛠️ 2. Instalar MySQL Server

Baixe o MySQL 8.0+:

https://dev.mysql.com/downloads/mysql/8.0.html

Após instalar, adicione o MySQL ao PATH:

setx PATH "%PATH%;\"C:\Program Files\MySQL\MySQL Server 8.4\bin\""

Ajuste o caminho caso sua instalação seja diferente.

### 🐍 3. Instalar o UV (gerenciador de pacotes Python)

Execute no PowerShell:

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

### 📦 4. Clonar o Repositório

git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>

### ⚙️ 5. Configurar Variáveis de Ambiente

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

ROOT_USER=root  
ROOT_PASSWORD=root  
MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.4\bin

### 🗄️ 6. Executar Migrações do Banco

Execute:

uv run migration.py

Se tudo estiver correto, o banco wallet_homolog será criado.

### ▶️ 7. Rodar o Servidor FastAPI

Execute:

uv run uvicorn api.main:app --reload

O servidor iniciará em:

http://127.0.0.1:8000  
http://127.0.0.1:8000/docs

## 📁 8. Estrutura do Projeto

api/  
 ├── main.py  
 ├── services/  
 ├── models/  
 ├── persistence/  
 ├── routers/  
migration.py  
.env  
README.md
