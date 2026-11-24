from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from app.database import settings, is_production

app = FastAPI(
    title="Autometrica API",
    version="1.0.0",
    docs_url=None if is_production and not settings.DEBUG else "/docs",
    redoc_url=None if is_production and not settings.DEBUG else "/redoc",
)

cors_origins_env = settings.CORS_ORIGINS.strip()
if cors_origins_env == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database import engine, Base
from app.routers import (
    talleres,
    usuarios,
    clientes,
    vehiculos,
    mecanicos,
    tipos_reparacion,
    ordenes,
    repuestos,
    historial_estados,
    mensajes,
    proximos_servicios,
    reportes_ingresos,
    contactos_web,
    citas,
    inventario,
    presupuestos,
    facturas,
    proveedores,
    audit_logs,
)

# Crear tablas si no existen y verificar columnas requeridas
try:
    Base.metadata.create_all(bind=engine)
    
    # Migración de columnas adicionales en tablas existentes si aplica
    from sqlalchemy import text
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE talleres ADD COLUMN IF NOT EXISTS codigo_unico VARCHAR(30);"))
            conn.execute(text("ALTER TABLE tipos_reparacion ADD COLUMN IF NOT EXISTS mecanico_id INTEGER;"))
            conn.execute(text("ALTER TABLE tipos_reparacion ADD COLUMN IF NOT EXISTS precio_base NUMERIC(10, 2) DEFAULT 0;"))
            conn.execute(text("ALTER TABLE tipos_reparacion ADD COLUMN IF NOT EXISTS tiempo_estimado_min INTEGER DEFAULT 60;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS garantia_dias INTEGER DEFAULT 0;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS garantia_vencimiento DATE;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS tiempo_inicio TIMESTAMP;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS tiempo_fin TIMESTAMP;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS tiempo_total_minutos INTEGER DEFAULT 0;"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN IF NOT EXISTS fotos_urls TEXT;"))
            conn.execute(text("ALTER TABLE presupuestos ADD COLUMN IF NOT EXISTS taller_id INTEGER;"))
            conn.execute(text("ALTER TABLE presupuestos ADD COLUMN IF NOT EXISTS vehiculo_id INTEGER;"))
            conn.execute(text("ALTER TABLE presupuestos ADD COLUMN IF NOT EXISTS cliente_id INTEGER;"))
            conn.execute(text("ALTER TABLE presupuestos ADD COLUMN IF NOT EXISTS mecanico_id INTEGER;"))
            conn.execute(text("ALTER TABLE presupuestos ALTER COLUMN orden_id DROP NOT NULL;"))
        except Exception as _e:
            pass

    print("[Base de Datos] Esquemas y tablas sincronizados correctamente (sin datos quemados).")

except Exception as e:
    print(f"[Advertencia] No se pudo conectar a la base de datos al iniciar: {e}")

PREFIX = "/api/v1"

app.include_router(talleres.router, prefix=PREFIX)
app.include_router(usuarios.router, prefix=PREFIX)
app.include_router(clientes.router, prefix=PREFIX)
app.include_router(vehiculos.router, prefix=PREFIX)
app.include_router(mecanicos.router, prefix=PREFIX)
app.include_router(tipos_reparacion.router, prefix=PREFIX)
app.include_router(ordenes.router, prefix=PREFIX)
app.include_router(repuestos.router, prefix=PREFIX)
app.include_router(historial_estados.router, prefix=PREFIX)
app.include_router(mensajes.router, prefix=PREFIX)
app.include_router(proximos_servicios.router, prefix=PREFIX)
app.include_router(reportes_ingresos.router, prefix=PREFIX)
app.include_router(contactos_web.router, prefix=PREFIX)
app.include_router(citas.router, prefix=PREFIX)
app.include_router(inventario.router, prefix=PREFIX)
app.include_router(presupuestos.router, prefix=PREFIX)
app.include_router(facturas.router, prefix=PREFIX)
app.include_router(proveedores.router, prefix=PREFIX)
app.include_router(audit_logs.router, prefix=PREFIX)


@app.get("/")
def root():
    return {"mensaje": "Autometrica API funcionando", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(f"{PREFIX}/sistema/limpiar-base-datos")
def limpiar_base_datos():
    """Limpia completamente todas las tablas de la base de datos para iniciar pruebas limpias desde cero."""
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        # Eliminar registros en orden de dependencias
        for modelo in [
            models.ItemPresupuesto,
            models.Presupuesto,
            models.Pago,
            models.Factura,
            models.RepuestoOrden,
            models.HistorialEstado,
            models.Mensaje,
            models.ProximoServicio,
            models.Cita,
            models.OrdenCompra,
            models.OrdenServicio,
            models.TipoReparacion,
            models.InventarioItem,
            models.Proveedor,
            models.Vehiculo,
            models.Cliente,
            models.Mecanico,
            models.AuditLog,
            models.ContactoWeb,
            models.Usuario,
        ]:
            try:
                db.query(modelo).delete()
            except Exception:
                pass
        db.commit()
        db.close()
        return {"mensaje": "Base de datos limpiada exitosamente. Se preservaron los talleres y se eliminaron todos los usuarios, clientes, vehículos y órdenes."}
    except Exception as e:
        return {"error": f"Error al limpiar la base de datos: {e}"}
