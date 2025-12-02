from api.persistence.repositories.moeda_repository import MoedaRepository
from api.models.carteira_models import Moeda

class MoedaService:
    def __init__(self, moeda_repo: MoedaRepository):
        self.moeda_repo = moeda_repo

    def buscar_por_id(self, id_moeda: int) -> Moeda:
        row = self.moeda_repo.buscar_por_id(id_moeda)

        if not row:
            raise ValueError("Moeda não encontrada")

        return Moeda(
            id_moeda=row["id_moeda"],
            codigo=row["codigo"],
            nome=row["nome"],
            tipo=row["tipo"],
        )