import os
from decimal import Decimal

from api.services.saldo_service import SaldoService
from api.services.carteira_service import CarteiraService
from api.persistence.repositories.deposito_saque_repository import DepositoSaqueRepository
from api.persistence.repositories.saldo_repository import  SaldoRepository
from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.models.carteira_models import DepositoSaque, DepositoRequest, SaqueRequest

class DepositoSaqueService():
    def __init__(self, deposito_saque_repo: DepositoSaqueRepository):
        self.deposito_saque_repo = deposito_saque_repo
        self.saldo_service = SaldoService(SaldoRepository())
        self.auth_service = CarteiraService(CarteiraRepository())

    def criar_deposito_saque(self, endereco_carteira: str, deposito_request: DepositoRequest, tipo: str, taxa_valor: Decimal) -> DepositoSaque:
        row = self.deposito_saque_repo.criar_deposito_saque(endereco_carteira, deposito_request, tipo, taxa_valor)

        if not row:
            raise ValueError("Erro durante criação de saldo")

        return DepositoSaque(
                id_movimento=row["id_movimento"],
                endereco_carteira=row["endereco_carteira"],
                id_moeda=row["id_moeda"],
                tipo = row["tipo"],
                valor = row["valor"],
                taxa_valor = row["taxa_valor"],
                data_hora = row["data_hora"],
            )

    def realizar_deposito(self, endereco_carteira: str, deposito_request: DepositoRequest) -> DepositoSaque:
        try:
            saldo = self.saldo_service.buscar_carteira_saldo(endereco_carteira, deposito_request.id_moeda)
        except ValueError:
            saldo = self.saldo_service.criar_saldo(endereco_carteira, deposito_request.id_moeda)

        novo_valor:Decimal = saldo.saldo + deposito_request.valor

        self.saldo_service.atualizar_saldo(endereco_carteira, deposito_request.id_moeda, novo_valor)

        return self.criar_deposito_saque(endereco_carteira, deposito_request, "DEPOSITO", 0)
        
    
    def realizar_saque(self, endereco_carteira: str, saque_request: SaqueRequest) -> DepositoSaque:

        if not self.auth_service.carteira_auth(endereco_carteira,saque_request.hash_privada):
            raise ValueError("Chave privada incorreta")

        try:
            saldo = self.saldo_service.buscar_carteira_saldo(endereco_carteira, saque_request.id_moeda)
        except ValueError:
            raise ValueError("Não existe saldo para essa moeda nesta carteira")
        
        taxa:Decimal = Decimal(os.getenv("TAXA_SAQUE_PERCENTUAL"))
        taxa_valor:Decimal = saque_request.valor * taxa 

        novo_valor:Decimal =  saldo.saldo - saque_request.valor - taxa_valor

        if saldo.saldo < saque_request.valor + taxa_valor:
            raise ValueError("Saldo insuficiente para saque")

        self.saldo_service.atualizar_saldo(endereco_carteira, saque_request.id_moeda, novo_valor)

        return self.criar_deposito_saque(endereco_carteira, saque_request, "SAQUE", taxa_valor)
