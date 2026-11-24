"""
Pruebas Unitarias para Clean Code #1: Nombres reveladores y eliminación de números/strings mágicos.
"""
from app.core.constants import (
    RolUsuario,
    EstadoOrden,
    CALIFICACION_MINIMA,
    CALIFICACION_MAXIMA,
    PASSWORD_MIN_LONGITUD,
    BCRYPT_ROUNDS,
    BCRYPT_MAX_BYTES,
    TOKEN_BYTES_SEGURIDAD,
    TOKEN_EXPIRACION_MINUTOS,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)


def test_roles_usuario_enums():
    assert RolUsuario.ADMIN.value == "admin"
    assert RolUsuario.MECANICO.value == "mecanico"
    assert RolUsuario.CLIENTE.value == "cliente"
    valores = RolUsuario.valores()
    assert "admin" in valores
    assert len(valores) == 3


def test_estados_orden_enums():
    assert EstadoOrden.RECIBIDO.value == "Recibido"
    assert EstadoOrden.EN_DIAGNOSTICO.value == "En Diagnóstico"
    assert EstadoOrden.EN_REPARACION.value == "En Reparación"
    assert EstadoOrden.SERVICIO_FINALIZADO.value == "Servicio Finalizado"
    assert EstadoOrden.CANCELADO.value == "Cancelado"
    assert len(EstadoOrden.valores()) == 5


def test_limites_calificacion():
    assert CALIFICACION_MINIMA == 1
    assert CALIFICACION_MAXIMA == 5


def test_parametros_seguridad():
    assert PASSWORD_MIN_LONGITUD == 8
    assert BCRYPT_ROUNDS == 12
    assert BCRYPT_MAX_BYTES == 72
    assert TOKEN_BYTES_SEGURIDAD == 24
    assert TOKEN_EXPIRACION_MINUTOS == 30
    assert JWT_ALGORITHM == "HS256"
    assert len(JWT_SECRET_KEY) > 10
