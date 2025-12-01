from typing import Literal
from datetime import  datetime
from decimal import Decimal
from pydantic import BaseModel


class Carteira(BaseModel):
    endereco_carteira: str
    data_criacao: datetime
    status: int

class CarteiraCriada(Carteira):
    chave_privada: str

class Saldo(BaseModel):
    endereco_carteira: str
    id_moeda: int
    saldo: Decimal
    data_atualizacao: datetime

class DepositoSaque(BaseModel):
    id_movimento: int
    endereco_carteira: str
    id_moeda: int
    tipo: str
    valor: Decimal
    taxa_valor: Decimal
    data_hora: datetime

class DepositoRequest(BaseModel):
    id_moeda: int
    valor: Decimal

class SaqueRequest(DepositoRequest):
    hash_privada: str

class Conversao(BaseModel):
    id_conversao: int
    endereco_carteira: str
    id_moeda_origem: int
    id_moeda_destino: int
    valor_origem: Decimal
    valor_destino: Decimal
    taxa_percentual: Decimal
    taxa_valor: Decimal
    cotacao_utilizada: Decimal
    data_hora: datetime

class ConversaoRequest(BaseModel):
    id_moeda_origem: int
    id_moeda_destino: int
    valor_origem: Decimal
    hash_privada: str

class Transferencia(BaseModel):
    id_transferencia: int
    endereco_origem: str
    endereco_destino: str
    id_moeda: int
    valor: Decimal
    taxa_valor: Decimal
    data_hora: datetime

class TransferenciaRequest(BaseModel):
    endereco_destino: str
    id_moeda: int
    valor: Decimal
    hash_privada: str

class Moeda(BaseModel):
    id_moeda: int
    codigo: str
    nome: str
    tipo: str
