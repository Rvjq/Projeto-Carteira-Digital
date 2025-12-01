from typing import Dict, Any
from sqlalchemy import text
from decimal import Decimal

from api.models.carteira_models import TransferenciaRequest
from api.persistence.db import get_connection

class TransferenciaRepository:

    def criar_transferencia(self, endereco_carteira: str, transferencia_request: TransferenciaRequest, taxa_valor: Decimal) -> Dict[str, Any]:
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO transferencia (endereco_origem, endereco_destino, id_moeda, valor, taxa_valor)
                    VALUES (:endereco_origem, :endereco_destino, :id_moeda, :valor, :taxa_valor)
                """),
                {"endereco_origem": endereco_carteira, "endereco_destino": transferencia_request.endereco_destino, "id_moeda": transferencia_request.id_moeda, "valor": transferencia_request.valor, "taxa_valor": taxa_valor},
            )

            row = conn.execute(
                text("""
                    SELECT id_transferencia,
                           endereco_origem,
                           endereco_destino,
                           id_moeda,
                           valor,
                           taxa_valor,
                           data_hora
                      FROM transferencia
                     WHERE endereco_origem = :endereco
                     ORDER BY data_hora DESC
                     LIMIT 1
                """),
                {"endereco": endereco_carteira},
            ).mappings().first()

        return dict(row) if row else None