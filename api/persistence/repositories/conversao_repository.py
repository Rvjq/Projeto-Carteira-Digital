from typing import Dict, Any
from sqlalchemy import text
from decimal import Decimal

from api.models.carteira_models import ConversaoRequest
from api.persistence.db import get_connection

class ConversaoRepository:

    def criar_conversao(self, endereco_carteira: str, conversao_request: ConversaoRequest, valor_destino: Decimal, taxa_percentual: Decimal, taxa_valor: Decimal, cotacao_utilizada: Decimal) -> Dict[str, Any]:
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO conversao (endereco_carteira, id_moeda_origem, id_moeda_destino, valor_origem, valor_destino, taxa_percentual, taxa_valor, cotacao_utilizada)
                    VALUES (:endereco_carteira, :id_moeda_origem, :id_moeda_destino, :valor_origem, :valor_destino, :taxa_percentual, :taxa_valor, :cotacao_utilizada)
                """),
                {"endereco_carteira": endereco_carteira, "id_moeda_origem": conversao_request.id_moeda_origem, "id_moeda_destino": conversao_request.id_moeda_destino, "valor_origem": conversao_request.valor_origem, "valor_destino": valor_destino, "taxa_percentual": taxa_percentual, "taxa_valor": taxa_valor, "cotacao_utilizada": cotacao_utilizada},
            )

            row = conn.execute(
                text("""
                    SELECT id_conversao,
                           endereco_carteira, 
                           id_moeda_origem, 
                           id_moeda_destino, 
                           valor_origem, 
                           valor_destino, 
                           taxa_percentual, 
                           taxa_valor, 
                           cotacao_utilizada,
                           data_hora
                      FROM conversao
                     WHERE endereco_carteira = :endereco
                     ORDER BY data_hora DESC
                     LIMIT 1
                """),
                {"endereco": endereco_carteira},
            ).mappings().first()

        return dict(row) if row else None