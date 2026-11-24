from fastapi import APIRouter, Depends, status
from typing import List
from app import schemas
from app.services.ordenes_service import OrdenesService
from app.dependencies import get_ordenes_service

router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


@router.get("/", response_model=List[schemas.OrdenServicioOut])
def listar_ordenes(
    filtros: schemas.FiltrosOrdenServicio = Depends(),
    service: OrdenesService = Depends(get_ordenes_service)
):
    return service.listar_ordenes(filtros)


@router.get("/numero/{numero_orden}", response_model=schemas.OrdenServicioOut)
def obtener_por_numero(numero_orden: str, service: OrdenesService = Depends(get_ordenes_service)):
    return service.obtener_por_numero_o_fallar(numero_orden)


@router.get("/{orden_id}", response_model=schemas.OrdenServicioOut)
def obtener_orden(orden_id: int, service: OrdenesService = Depends(get_ordenes_service)):
    return service.obtener_por_id_o_fallar(orden_id)


@router.post("/", response_model=schemas.OrdenServicioOut, status_code=status.HTTP_201_CREATED)
def crear_orden(data: schemas.OrdenServicioCreate, service: OrdenesService = Depends(get_ordenes_service)):
    return service.crear_orden(data)


@router.put("/{orden_id}", response_model=schemas.OrdenServicioOut)
def actualizar_orden(orden_id: int, data: schemas.OrdenServicioUpdate, service: OrdenesService = Depends(get_ordenes_service)):
    return service.actualizar_orden(orden_id, data)


@router.delete("/{orden_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(orden_id: int, service: OrdenesService = Depends(get_ordenes_service)):
    service.eliminar_orden(orden_id)
