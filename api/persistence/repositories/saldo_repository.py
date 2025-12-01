from typing import Dict, Any, Optional, List
from sqlalchemy import text
from decimal import Decimal

from api.persistence.db import get_connection

class SaldoRepository:

    def criar_saldo(self, endereco_carteira: str, id_moeda: int ) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO saldo_carteira (endereco_carteira, id_moeda)
                    VALUES (:endereco_carteira, :id_moeda)
                """),
                {"endereco_carteira": endereco_carteira, "id_moeda": id_moeda},
            )

        return self.buscar_por_endereco_moeda(endereco_carteira, id_moeda)
    
    def atualizar_saldo(self, endereco_carteira: str, id_moeda: int, valor: Decimal) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            conn.execute(
                text("""
                    UPDATE saldo_carteira
                       SET saldo = :valor
                     WHERE endereco_carteira = :endereco
                       AND id_moeda = :id_moeda
                """),
                {"valor":valor, "endereco": endereco_carteira, "id_moeda": id_moeda},
            )   

        return self.buscar_por_endereco_moeda(endereco_carteira, id_moeda)    

    def buscar_por_endereco_moeda(self, endereco_carteira: str, id_moeda: int) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute(
                text("""
                    SELECT endereco_carteira,
                           id_moeda,
                           saldo,
                           data_atualizacao
                      FROM saldo_carteira
                     WHERE endereco_carteira = :endereco
                       AND id_moeda = :id_moeda
                """),
                {"endereco": endereco_carteira, "id_moeda": id_moeda},
            ).mappings().first()

        return dict(row) if row else None

    def buscar_por_endereco(self, endereco_carteira: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute(
                text("""
                    SELECT endereco_carteira,
                           id_moeda,
                           saldo,
                           data_atualizacao
                      FROM saldo_carteira
                     WHERE endereco_carteira = :endereco
                """),
                {"endereco": endereco_carteira},
            ).mappings().all()

        return [dict(r) for r in rows]

    def listar(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute(
                text("""
                    SELECT endereco_carteira,
                           id_moeda,
                           saldo,
                           data_atualizacao
                      FROM saldo_carteira
                """)
            ).mappings().all()

        return [dict(r) for r in rows]
