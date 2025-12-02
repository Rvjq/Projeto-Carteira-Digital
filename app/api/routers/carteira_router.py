from fastapi import APIRouter, HTTPException, Depends
from typing import List

from api.services.carteira_service import CarteiraService
from api.services.saldo_service import SaldoService
from api.services.deposito_saque_service import DepositoSaqueService
from api.services.conversao_service import ConversaoService
from api.services.transferencia_service import TransferenciaService
from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.persistence.repositories.saldo_repository import SaldoRepository
from api.persistence.repositories.deposito_saque_repository import DepositoSaqueRepository
from api.persistence.repositories.conversao_repository import ConversaoRepository
from api.persistence.repositories.transferencia_repository import TransferenciaRepository
from api.models.carteira_models import Carteira, CarteiraCriada, Saldo, Conversao, Transferencia, DepositoSaque, SaqueRequest, DepositoRequest, ConversaoRequest, TransferenciaRequest


router = APIRouter(prefix="/carteiras", tags=["carteiras"])

def get_deposito_saque_service() -> DepositoSaqueService:
    repo = DepositoSaqueRepository()
    return DepositoSaqueService(repo)

def get_carteira_service() -> CarteiraService:
    repo = CarteiraRepository()
    return CarteiraService(repo)

def get_saldo_service() -> SaldoService:
    repo = SaldoRepository()
    return SaldoService(repo)

def get_conversao_service() -> ConversaoService:
    repo = ConversaoRepository()
    return ConversaoService(repo)

def get_transferencia_service() -> TransferenciaService:
    repo = TransferenciaRepository()
    return TransferenciaService(repo)

#14.1.1
@router.post("", response_model=CarteiraCriada, status_code=201)
def criar_carteira(
    service: CarteiraService = Depends(get_carteira_service),
)->CarteiraCriada:
    """
    Cria uma nova carteira. O body é opcional .
    Retorna endereço e chave privada (apenas nesta resposta).
    """
    try:
        return service.criar_carteira()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[Carteira])
def listar_carteiras(service: CarteiraService = Depends(get_carteira_service)):
    return service.listar()

#14.1.2
@router.get("/{endereco_carteira}", response_model=Carteira)
def buscar_carteira(
    endereco_carteira: str,
    service: CarteiraService = Depends(get_carteira_service),
):
    try:
        return service.buscar_por_endereco(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{endereco_carteira}", response_model=Carteira)
def bloquear_carteira(
    endereco_carteira: str,
    service: CarteiraService = Depends(get_carteira_service),
):
    try:
        return service.bloquear(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#14.1.3
@router.get("/{endereco_carteira}/saldos", response_model=List[Saldo])
def buscar_carteira_saldos(
    endereco_carteira: str,
    service: SaldoService = Depends(get_saldo_service),
):
    try:
        return service.buscar_carteira_saldos(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{endereco_carteira}/{id_moeda}", response_model=Saldo)
def buscar_carteira_saldo(
    endereco_carteira: str,
    id_moeda: int,
    service: SaldoService = Depends(get_saldo_service),
):
    try:
        return service.buscar_carteira_saldo(endereco_carteira, id_moeda)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#14.2.1
@router.post("/{endereco_carteira}/depositos", response_model=DepositoSaque)
def realizar_deposito(
    endereco_carteira: str,
    request: DepositoRequest,
    service: DepositoSaqueService = Depends(get_deposito_saque_service),
):
    try:
        return service.realizar_deposito(endereco_carteira, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#14.2.2
@router.post("/{endereco_carteira}/saques", response_model=DepositoSaque)
def realizar_saque(
    endereco_carteira: str,
    request: SaqueRequest,
    service: DepositoSaqueService = Depends(get_deposito_saque_service),
):
    try:
        return service.realizar_saque(endereco_carteira, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#14.3.1
@router.post("/{endereco_carteira}/conversoes", response_model=Conversao)
async def realizar_conversao(
    endereco_carteira: str,
    request: ConversaoRequest,
    service: ConversaoService = Depends(get_conversao_service),
):
    try:
        return await service.realizar_conversao(endereco_carteira, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#14.4.1
@router.post("/{endereco_carteira}/transferencias", response_model=Transferencia)
def realizar_transferencia(
    endereco_carteira: str,
    request: TransferenciaRequest,
    service: TransferenciaService = Depends(get_transferencia_service),
):
    try:
        return service.realizar_transferencia(endereco_carteira, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))