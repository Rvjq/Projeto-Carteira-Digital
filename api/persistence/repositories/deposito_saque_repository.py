from typing import Dict, Any, Optional
from sqlalchemy import text
from decimal import Decimal

from api.persistence.db import get_connection
from api.models.carteira_models import DepositoRequest

class DepositoSaqueRepository():

    def criar_deposito_saque(self, endereco_carteira: str, deposito_request: DepositoRequest, tipo: str, taxa_valor: Decimal) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO deposito_saque (endereco_carteira, id_moeda, tipo, valor, taxa_valor)
                    VALUES (:endereco_carteira, :id_moeda, :tipo, :valor, :taxa_valor)
                """),
                {"endereco_carteira": endereco_carteira, "id_moeda": deposito_request.id_moeda, "tipo": tipo, "valor": deposito_request.valor, "taxa_valor": taxa_valor},
            )

            row = conn.execute(
                text("""
                    SELECT id_movimento,
                           endereco_carteira,
                           id_moeda,
                           tipo,
                           valor,
                           taxa_valor,
                           data_hora
                      FROM deposito_saque
                     WHERE endereco_carteira = :endereco
                     ORDER BY data_hora DESC
                     LIMIT 1
                """),
                {"endereco": endereco_carteira},
            ).mappings().first()

        return dict(row) if row else None