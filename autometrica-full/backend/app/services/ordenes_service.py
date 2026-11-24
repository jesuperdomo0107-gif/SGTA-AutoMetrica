"""
Servicio de Órdenes de Servicio para AutoMétrica.
Aplica SOLID (S) y (D): Encapsula reglas de negocio e interactúa a través del repositorio inyectado.
"""
from typing import List, Optional
from app import models, schemas, exceptions
from app.repositories.ordenes_repo import OrdenesRepository
from app.core.constants import EstadoOrden, CALIFICACION_MINIMA, CALIFICACION_MAXIMA


class OrdenesService:
    def __init__(self, repo: OrdenesRepository):
        self.repo = repo

    def _validar_calificacion(self, calificacion: Optional[int]) -> None:
        if calificacion is not None:
            if calificacion < CALIFICACION_MINIMA or calificacion > CALIFICACION_MAXIMA:
                raise exceptions.bad_request(
                    f"La calificacion debe ser entre {CALIFICACION_MINIMA} y {CALIFICACION_MAXIMA}"
                )

    def listar_ordenes(self, filtros: schemas.FiltrosOrdenServicio) -> List[models.OrdenServicio]:
        return self.repo.get_all(filtros)

    def obtener_por_id_o_fallar(self, orden_id: int) -> models.OrdenServicio:
        orden = self.repo.get_by_id(orden_id)
        if orden is None:
            raise exceptions.not_found("OrdenServicio", orden_id)
        return orden

    def obtener_por_numero_o_fallar(self, numero: str) -> models.OrdenServicio:
        orden = self.repo.get_by_numero(numero)
        if orden is None:
            raise exceptions.not_found("OrdenServicio numero", numero)
        return orden

    def crear_orden(self, data: schemas.OrdenServicioCreate) -> models.OrdenServicio:
        if data.estado not in EstadoOrden.valores():
            raise exceptions.valor_invalido("estado", EstadoOrden.valores())
        self._validar_calificacion(data.calificacion)

        existente = self.repo.get_by_numero(data.numero_orden)
        if existente:
            raise exceptions.already_exists("numero_orden", data.numero_orden)

        return self.repo.create(data)

    def actualizar_orden(self, orden_id: int, data: schemas.OrdenServicioUpdate) -> models.OrdenServicio:
        orden = self.obtener_por_id_o_fallar(orden_id)
        cambios = data.model_dump(exclude_unset=True)

        if "estado" in cambios and cambios["estado"] not in EstadoOrden.valores():
            raise exceptions.valor_invalido("estado", EstadoOrden.valores())
        if "calificacion" in cambios:
            self._validar_calificacion(cambios["calificacion"])

        return self.repo.update(orden, cambios)

    def eliminar_orden(self, orden_id: int) -> None:
        orden = self.obtener_por_id_o_fallar(orden_id)
        self.repo.delete(orden)
