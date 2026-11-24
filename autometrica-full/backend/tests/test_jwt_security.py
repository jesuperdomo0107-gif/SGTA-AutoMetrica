"""
Pruebas Unitarias para Autenticación con Tokens JWT en AutoMétrica.
Valida la generación, firma criptográfica, expiración y decodificación de tokens JWT.
"""
import datetime
from app import security


def test_generacion_y_decodificacion_token_jwt():
    """Verifica que un token generado con payload se decodifique con los mismos datos."""
    payload_original = {
        "sub": "42",
        "correo": "admin@autometrica.com",
        "rol": "admin",
        "taller_id": 1,
        "nombre": "Administrador Principal",
    }
    token = security.crear_access_token(payload_original)
    assert isinstance(token, str)
    assert len(token) > 20

    payload_decodificado = security.decodificar_token(token)
    assert payload_decodificado is not None
    assert payload_decodificado["sub"] == "42"
    assert payload_decodificado["correo"] == "admin@autometrica.com"
    assert payload_decodificado["rol"] == "admin"
    assert payload_decodificado["taller_id"] == 1


def test_token_jwt_expirado():
    """Verifica que un token con tiempo expirado sea rechazado (retorne None)."""
    payload = {"sub": "99", "correo": "expirado@taller.com"}
    # Expirado hace 10 minutos
    delta_negativo = datetime.timedelta(minutes=-10)
    token_expirado = security.crear_access_token(payload, expires_delta=delta_negativo)

    resultado = security.decodificar_token(token_expirado)
    assert resultado is None


def test_token_jwt_manipulado_o_invalido():
    """Verifica que firmas falsas o manipuladas no sean aceptadas."""
    resultado = security.decodificar_token("token.completamente.falso.invalido")
    assert resultado is None
