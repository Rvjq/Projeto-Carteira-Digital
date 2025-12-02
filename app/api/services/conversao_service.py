import os
import httpx
import logging

from decimal import Decimal

from api.services.saldo_service import SaldoService
from api.services.carteira_service import CarteiraService
from api.services.moeda_service import MoedaService
from api.persistence.repositories.conversao_repository import ConversaoRepository
from api.persistence.repositories.saldo_repository import  SaldoRepository
from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.persistence.repositories.moeda_repository import MoedaRepository
from api.models.carteira_models import Conversao, ConversaoRequest, Moeda

class ConversaoService:
    def __init__(self, conversao_repo: ConversaoRepository):
        self.conversao_repo = conversao_repo
        self.auth_service = CarteiraService(CarteiraRepository())
        self.saldo_service = SaldoService(SaldoRepository())
        self.moeda_service = MoedaService(MoedaRepository())

    async def realizar_conversao(self, endereco_carteira: str, request: ConversaoRequest) -> Conversao:
        if not self.auth_service.carteira_auth(endereco_carteira,request.hash_privada):
            raise ValueError("Chave privada incorreta")

        try:
            saldo_origem = self.saldo_service.buscar_carteira_saldo(endereco_carteira, request.id_moeda_origem)
        except ValueError:
            raise ValueError("Não existe saldo para essa moeda nesta carteira")
        
        if saldo_origem.saldo < request.valor_origem:
            raise ValueError("Saldo insuficiente para conversao")

        try:
            saldo_destino = self.saldo_service.buscar_carteira_saldo(endereco_carteira, request.id_moeda_destino)
        except ValueError:
            saldo_destino = self.saldo_service.criar_saldo(endereco_carteira, request.id_moeda_destino)
        
        try:
            moeda_origem = self.moeda_service.buscar_por_id(request.id_moeda_origem).codigo
        except ValueError:
            raise ValueError("Moeda origem não existe")
        
        try:
            moeda_destino = self.moeda_service.buscar_por_id(request.id_moeda_destino).codigo
        except ValueError:
            raise ValueError("Moeda destino não existe")

        try:
            cotacao = await self.obter_cotacao_coinbase(moeda_origem, moeda_destino)
            cotacao = Decimal(str(cotacao))
        except RuntimeError as e:
            raise ValueError("Falha ao obter cotação:",e)

        taxa:Decimal = Decimal(os.getenv("TAXA_CONVERSAO_PERCENTUAL"))
        valor_destino:Decimal = request.valor_origem * cotacao
        taxa_valor:Decimal = valor_destino * taxa
        valor_destino = valor_destino - taxa_valor

        self.saldo_service.atualizar_saldo(endereco_carteira, request.id_moeda_origem, saldo_origem.saldo - request.valor_origem)
        self.saldo_service.atualizar_saldo(endereco_carteira, request.id_moeda_destino, saldo_destino.saldo + valor_destino )        

        row = self.conversao_repo.criar_conversao(endereco_carteira, request, valor_destino, taxa, taxa_valor, cotacao)
        return Conversao(
            id_conversao=row["id_conversao"],
            endereco_carteira=row["endereco_carteira"],
            id_moeda_origem=row["id_moeda_origem"],
            id_moeda_destino=row["id_moeda_destino"],
            valor_origem=row["valor_origem"],
            valor_destino=row["valor_destino"],
            taxa_percentual=row["taxa_percentual"],
            taxa_valor=row["taxa_valor"],
            cotacao_utilizada=row["cotacao_utilizada"],
            data_hora=row["data_hora"],
        )

    async def obter_cotacao_coinbase(self, moeda_origem: str, moeda_destino: str) -> float:
        url = f"https://api.coinbase.com/v2/prices/{moeda_origem}-{moeda_destino}/spot"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()

                data = response.json()

                # Valida formato do JSON
                if "data" not in data or "amount" not in data["data"]:
                    raise ValueError("Resposta inesperada da Coinbase")

                return float(data["data"]["amount"])

        except httpx.TimeoutException:
            logging.error(f"Timeout ao acessar Coinbase: {url}")
            raise RuntimeError("Serviço de cotação indisponível (timeout)")

        except httpx.RequestError as e:
            logging.error(f"Erro de rede ao consultar Coinbase: {e}")
            raise RuntimeError("Erro ao consultar serviço de cotação")

        except httpx.HTTPStatusError as e:
            logging.error(f"Coinbase retornou status {e.response.status_code}: {e}")
            raise RuntimeError("Serviço de cotação retornou erro")

        except ValueError as e:
            logging.error(f"Erro ao interpretar JSON da Coinbase: {e}")
            raise RuntimeError("Formato de resposta inválido do serviço de cotação")

        except Exception as e:
            logging.exception(f"Erro inesperado ao consultar cotação: {e}")
            raise RuntimeError("Erro inesperado ao obter cotação")