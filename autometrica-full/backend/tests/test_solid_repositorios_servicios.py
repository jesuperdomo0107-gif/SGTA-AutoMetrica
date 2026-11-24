"""
Pruebas Unitarias para SOLID (S y D).
"""
import pytest
from fastapi import HTTPException
from app.repositories.ordenes_repo import OrdenesRepository
from app.services.ordenes_service import OrdenesService
from app.schemas import OrdenServicioCreate


def test_servicio_crear_orden_estado_invalido(db_session):
    repo = OrdenesRepository(db_session)
    servicio = OrdenesService(repo)
    orden_data = OrdenServicioCreate(
        taller_id=1, vehiculo_id=1, cliente_id=1,
        numero_orden="ORD-TEST-001", estado="EstadoInvalido", motivo_ingreso="Test"
    )
    with pytest.raises(HTTPException) as exc_info:
        servicio.crear_orden(orden_data)
    assert exc_info.value.status_code == 422


def test_servicio_buscar_orden_inexistente(db_session):
    repo = OrdenesRepository(db_session)
    servicio = OrdenesService(repo)
    with pytest.raises(HTTPException) as exc_info:
        servicio.obtener_por_id_o_fallar(999999)
    assert exc_info.value.status_code == 404
