import os
from decimal import Decimal

from api.services.saldo_service import SaldoService
from api.services.carteira_service import CarteiraService
from api.persistence.repositories.transferencia_repository import TransferenciaRepository
from api.persistence.repositories.saldo_repository import  SaldoRepository
from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.models.carteira_models import Transferencia, TransferenciaRequest

class TransferenciaService:
    def __init__(self, transferencia_repo: TransferenciaRepository):
        self.transferencia_repo = transferencia_repo
        self.auth_service = CarteiraService(CarteiraRepository())
        self.saldo_service = SaldoService(SaldoRepository())

    
    def realizar_transferencia(self, endereco_carteira: str, request: TransferenciaRequest) -> Transferencia:
        if not self.auth_service.carteira_auth(endereco_carteira,request.hash_privada):
            raise ValueError("Chave privada incorreta")
        
        try:
            saldo_origem = self.saldo_service.buscar_carteira_saldo(endereco_carteira, request.id_moeda)
        except ValueError:
            raise ValueError("Não existe saldo para essa moeda nesta carteira")
        
        if saldo_origem.saldo < request.valor:
            raise ValueError("Saldo insuficiente para transferencia")

        taxa:Decimal = Decimal(os.getenv("TAXA_TRANSFERENCIA_PERCENTUAL"))
        taxa_valor = request.valor * taxa

        try:
            saldo_destino = self.saldo_service.buscar_carteira_saldo(request.endereco_destino, request.id_moeda)
        except ValueError:
            saldo_destino = self.saldo_service.criar_saldo(request.endereco_destino, request.id_moeda)

        self.saldo_service.atualizar_saldo(endereco_carteira, request.id_moeda, saldo_origem.saldo - request.valor)
        self.saldo_service.atualizar_saldo(request.endereco_destino, request.id_moeda, saldo_destino.saldo + request.valor - taxa_valor)

        row = self.transferencia_repo.criar_transferencia(endereco_carteira, request, taxa_valor)
        return Transferencia(
            id_transferencia=row["id_transferencia"],
            endereco_origem=row["endereco_origem"],
            endereco_destino=row["endereco_destino"],
            id_moeda=row["id_moeda"],
            valor=row["valor"],
            taxa_valor=row["taxa_valor"],
            data_hora=row["data_hora"],
        )

