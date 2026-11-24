"""
Pruebas Unitarias para validación de complejidad de contraseña y hashing.
"""
from app import security
from app.core.constants import PASSWORD_MIN_LONGITUD


def test_password_demasiado_corta():
    es_valida, msg = security.validar_complejidad_password("Ab1!")
    assert not es_valida
    assert f"al menos {PASSWORD_MIN_LONGITUD} caracteres" in msg


def test_password_sin_mayuscula():
    es_valida, msg = security.validar_complejidad_password("password123!")
    assert not es_valida


def test_password_sin_minuscula():
    es_valida, msg = security.validar_complejidad_password("PASSWORD123!")
    assert not es_valida


def test_password_sin_caracter_especial():
    es_valida, msg = security.validar_complejidad_password("Password123")
    assert not es_valida


def test_password_valida_completa():
    es_valida, msg = security.validar_complejidad_password("AutoMetrica2026*")
    assert es_valida
    assert msg == ""


def test_hash_y_verificacion_password():
    plain = "MiClaveSegura#2026"
    hashed = security.hash_password(plain)
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert security.verify_password(plain, hashed) is True
    assert security.verify_password("ClaveEquivocada", hashed) is False
