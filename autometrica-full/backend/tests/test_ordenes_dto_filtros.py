"""
Pruebas Unitarias para DTO de Filtros y validaciones en Ordenes.
"""
import pytest
from fastapi import HTTPException
from app.schemas import FiltrosOrdenServicio
from app.controllers.ordenes_ctrl import _validar_calificacion


def test_filtros_orden_servicio_valores_por_defecto():
    dto = FiltrosOrdenServicio()
    assert dto.skip == 0
    assert dto.limit == 100
    assert dto.taller_id is None
    assert dto.estado is None


def test_filtros_orden_servicio_con_parametros():
    dto = FiltrosOrdenServicio(skip=10, limit=25, taller_id=1, estado="En Diagnóstico")
    assert dto.skip == 10
    assert dto.limit == 25
    assert dto.taller_id == 1
    assert dto.estado == "En Diagnóstico"


def test_validacion_calificacion_rango_valido():
    _validar_calificacion(1)
    _validar_calificacion(5)
    _validar_calificacion(None)


def test_validacion_calificacion_rango_invalido():
    with pytest.raises(HTTPException) as exc_info:
        _validar_calificacion(0)
    assert exc_info.value.status_code == 400

    with pytest.raises(HTTPException) as exc_info2:
        _validar_calificacion(6)
    assert exc_info2.value.status_code == 400


def test_api_endpoint_ordenes_con_dto(client):
    response = client.get("/api/v1/ordenes/?skip=0&limit=5&estado=Recibido")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
