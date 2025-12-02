from decimal import Decimal
from typing import List

from api.persistence.repositories.saldo_repository import SaldoRepository
from api.models.carteira_models import Saldo


class SaldoService:
    def __init__(self, saldo_repo: SaldoRepository):
        self.saldo_repo = saldo_repo

    def criar_saldo(self, endereco_carteira: str, id_moeda: int) -> Saldo:
        row = self.saldo_repo.criar_saldo(endereco_carteira, id_moeda)

        if not row:
            raise ValueError("Erro durante criação de saldo")

        return Saldo(
                endereco_carteira=row["endereco_carteira"],
                id_moeda=row["id_moeda"],
                saldo=row["saldo"],
                data_atualizacao=row["data_atualizacao"],
            )

    def atualizar_saldo(self, endereco_carteira: str, id_moeda: int, valor: Decimal) -> Saldo:
        row = self.saldo_repo.atualizar_saldo(endereco_carteira, id_moeda, valor)

        if not row:
            raise ValueError("Erro durante atualização de saldo")

        return Saldo(
                endereco_carteira=row["endereco_carteira"],
                id_moeda=row["id_moeda"],
                saldo=row["saldo"],
                data_atualizacao=row["data_atualizacao"],
            )
    
    def buscar_carteira_saldo(self, endereco_carteira: str, id_moeda: int) -> Saldo:
        row = self.saldo_repo.buscar_por_endereco_moeda(endereco_carteira, id_moeda)

        if not row:
            raise ValueError("Esta Carteira não possui saldo para esta moeda")

        return Saldo(
                endereco_carteira=row["endereco_carteira"],
                id_moeda=row["id_moeda"],
                saldo=row["saldo"],
                data_atualizacao=row["data_atualizacao"],
            )


    def buscar_carteira_saldos(self, endereco_carteira: str) -> List[Saldo]:
        rows = self.saldo_repo.buscar_por_endereco(endereco_carteira)

        if not rows:
            raise ValueError("Esta Carteira não possui saldo")
        
        return [
            Saldo(
                endereco_carteira=r["endereco_carteira"],
                id_moeda=r["id_moeda"],
                saldo=r["saldo"],
                data_atualizacao=r["data_atualizacao"],
            )
            for r in rows
        ]