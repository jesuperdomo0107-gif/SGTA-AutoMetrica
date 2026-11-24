"""
Proveedores de dependencias para inyección en FastAPI (SOLID - D).
Permite desacoplar los endpoints de implementaciones concretas y facilita el testing.
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.ordenes_repo import OrdenesRepository
from app.services.ordenes_service import OrdenesService


def get_ordenes_service(db: Session = Depends(get_db)) -> OrdenesService:
    repo = OrdenesRepository(db)
    return OrdenesService(repo)


from typing import Optional, List
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app import security, models

security_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db),
) -> Optional[models.Usuario]:
    """Obtiene el usuario actual a partir del token JWT Bearer si se proporciona."""
    if not auth or not auth.credentials:
        return None
    payload = security.decodificar_token(auth.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de sesión inválido o expirado. Por favor inicia sesión nuevamente.",
        )
    usuario_id = payload.get("sub")
    if not usuario_id:
        return None
    return db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()


def requerir_autenticacion(usuario: Optional[models.Usuario] = Depends(get_current_user)) -> models.Usuario:
    """Exige que la petición provenga de un usuario debidamente autenticado con JWT."""
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: se requiere token de autenticación.",
        )
    return usuario


def requerir_roles(roles_permitidos: List[str]):
    """Genera una dependencia que valida si el usuario tiene uno de los roles permitidos."""
    def verificador_rol(usuario: models.Usuario = Depends(requerir_autenticacion)):
        if usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requiere uno de los roles {roles_permitidos}.",
            )
        return usuario
    return verificador_rol

