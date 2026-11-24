"""
Script de inicialización de producción para Render:
1. Verifica conexión a PostgreSQL y crea/actualiza todas las tablas del esquema.
2. Crea un taller base si no existe ninguno.
3. Crea un superusuario (rol 'admin') de forma idempotente usando variables de entorno:
   - SUPERUSER_EMAIL (o ADMIN_EMAIL)
   - SUPERUSER_PASSWORD (o ADMIN_PASSWORD)
   - SUPERUSER_NAME (opcional, por defecto 'Administrador AutoMétrica')
"""
import os
import sys
from app.database import engine, SessionLocal, Base
from app import models, security


def init_database():
    print("[init_prod] Sincronizando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("[init_prod] Tablas verificadas/creadas correctamente.")


def create_superuser():
    admin_email = (os.getenv("SUPERUSER_EMAIL") or os.getenv("ADMIN_EMAIL") or "").strip().lower()
    admin_password = (os.getenv("SUPERUSER_PASSWORD") or os.getenv("ADMIN_PASSWORD") or "").strip()
    admin_name = (os.getenv("SUPERUSER_NAME") or os.getenv("ADMIN_NAME") or "Administrador AutoMétrica").strip()

    if not admin_email or not admin_password:
        print(
            "[init_prod] AVISO: SUPERUSER_EMAIL / SUPERUSER_PASSWORD no definidos en las variables de entorno. "
            "Omitiendo creación automática de superusuario."
        )
        return

    db = SessionLocal()
    try:
        # Asegurar que exista al menos un taller principal
        taller = db.query(models.Taller).first()
        if not taller:
            taller = models.Taller(
                nombre="AutoMétrica Sede Principal",
                codigo_unico="AM-PRINCIPAL-001",
                nit="900000000-1",
                correo=admin_email,
                ciudad="Bogotá",
                activo=True,
            )
            db.add(taller)
            db.commit()
            db.refresh(taller)
            print(f"[init_prod] Taller principal creado: {taller.nombre} ({taller.codigo_unico})")

        # Verificar si el superusuario ya existe
        existente = db.query(models.Usuario).filter(models.Usuario.correo == admin_email).first()
        if existente:
            print(f"[init_prod] El superusuario '{admin_email}' ya existe (ID: {existente.id}). No se realizan cambios.")
            return

        nuevo_admin = models.Usuario(
            taller_id=taller.id,
            nombre_completo=admin_name,
            correo=admin_email,
            contrasena_hash=security.hash_password(admin_password),
            rol="admin",
            activo=True,
        )
        db.add(nuevo_admin)
        db.commit()
        print(f"[init_prod] Superusuario creado exitosamente: {admin_email} (rol: admin)")
    except Exception as e:
        db.rollback()
        print(f"[init_prod] Error al crear superusuario: {e}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    create_superuser()
