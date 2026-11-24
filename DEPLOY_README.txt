================================================================================
GUÍA COMPLETA DE DESPLIEGUE EN PRODUCCIÓN - RENDER (PLAN GRATUITO)
Proyecto: AutoMétrica (Backend FastAPI + PostgreSQL | Frontend React + Vite)
================================================================================

NOTA IMPORTANTE DE ARQUITECTURA:
El proyecto AutoMétrica está construido con:
  - Backend: Python + FastAPI + SQLAlchemy (carpeta: autometrica-full/backend)
  - Frontend: React + Vite (carpeta: autometrica-full/frontend)
  - Base de Datos: PostgreSQL externo en Render

En Render (Plan Gratuito), el despliegue óptimo consiste en:
  1. Una base de datos PostgreSQL gratuita en Render.
  2. Un Web Service gratuito para el Backend (FastAPI + Gunicorn/Uvicorn).
  3. Un Static Site gratuito para el Frontend (React + Vite).

--------------------------------------------------------------------------------
1. REQUISITOS PREVIOS
--------------------------------------------------------------------------------
- Cuenta activa en GitHub (https://github.com) con este repositorio subido.
- Cuenta activa en Render (https://render.com) vinculada a tu cuenta de GitHub.
- No subir archivos .env ni bases de datos locales (.db / .sqlite3); el archivo
  .gitignore incluido ya los bloquea automáticamente.

--------------------------------------------------------------------------------
2. VARIABLES DE ENTORNO A CONFIGURAR EN RENDER (BACKEND)
--------------------------------------------------------------------------------
En el panel de tu Web Service en Render (pestaña "Environment"), agrega:

  ENVIRONMENT         = production
  DEBUG               = False
  PYTHON_VERSION      = 3.11.9
  DATABASE_URL        = <Internal Database URL de tu PostgreSQL en Render>
  JWT_SECRET_KEY      = <Genera una cadena aleatoria larga y segura de 32+ chars>
  CORS_ORIGINS        = https://tu-frontend.onrender.com
  FRONTEND_URL        = https://tu-frontend.onrender.com
  SUPERUSER_EMAIL     = admin@tudominio.com
  SUPERUSER_PASSWORD  = TuClaveSegura2026!
  SUPERUSER_NAME      = Administrador AutoMétrica

Variables opcionales para envío real de correos (Gmail SMTP o Resend):
  SMTP_HOST           = smtp.gmail.com
  SMTP_PORT           = 587
  SMTP_USER           = tu_correo@gmail.com
  SMTP_PASSWORD       = tu_clave_de_aplicacion_google_16_caracteres
  SMTP_FROM_NAME      = AutoMétrica Soporte
  SMTP_FROM_EMAIL     = tu_correo@gmail.com
  RESEND_API_KEY      = re_xxxxxxxxxxxxx (opcional si usas Resend)

Variable de entorno para el Frontend (Static Site en Render):
  VITE_API_URL        = https://tu-backend.onrender.com

--------------------------------------------------------------------------------
3. PASO 1: CREAR LA BASE DE DATOS POSTGRESQL EN RENDER
--------------------------------------------------------------------------------
1. Inicia sesión en https://dashboard.render.com.
2. Haz clic en "New +" -> "PostgreSQL".
3. Configura los siguientes datos:
   - Name: autometrica-db
   - Database: autometrica_db
   - User: autometrica_user
   - Region: Oregon (US West) o Virginia (US East) [usa la misma en todo].
   - Instance Type: Free ($0/month).
4. Haz clic en "Create Database".
5. Espera a que el estado cambie a "Available" y copia el valor de
   "Internal Database URL" (empieza por postgresql://...).

--------------------------------------------------------------------------------
4. PASO 2: CONECTAR EL REPOSITORIO Y CREAR EL WEB SERVICE (BACKEND)
--------------------------------------------------------------------------------
1. Sube todo el contenido actualizado de esta carpeta a tu repositorio en GitHub.
   (Si usas Linux/Mac, asegúrate de dar permisos de ejecución a build.sh:
    git update-index --chmod=+x autometrica-full/backend/build.sh)
2. En Render Dashboard, haz clic en "New +" -> "Web Service".
3. Selecciona tu repositorio de GitHub ("Autometrica-main").
4. Completa los campos de configuración exactamente así:
   - Name: autometrica-backend
   - Region: La misma región elegida para tu PostgreSQL.
   - Branch: main
   - Root Directory: autometrica-full/backend
   - Runtime: Python 3
   - Build Command: chmod +x build.sh && ./build.sh
   - Start Command: gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   - Instance Type: Free ($0/month)
5. Haz clic en "Advanced" o ve a la pestaña "Environment" y añade todas las
   variables de entorno listadas en la Sección 2 (especialmente DATABASE_URL,
   SUPERUSER_EMAIL y SUPERUSER_PASSWORD).
6. Haz clic en "Create Web Service".
7. Durante el build, Render ejecutará build.sh, instalará dependencias,
   creará automáticamente todas las tablas en PostgreSQL y registrará el
   superusuario con las credenciales definidas en tus variables de entorno.
8. Copia la URL pública asignada a tu backend (ej: https://autometrica-backend.onrender.com).

--------------------------------------------------------------------------------
5. PASO 3: DESPLEGAR EL FRONTEND (REACT + VITE) EN RENDER
--------------------------------------------------------------------------------
1. En Render Dashboard, haz clic en "New +" -> "Static Site".
2. Selecciona el mismo repositorio de GitHub.
3. Configura los siguientes parámetros:
   - Name: autometrica-frontend
   - Branch: main
   - Root Directory: autometrica-full/frontend
   - Build Command: npm install && npm run build
   - Publish Directory: dist
4. En "Environment Variables", agrega:
   - VITE_API_URL = https://autometrica-backend.onrender.com (sin barra "/" al final)
5. Haz clic en "Create Static Site".
6. IMPORTANTE (Para que React Router funcione sin error 404 al recargar):
   - Ve a la pestaña "Redirects/Rewrites" de tu Static Site.
   - Haz clic en "Add Rule":
     * Source: /*
     * Destination: /index.html
     * Action: Rewrite
   - Guarda los cambios.
7. Regresa a tu Web Service del Backend -> "Environment" y actualiza:
   - CORS_ORIGINS = https://autometrica-frontend.onrender.com
   - FRONTEND_URL = https://autometrica-frontend.onrender.com
   (Render reiniciará el backend automáticamente para aplicar los cambios).

--------------------------------------------------------------------------------
6. VERIFICACIONES POST-DESPLIEGUE
--------------------------------------------------------------------------------
1. Verifica el estado del Backend entrando a:
   https://autometrica-backend.onrender.com/health
   Debe responder: {"status":"ok"}
2. Revisa la pestaña "Logs" en Render para confirmar que aparece:
   "[Base de Datos] Conectado en modo PRODUCCIÓN a PostgreSQL externo."
   "[init_prod] Superusuario creado exitosamente..."
3. Abre la URL de tu Frontend (https://autometrica-frontend.onrender.com) e
   inicia sesión con el SUPERUSER_EMAIL y SUPERUSER_PASSWORD configurados.
4. Si necesitas crear otro superusuario manualmente más adelante, abre la
   pestaña "Shell" en el Web Service (o ejecuta desde tu terminal local con
   la External Database URL) y corre:
   python init_prod.py

--------------------------------------------------------------------------------
7. SOLUCIÓN DE PROBLEMAS COMUNES EN RENDER (PLAN GRATUITO)
--------------------------------------------------------------------------------
- Problema 1: "Permission denied: ./build.sh"
  Solución: Usa como Build Command: chmod +x build.sh && ./build.sh

- Problema 2: La primera petición tarda 30-50 segundos en responder.
  Causa: El plan gratuito de Render suspende ("spin down") los Web Services
  tras 15 minutos de inactividad. Es comportamiento normal del plan gratuito.

- Problema 3: Error de CORS en el navegador al iniciar sesión.
  Solución: Verifica que CORS_ORIGINS en el backend coincida exactamente con la
  URL del frontend (con https:// y sin barra final /).

- Problema 4: Error 404 al recargar rutas como /login o /panel-mecanico.
  Solución: Verifica que agregaste la regla Rewrite (/* -> /index.html) en la
  pestaña Redirects/Rewrites del Static Site en Render.

- Problema 5: Pérdida de datos tras 30 días.
  Causa: Las bases de datos PostgreSQL gratuitas en Render expiran a los 30
  días. Crea respaldos periódicos con pg_dump o migra al plan Starter ($7/mes).
================================================================================
