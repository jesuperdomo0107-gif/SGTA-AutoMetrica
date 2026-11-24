"""
Repositorio de Órdenes de Servicio para AutoMétrica.
Aplica SOLID (S): Esta capa es la ÚNICA responsable de ejecutar consultas SQL con SQLAlchemy.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas


class OrdenesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, filtros: schemas.FiltrosOrdenServicio) -> List[models.OrdenServicio]:
        q = self.db.query(models.OrdenServicio)
        if filtros.taller_id is not None:
            q = q.filter(models.OrdenServicio.taller_id == filtros.taller_id)
        if filtros.estado is not None:
            q = q.filter(models.OrdenServicio.estado == filtros.estado)
        if filtros.es_urgente is not None:
            q = q.filter(models.OrdenServicio.es_urgente == filtros.es_urgente)
        if filtros.cliente_id is not None:
            q = q.filter(models.OrdenServicio.cliente_id == filtros.cliente_id)
        if filtros.mecanico_id is not None:
            q = q.filter(models.OrdenServicio.mecanico_id == filtros.mecanico_id)
        return q.order_by(models.OrdenServicio.fecha_ingreso.desc()).offset(filtros.skip).limit(filtros.limit).all()

    def get_by_id(self, orden_id: int) -> Optional[models.OrdenServicio]:
        return self.db.query(models.OrdenServicio).filter(models.OrdenServicio.id == orden_id).first()

    def get_by_numero(self, numero: str) -> Optional[models.OrdenServicio]:
        return self.db.query(models.OrdenServicio).filter(models.OrdenServicio.numero_orden == numero).first()

    def create(self, data: schemas.OrdenServicioCreate) -> models.OrdenServicio:
        orden = models.OrdenServicio(**data.model_dump())
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def update(self, orden: models.OrdenServicio, cambios: dict) -> models.OrdenServicio:
        for campo, valor in cambios.items():
            setattr(orden, campo, valor)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def delete(self, orden: models.OrdenServicio) -> None:
        self.db.delete(orden)
        self.db.commit()
