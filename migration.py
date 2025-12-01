# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "dotenv",
# ]
# ///

import subprocess
import os
from dotenv import load_dotenv


load_dotenv() 
MYSQL_PATH = os.getenv("MYSQL_PATH", r"C:\Program Files\MySQL\MySQL Server 8.4\bin")
MYSQL_USER = os.getenv("ROOT_USER", "root")
MYSQL_PASSWORD = os.getenv("ROOT_PASSWORD", "root")
MYSQL_HOST = os.getenv("DB_HOST", "localhost")
MYSQL_PORT = os.getenv("DB_PORT", "3306")
SQL_FILE = "sql/DDL_Carteira_Digital.sql"
os.environ["PATH"] += ";" + MYSQL_PATH

def run_migration():
    print("Executando migração...")
    print("User:",MYSQL_USER,"Password:",MYSQL_PASSWORD,"Port:",MYSQL_PORT,"Host:",MYSQL_HOST)

    command = [
        "mysql",
        f"-u{MYSQL_USER}",
        f"-p{MYSQL_PASSWORD}",
        f"-h{MYSQL_HOST}",
        f"-P{MYSQL_PORT}",
        "-e",
        f"SOURCE {SQL_FILE};"
    ]

    try:
        subprocess.run(command, check=True)
        print("Migração executada com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro ao executar migração:")
        print(e)

if __name__ == "__main__":
    run_migration()
