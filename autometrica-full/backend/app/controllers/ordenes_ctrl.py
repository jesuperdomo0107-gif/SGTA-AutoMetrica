from sqlalchemy.orm import Session
from typing import Optional, Union
from app import models, schemas, exceptions
from app.core.constants import (
    EstadoOrden,
    CALIFICACION_MINIMA,
    CALIFICACION_MAXIMA,
    PAGINACION_SKIP_DEFECTO,
    PAGINACION_LIMITE_DEFECTO,
)

estados_validos = EstadoOrden.valores()


def _validar_calificacion(calificacion: Optional[int]) -> None:
    """Valida que la calificación se encuentre dentro del rango de negocio permitido."""
    if calificacion is not None:
        if calificacion < CALIFICACION_MINIMA or calificacion > CALIFICACION_MAXIMA:
            raise exceptions.bad_request(
                f"La calificacion debe ser entre {CALIFICACION_MINIMA} y {CALIFICACION_MAXIMA}"
            )


def get_all(
    db: Session,
    filtros: Optional[schemas.FiltrosOrdenServicio] = None,
    skip: int = PAGINACION_SKIP_DEFECTO,
    limit: int = PAGINACION_LIMITE_DEFECTO,
    taller_id: Optional[int] = None,
    estado: Optional[str] = None,
    es_urgente: Optional[bool] = None,
    cliente_id: Optional[int] = None,
    mecanico_id: Optional[int] = None,
):
    """Obtiene órdenes aplicando DTO FiltrosOrdenServicio o parámetros individuales para compatibilidad."""
    if filtros is not None:
        skip = filtros.skip
        limit = filtros.limit
        taller_id = filtros.taller_id
        estado = filtros.estado
        es_urgente = filtros.es_urgente
        cliente_id = filtros.cliente_id
        mecanico_id = filtros.mecanico_id

    q = db.query(models.OrdenServicio)
    if taller_id is not None:
        q = q.filter(models.OrdenServicio.taller_id == taller_id)
    if estado is not None:
        q = q.filter(models.OrdenServicio.estado == estado)
    if es_urgente is not None:
        q = q.filter(models.OrdenServicio.es_urgente == es_urgente)
    if cliente_id is not None:
        q = q.filter(models.OrdenServicio.cliente_id == cliente_id)
    if mecanico_id is not None:
        q = q.filter(models.OrdenServicio.mecanico_id == mecanico_id)
    return q.order_by(models.OrdenServicio.fecha_ingreso.desc()).offset(skip).limit(limit).all()


def get_by_id(db: Session, orden_id: int):
    o = db.query(models.OrdenServicio).filter(models.OrdenServicio.id == orden_id).first()
    if o is None:
        raise exceptions.not_found("OrdenServicio", orden_id)
    return o


def get_by_numero(db: Session, numero: str):
    o = db.query(models.OrdenServicio).filter(models.OrdenServicio.numero_orden == numero).first()
    if o is None:
        raise exceptions.not_found("OrdenServicio numero", numero)
    return o


def create(db: Session, data: schemas.OrdenServicioCreate):
    if data.estado not in estados_validos:
        raise exceptions.valor_invalido("estado", estados_validos)
    _validar_calificacion(data.calificacion)

    numero_repetido = db.query(models.OrdenServicio).filter(
        models.OrdenServicio.numero_orden == data.numero_orden
    ).first()
    if numero_repetido:
        raise exceptions.already_exists("numero_orden", data.numero_orden)
    o = models.OrdenServicio(**data.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


def update(db: Session, orden_id: int, data: schemas.OrdenServicioUpdate):
    o = get_by_id(db, orden_id)
    cambios = data.model_dump(exclude_unset=True)
    if "estado" in cambios:
        if cambios["estado"] not in estados_validos:
            raise exceptions.valor_invalido("estado", estados_validos)
    if "calificacion" in cambios:
        _validar_calificacion(cambios["calificacion"])

    for campo in cambios:
        setattr(o, campo, cambios[campo])
    db.commit()
    db.refresh(o)
    return o


def delete(db: Session, orden_id: int):
    o = get_by_id(db, orden_id)
    db.delete(o)
    db.commit()

