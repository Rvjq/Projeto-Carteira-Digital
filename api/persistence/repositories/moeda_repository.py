from typing import Dict, Any, Optional
from sqlalchemy import text

from api.persistence.db import get_connection

class MoedaRepository:

    def buscar_por_id(self, id_moeda: int) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute(
                text("""
                    SELECT id_moeda,
                           codigo,
                           nome,
                           tipo
                      FROM moeda
                     WHERE id_moeda = :id_moeda
                """),
                {"id_moeda": id_moeda},
            ).mappings().first()

        return dict(row) if row else None